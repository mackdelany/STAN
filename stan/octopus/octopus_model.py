
from pathlib import Path

import torch
from torch import nn
from transformers import DistilBertModel, DistilBertConfig

from .training_util import concat_tensors_in_dict


class OctopusModel(nn.Module):
    def __init__(
        self,
        device,
        class_weights=None,
        model_path: str = './stan/model/saved/hf/triage',
        octopus_model_name: str = 'octopus_triage_model',
        octopus_config_name: str = 'octopus_model_config'
    ):
        """
        """
        super(OctopusModel, self).__init__()
        self.device = device
        self.class_weights = class_weights
        if class_weights is None:
            self._init_default_class_weights()

        print('\nLoading config, distilbert-base-uncased from pretrained')
        self.config = DistilBertConfig.from_pretrained(
            str(Path(model_path, octopus_config_name)), return_dict=True
        )
        print('\nLoading model, distilbert-base-uncased from pretrained')
        self.distilbert = DistilBertModel.from_pretrained(
            str(Path(model_path, octopus_model_name)), config=self.config
        ).to(self.device)

        # pooling
        self.pooling_layer = nn.Linear(768, 768, bias=True).to(self.device)
        self.pooling_dropout = nn.Dropout(0.2).to(self.device)

        # triage code --> 1 output y1
        self.tc_classifier = nn.Linear(768, 5, bias=True).to(self.device)
        self.tc_loss = nn.CrossEntropyLoss(
            weight=self.class_weights['tc_weights']).to(self.device)
        self.triage_code_output = nn.Softmax(-1).to(self.device)

        # abcd --> 7 outputs y2-y8
        self.abcd_classifier = nn.Linear(768, 7, bias=True).to(self.device)
        self.abcd_loss = nn.BCEWithLogitsLoss(
            pos_weight=self.class_weights['abcd_pos_weights']).to(self.device)
        self.abcd_sigmoid = nn.Sigmoid().to(self.device)

        # output --> 1 output y9
        self.sepsis_classifier = nn.Linear(768, 1, bias=True).to(self.device)
        self.sepsis_loss = nn.BCEWithLogitsLoss(
            pos_weight=self.class_weights['sepsis_pos_weights']).to(self.device)
        self.sepsis_sigmoid = nn.Sigmoid().to(self.device)

        self.model_params = [
            {'params': self.distilbert.parameters()},
            {'params': self.pooling_layer.parameters()},
            {'params': self.tc_classifier.parameters()},
        ]

    def _init_default_class_weights(self):
        self.class_weights = {
            'tc_weights': torch.tensor([60.,  3.,  1.,  2., 40.]),
            'abcd_pos_weights': torch.tensor([112.3690,   9.3967,   8.8409,  64.8862,  48.3711,  82.6667,  12.1245]),
            'sepsis_pos_weights': torch.tensor(131.1806)
        }

    def forward(self, inputs):
        """
        """
        output = self.distilbert(**inputs)
        hidden_state = output.last_hidden_state     # (bs, seq_length, dim)
        pooled_output = hidden_state[:, 0]          # (bs, dim)

        # pooling
        pooled_output = self.pooling_layer(pooled_output)
        pooled_output = nn.ReLU()(pooled_output)
        pooled_output = self.pooling_dropout(pooled_output)

        tc_logits = self.tc_classifier(pooled_output)
        tc_probs = self.triage_code_output(tc_logits)

        # abcd
        abcd_logits = self.abcd_classifier(pooled_output)
        abcd_probs = self.abcd_sigmoid(abcd_logits)

        # outputs
        sepsis_logits = self.sepsis_classifier(pooled_output)
        sepsis_probs = self.sepsis_sigmoid(sepsis_logits)

        outputs = {
            'tc_logits': tc_logits,
            'tc_probs': tc_probs,
            'abcd_logits': abcd_logits,
            'abcd_probs': abcd_probs,
            'sepsis_logits': sepsis_logits,
            'sepsis_probs': sepsis_probs
        }

        return outputs

    def calculate_losses(self, labels, outputs):
        """
        """

        # triage code
        tc_loss = self.tc_loss(outputs['tc_logits'], labels['y1_triage_code'])

        # abcd
        abcd_labels = torch.cat((
            labels['y2_airway_altered'].reshape(-1, 1),
            labels['y3_breathing_altered'].reshape(-1, 1),
            labels['y4_circulation_altered'].reshape(-1, 1),
            labels['y5_disability_altered'].reshape(-1, 1),
            labels['y6_neuro_altered'].reshape(-1, 1),
            labels['y7_immunocompromised'].reshape(-1, 1),
            labels['y8_mental_health'].reshape(-1, 1)
        ), 1).type_as(outputs['abcd_logits'])

        abcd_loss = self.abcd_loss(outputs['abcd_logits'], abcd_labels)

        # sepsis
        sepsis_labels = labels['y9_sepsis'].reshape(
            -1, 1).type_as(outputs['sepsis_logits'])
        sepsis_loss = self.sepsis_loss(outputs['sepsis_logits'], sepsis_labels)

        losses = {
            'tc_loss': tc_loss,
            'abcd_loss': abcd_loss,
            'sepsis_loss': sepsis_loss
        }

        return losses

    def load_params(self, path_to_param_dict, for_eval=True):
        if self.device == 'cuda':
            params = torch.load(path_to_param_dict)
        else:
            params = torch.load(path_to_param_dict,
                                map_location=torch.device('cpu'))
        self.load_state_dict(params)
        if for_eval:
            self.eval()   # using for inference...

    def infer_in_batches(self, input_ids, attn_mask, batch_size):
        val_batches_unrounded = input_ids.shape[0] / batch_size
        # round up and return int without importing math
        val_batches = int(-(-val_batches_unrounded // 1))

        print('Evaluating {} examples {} times'.format(batch_size, val_batches))
        outputs = None
        for ite in range(val_batches):
            ite_input_ids = input_ids[ite*batch_size:(ite+1)*batch_size, :]
            ite_attn_mask = attn_mask[ite*batch_size:(ite+1)*batch_size, :]
            ite_inputs = {'input_ids': ite_input_ids,
                          'attention_mask': ite_attn_mask}
            ite_outputs = self.forward(ite_inputs)
            outputs = concat_tensors_in_dict(ite_outputs, outputs)
        assert (val_examples :=
                input_ids.shape[0]) == outputs['tc_probs'].shape[0]

        return outputs, val_examples

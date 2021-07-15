
from collections import namedtuple
from pathlib import Path

import torch
from transformers import DistilBertTokenizer

from ..core.triage_request import TriageRequest
from ..core.stan_sequence_util import generate_stan_sequence
from .i_octopus_model import IOctopusModel
from ..octopus.octopus_model import OctopusModel


OctopusResult = namedtuple(
    'OctopusResult', [
        'tc_probs',
        'airway_altered',
        'breathing_altered',
        'circulation_altered',
        'disability_altered',
        'neuro_altered',
        'immunocompromised',
        'mental_health_concerns',
        'sepsis'
    ]
)


class OctopusWrapper(IOctopusModel):
    ROOT_MODEL_PATH = 'stan/model/saved/octopus'
    ABCD_CLASSES = []
    THRESHOLDS = {
        'airway_altered': 0.5,
        'breathing_altered': 0.5,
        'circulation_altered': 0.5,
        'disability_altered': 0.5,
        'neuro_altered': 0.5,
        'immunocompromised': 0.5,
        'mental_health_concerns': 0.5,
        'sepsis': 0.5,
    }

    def __init__(
        self,
        model_to_load='test_model',
        debug=False,
        model_max_length: int = 512,
        model_path: str = './stan/model/saved/hf/triage',
        octopus_tokenizer_name: str = 'octopus_tokenizer'
    ):
        self.debug = debug
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')
        print('Using device: {}'.format(self.device))

        self.model = OctopusModel(
            self.device
        )

        path_to_model = Path.cwd() / OctopusWrapper.ROOT_MODEL_PATH / model_to_load
        self.model.load_params(str(path_to_model), for_eval=True)

        print('\nLoading tokenizer, distilbert-base-uncased from pretrained')
        self.tokenizer = DistilBertTokenizer.from_pretrained(
            str(Path(model_path, octopus_tokenizer_name)),
            max_length=model_max_length
        )
        assert self.tokenizer.model_max_length == model_max_length
        print('\nModel loaded')

    def triage(self, triage_request: TriageRequest):
        """
        """
        sequence = generate_stan_sequence(triage_request)
        if self.debug:
            print('\nConstructed sequence:\n{}\n'.format(sequence))

        inputs = self.tokenizer(
            sequence, truncation=True, padding='max_length', return_tensors='pt'
        )

        outputs = self.model.forward(inputs)
        tc_probs = outputs['tc_probs'].reshape(-1)
        abcd_probs = outputs['abcd_probs'].reshape(-1)
        outcomes = outputs['sepsis_probs'].reshape(-1)

        triage_request.set_tc_probs(tc_probs)

        airway_altered_pred = OctopusWrapper.THRESHOLDS['airway_altered'] <= abcd_probs[0].item(
        )
        breathing_altered_pred = OctopusWrapper.THRESHOLDS['breathing_altered'] <= abcd_probs[1].item(
        )
        circulation_altered_pred = OctopusWrapper.THRESHOLDS['circulation_altered'] <= abcd_probs[2].item(
        )
        disability_altered_pred = OctopusWrapper.THRESHOLDS['disability_altered'] <= abcd_probs[3].item(
        )
        neuro_altered_pred = OctopusWrapper.THRESHOLDS['neuro_altered'] <= abcd_probs[4].item(
        )
        immunocompromised_pred = OctopusWrapper.THRESHOLDS['immunocompromised'] <= abcd_probs[5].item(
        )
        mental_health_concerns_pred = OctopusWrapper.THRESHOLDS['mental_health_concerns'] <= abcd_probs[6].item(
        )
        sepsis_pred = OctopusWrapper.THRESHOLDS['sepsis'] <= outcomes[0].item()

        if self.debug:
            tc_prob_1 = tc_probs[0].item()
            tc_prob_2 = tc_probs[1].item()
            tc_prob_3 = tc_probs[2].item()
            tc_prob_4 = tc_probs[3].item()
            tc_prob_5 = tc_probs[4].item()
            print('\nProcessed octopus:')
            print(
                f'Nurse triage code: {triage_request.nurse_triage_code}'
                f'\tSTAN probs 1:{tc_prob_1:.2f} 2:{tc_prob_2:.2f} 3:{tc_prob_3:.2f} 4:{tc_prob_4:.2f} 5:{tc_prob_5:.2f}'
            )
            print(
                f'Airway measured {triage_request.airway_was_measured}\tSTAN {airway_altered_pred}:{abcd_probs[0].item():.2f}\tnurse {triage_request.airway_altered}')
            print(
                f'Breathing measured {triage_request.breathing_was_measured}\tSTAN {breathing_altered_pred}:{abcd_probs[1].item():.2f}\tnurse {triage_request.breathing_altered}')
            print(
                f'Circulation measured {triage_request.circulation_was_measured}\tSTAN {circulation_altered_pred}:{abcd_probs[2].item():.2f}\tnurse {triage_request.circulation_altered}')
            print(
                f'Disability measured {triage_request.disability_gcs_was_measured}\tSTAN {disability_altered_pred}:{abcd_probs[3].item():.2f}\tnurse {triage_request.disability_gcs}')
            print(
                f'Neuro measured {triage_request.neuro_was_measured}\tSTAN {neuro_altered_pred}:{abcd_probs[4].item():.2f}\tnurse {triage_request.neuro_altered}')
            print(
                f'Immunocompromised measured {triage_request.immunocompromised_was_measured}\tSTAN {immunocompromised_pred}:{abcd_probs[5].item():.2f}\tnurse {triage_request.immunocompromised}')
            print(
                f'Mental health measured {triage_request.mental_health_was_measured}\tSTAN {mental_health_concerns_pred}:{abcd_probs[6].item():.2f}\tnurse {triage_request.mental_health_concerns}')
            print(f'Sepsis predicted: {sepsis_pred}:{outcomes[0].item():.2f}')

        triage_request.review_airway_prediction(airway_altered_pred)
        triage_request.review_breathing_prediction(breathing_altered_pred)
        triage_request.review_circulation_prediction(circulation_altered_pred)
        triage_request.review_disability_prediction(disability_altered_pred)
        triage_request.review_neuro_prediction(neuro_altered_pred)
        triage_request.review_immuno_prediction(immunocompromised_pred)
        triage_request.review_mh_prediction(mental_health_concerns_pred)

        triage_request.review_outcome_prediction(
            {'sepsis_pred': sepsis_pred}
        )

        triage_request

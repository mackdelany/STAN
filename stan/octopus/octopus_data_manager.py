
import pandas as pd
from transformers import DistilBertTokenizer
import torch
from torch.utils.data import DataLoader

from .training_util import pd_series_to_tensor


class OctopusDataset(torch.utils.data.Dataset):
    """
    Expecting .csv with columns:
    'X'
    'y1_triage_code',
    'y2_airway_altered',
    'y3_breathing_altered',
    'y4_circulation_altered',
    'y5_disability_altered',
    'y6_neuro_altered',
    'y7_immunocompromised',
    'y8_mental_health',
    'y9_sepsis'
    """

    def __init__(self, labels, encodings):
        self.labels = labels
        self.encodings = encodings

    def __getitem__(self, idx):
        sequences = {key: torch.tensor(val[idx])
                     for key, val in self.encodings.items()}
        labels = self.labels[idx]
        item = {'X': {**sequences}, 'labels': {**labels}}
        return item

    def __len__(self):
        return len(self.labels)


class OctopusDataManager():
    contexts = {
        'context_1': ['EPS_FAST', 'EPSI_FAST', 'ESNO_FAST', 'EPS_VITAL', 'EPSI_VITAL', 'ESNO_VITAL'],
        'context_2': ['STAN_FAST', 'STAN_VITAL'],
        'context_3': ['EPS_FULL', 'EPSI_FULL', 'ESNO_FULL'],
        'context_4': ['STAN_FULL']
    }

    triage_code_contexts = ['context_1', 'context_2', 'context_3', 'context_4']
    abcd_contexts = ['context_1', 'context_2']
    outcome_contexts = ['context_1', 'context_3']

    def __init__(
        self,
        device,
        batch_size=1,
        tokenizer=None,
        path_to_data='/Users/mackdelany/Documents/STAN/stan_model/data/stan_one_training_23_12.csv',
        debug=False
    ):
        self.debug = debug
        self.device = device
        self.stan_data = pd.read_csv(path_to_data)
        self.batch_size = batch_size
        self._init_tokenizer(tokenizer)
        self._init_datasets()
        self._init_dataloaders()

    def get_data_classes_for_output(self, layer):
        if layer == 'triage_code':
            layer_contexts = OctopusDataManager.triage_code_contexts
        elif layer == 'abcd':
            layer_contexts = OctopusDataManager.abcd_contexts
        elif layer == 'outcome':
            layer_contexts = OctopusDataManager.outcome_contexts
        data_classes = []
        for context in layer_contexts:
            data_classes += OctopusDataManager.contexts[context]
        return data_classes

    def _init_tokenizer(self, tokenizer):
        if tokenizer:
            self.tokenizer = tokenizer
        else:
            self.tokenizer = DistilBertTokenizer.from_pretrained(
                'distilbert-base-uncased')

    def _init_datasets(self):
        print('\nLoading datasets..{} examples total'.format(
            self.stan_data.shape[0]))

        # -1 from triage code... #TODO decide if cleaner way to do this..
        self.stan_data['y1_triage_code'] = self.stan_data['y1_triage_code'] - 1
        self.train_df = self.stan_data[~self.stan_data.test_set].copy(
            deep=True).reset_index(drop=True)
        self.val_df = self.stan_data[self.stan_data.test_set].copy(
            deep=True).reset_index(drop=True)
        print('\nTotal train size: {}\nTotal test size: {}'.format(
            self.train_df.shape, self.val_df.shape))
        if not self.debug:
            df_1 = self.train_df[self.train_df.data_class.isin(
                OctopusDataManager.contexts['context_1'])]
            df_2 = self.train_df[self.train_df.data_class.isin(
                OctopusDataManager.contexts['context_2'])]
            df_3 = self.train_df[self.train_df.data_class.isin(
                OctopusDataManager.contexts['context_3'])]
            df_4 = self.train_df[self.train_df.data_class.isin(
                OctopusDataManager.contexts['context_4'])]
        else:
            df_1 = self.train_df[self.train_df.data_class.isin(
                OctopusDataManager.contexts['context_1'])].iloc[0:2000, :]
            df_2 = self.train_df[self.train_df.data_class.isin(
                OctopusDataManager.contexts['context_2'])].iloc[0:2000, :]
            df_3 = self.train_df[self.train_df.data_class.isin(
                OctopusDataManager.contexts['context_3'])].iloc[0:2000, :]
            df_4 = self.train_df[self.train_df.data_class.isin(
                OctopusDataManager.contexts['context_4'])].iloc[0:2000, :]

        def return_label_dict(data: tuple):
            label_dict = {
                'data_class': data.data_class,
                'y1_triage_code': data.y1_triage_code,
                'y2_airway_altered': data.y2_airway_altered,
                'y3_breathing_altered': data.y3_breathing_altered,
                'y4_circulation_altered': data.y4_circulation_altered,
                'y5_disability_altered': data.y5_disability_altered,
                'y6_neuro_altered': data.y6_neuro_altered,
                'y7_immunocompromised': data.y7_immunocompromised,
                'y8_mental_health': data.y8_mental_health,
                'y9_sepsis': data.y9_sepsis
            }
            return label_dict

        labels_1 = []
        labels_2 = []
        labels_3 = []
        labels_4 = []
        for event in df_1.itertuples():
            label_dict = return_label_dict(event)
            labels_1.append(label_dict)
        for event in df_2.itertuples():
            label_dict = return_label_dict(event)
            labels_2.append(label_dict)
        for event in df_3.itertuples():
            label_dict = return_label_dict(event)
            labels_3.append(label_dict)
        for event in df_4.itertuples():
            label_dict = return_label_dict(event)
            labels_4.append(label_dict)

        encodings_1 = self.tokenizer(
            df_1.X.tolist(), truncation=True, padding=True)
        encodings_2 = self.tokenizer(
            df_2.X.tolist(), truncation=True, padding=True)
        encodings_3 = self.tokenizer(
            df_3.X.tolist(), truncation=True, padding=True)
        encodings_4 = self.tokenizer(
            df_4.X.tolist(), truncation=True, padding=True)
        self.val_encodings = self.tokenizer(
            self.val_df.X.tolist(), truncation=True, padding=True, return_tensors='pt')
        self.train_1 = OctopusDataset(labels_1, encodings_1)
        self.train_2 = OctopusDataset(labels_2, encodings_2)
        self.train_3 = OctopusDataset(labels_3, encodings_3)
        self.train_4 = OctopusDataset(labels_4, encodings_4)

        if torch.cuda.is_available():
            #print('Moving data to GPU...')
            pass

    def _init_dataloaders(self):
        print('\nInitializing dataloaders..')
        self.train_loader_1 = DataLoader(
            self.train_1, batch_size=self.batch_size, pin_memory=True)
        self.train_loader_2 = DataLoader(
            self.train_2, batch_size=self.batch_size, pin_memory=True)
        self.train_loader_3 = DataLoader(
            self.train_3, batch_size=self.batch_size, pin_memory=True)
        self.train_loader_4 = DataLoader(
            self.train_4, batch_size=self.batch_size, pin_memory=True)
        self.train_contexts = {
            'context_1': self.train_loader_1,
            'context_2': self.train_loader_2,
            'context_3': self.train_loader_3,
            'context_4': self.train_loader_4
        }

    def init_class_weights(self, return_weights=True):
        print('\nLoading class weights')
        # triage code
        tc_counts = self.train_df.y1_triage_code.value_counts()
        tc_weights = torch.zeros(5)
        """
        tc_weights[0] = tc_counts.sum() / tc_counts[0]
        tc_weights[1] = tc_counts.sum() / tc_counts[1]
        tc_weights[2] = tc_counts.sum() / tc_counts[2]
        tc_weights[3] = tc_counts.sum() / tc_counts[3]
        tc_weights[4] = tc_counts.sum() / tc_counts[4]
        """
        # changed for XP
        tc_weights[0] = 60
        tc_weights[1] = 3
        tc_weights[2] = 1
        tc_weights[3] = 2
        tc_weights[4] = 40

        def get_pos_weight_from_series(series):
            """Get pos class weight scaler from pandas series of 1s and 0s.
            As per: https://pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html#torch.nn.BCEWithLogitsLoss
            """
            pos_count = (series == 1).sum()
            neg_count = (series == 0).sum()
            assert pos_count + neg_count == series.shape[0]
            pos_weight = neg_count / pos_count
            pos_weight = 0.5 * pos_weight
            return pos_weight

        abcd_pos_weights = torch.tensor([
            get_pos_weight_from_series(self.train_df.y2_airway_altered),
            get_pos_weight_from_series(self.train_df.y3_breathing_altered),
            get_pos_weight_from_series(self.train_df.y4_circulation_altered),
            get_pos_weight_from_series(self.train_df.y5_disability_altered),
            get_pos_weight_from_series(self.train_df.y6_neuro_altered),
            get_pos_weight_from_series(self.train_df.y7_immunocompromised),
            get_pos_weight_from_series(self.train_df.y8_mental_health)
        ])

        sepsis_pos_weights = torch.tensor(
            get_pos_weight_from_series(self.train_df.y9_sepsis))

        self.weights = {
            'tc_weights': tc_weights,
            'abcd_pos_weights': abcd_pos_weights,
            'sepsis_pos_weights': sepsis_pos_weights
        }
        if return_weights:
            return self.weights

    def init_val_data(self):
        # moved pd_series_to_tensor to core #TODO check still works
        self.y1_val_tensor = pd_series_to_tensor(self.val_df.y1_triage_code)
        self.y2_val_tensor = pd_series_to_tensor(self.val_df.y2_airway_altered)
        self.y3_val_tensor = pd_series_to_tensor(
            self.val_df.y3_breathing_altered)
        self.y4_val_tensor = pd_series_to_tensor(
            self.val_df.y4_circulation_altered)
        self.y5_val_tensor = pd_series_to_tensor(
            self.val_df.y5_disability_altered)
        self.y6_val_tensor = pd_series_to_tensor(self.val_df.y6_neuro_altered)
        self.y7_val_tensor = pd_series_to_tensor(
            self.val_df.y7_immunocompromised)
        self.y8_val_tensor = pd_series_to_tensor(self.val_df.y8_mental_health)
        self.y9_val_tensor = pd_series_to_tensor(self.val_df.y9_sepsis)

        tc_contexts = self.get_data_classes_for_output('triage_code')
        abcd_contexts = self.get_data_classes_for_output('abcd')
        outcome_contexts = self.get_data_classes_for_output('outcome')

        self.tc_val_context_mask = torch.tensor(
            self.val_df.data_class.isin(tc_contexts))
        self.abcd_val_context_mask = torch.tensor(
            self.val_df.data_class.isin(abcd_contexts))
        self.outcome_val_context_mask = torch.tensor(
            self.val_df.data_class.isin(outcome_contexts))

        self.y1_val_tensor = torch.masked_select(
            self.y1_val_tensor, self.tc_val_context_mask)
        self.y2_val_tensor = torch.masked_select(
            self.y2_val_tensor, self.abcd_val_context_mask)
        self.y3_val_tensor = torch.masked_select(
            self.y3_val_tensor, self.abcd_val_context_mask)
        self.y4_val_tensor = torch.masked_select(
            self.y4_val_tensor, self.abcd_val_context_mask)
        self.y5_val_tensor = torch.masked_select(
            self.y5_val_tensor, self.abcd_val_context_mask)
        self.y6_val_tensor = torch.masked_select(
            self.y6_val_tensor, self.abcd_val_context_mask)
        self.y7_val_tensor = torch.masked_select(
            self.y7_val_tensor, self.abcd_val_context_mask)
        self.y8_val_tensor = torch.masked_select(
            self.y8_val_tensor, self.abcd_val_context_mask)
        self.y9_val_tensor = torch.masked_select(
            self.y9_val_tensor, self.outcome_val_context_mask)

        assert self.y1_val_tensor.shape[0] == self.val_df.shape[0]
        assert self.y2_val_tensor.shape[0] != self.val_df.shape[0]

        self.y1_val_tensor = self.y1_val_tensor.to(self.device)
        self.y2_val_tensor = self.y2_val_tensor.to(self.device)
        self.y3_val_tensor = self.y3_val_tensor.to(self.device)
        self.y4_val_tensor = self.y4_val_tensor.to(self.device)
        self.y5_val_tensor = self.y5_val_tensor.to(self.device)
        self.y6_val_tensor = self.y6_val_tensor.to(self.device)
        self.y7_val_tensor = self.y7_val_tensor.to(self.device)
        self.y8_val_tensor = self.y8_val_tensor.to(self.device)
        self.y9_val_tensor = self.y9_val_tensor.to(self.device)

"""
"""

from pathlib import Path
from typing import Tuple

import torch
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer

from ..core.stan_sequence_util import generate_stan_sequence
from ..core.triage_request import TriageRequest
from .i_stan_model import IStanModel


class DistilBertRegressor(IStanModel):
    """
    Class for num_labels = 1.

    Output is a single scaler triage code prediction.
    """

    def __init__(
        self,
        model_path: str,
        pc_uncertainty_path: str,
        model_max_length: int = 512,
        tokenizer_path: str = './stan/model/saved/hf/predict/stan_tokenizer',
        debug=False
    ):
        self._init_pc_uncertainty(pc_uncertainty_path)
        self._init_tokenizer(tokenizer_path, model_max_length)
        self._init_model(model_path)
        self.debug_mode = debug

    def __call__(self, triage_request: TriageRequest) -> Tuple[float, list]:
        """
        """
        triage_code, prediction_distribution = self.predict(triage_request)
        return triage_code, prediction_distribution

    def _init_tokenizer(self, tokenizer_path, model_max_length):
        """
        """
        print('\nLoading tokenizer, distilbert-base-uncased from pretrained')
        self.tokenizer = DistilBertTokenizer.from_pretrained(
            tokenizer_path,
            max_length=model_max_length
        )

    def _init_model(self, model_path):
        """
        """
        self.model = DistilBertForSequenceClassification.from_pretrained(
            model_path, return_dict=True
        )

    def _get_pc_uncertainty(self, presenting_complaint):
        """
        """
        if presenting_complaint in self.pc_uncertainties:
            return self.pc_uncertainties[presenting_complaint]
        return 1.5

    def predict(self, triage_request: TriageRequest) -> Tuple[float, float, list]:
        """
        Returns
            - triage_code: float
            - model_code: float
            - prediction_distribution: list
        """
        sequence = generate_stan_sequence(triage_request)
        if self.debug_mode:
            print('\nConstructed sequence:\n{}\n'.format(sequence))

        tokens = self.tokenizer(
            sequence, truncation=True, padding='max_length', return_tensors='pt'
        )
        output = self.model(**tokens)
        triage_code = output['logits'].item()      # one element in tensor
        return triage_code

    def get_triage_distribution(
        self, model_code: int, min_urgency: int, presenting_complaint: str
    ) -> Tuple[float, float, list]:
        """
        """
        triage_code = min(model_code, min_urgency)
        std_dev = self._get_pc_uncertainty(presenting_complaint)
        pred_dist = IStanModel.gen_pred_dist(
            triage_code, std_dev, min_urgency=min_urgency)
        return triage_code, model_code, pred_dist

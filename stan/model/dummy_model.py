"""
"""


import random

import numpy as np

from ..core.triage_request import TriageRequest
from .i_stan_model import IStanModel



class DummyModel(IStanModel):
    def __init__(self):
        pass

    def predict(self, triage_request: TriageRequest) -> tuple:
        """
        Returns
            - triage_code: int/float
            - prediction_distribution: list
        """
        assert type(triage_request) == TriageRequest
        triage_code, prediction_distribution = self._generate_dummies()
        return triage_code, prediction_distribution

    def _generate_dummies(self):
        triage_code = random.uniform(1.1, 4.9)
        min_urgency = 5
        cpc_std_dev = random.uniform(0.15, 1)
        prediction_distribution = np.random.normal(triage_code, cpc_std_dev, 7000)

        prediction_distribution = prediction_distribution[(prediction_distribution >= 0.8) &\
            (prediction_distribution <= (min_urgency+0.2))]
        
        prediction_distribution = prediction_distribution.tolist()

        return triage_code, prediction_distribution




"""
"""

from abc import ABC, abstractmethod
import json
from pathlib import Path
from typing import Tuple

import numpy as np

from ..core.triage_request import TriageRequest

class IStanModel(ABC):
    @abstractmethod
    def predict(self, triage_request: TriageRequest, min_urgency: int) -> Tuple[float, float, list]:
        """
        Returns
            - triage_code: float
            - model_code: float
            - prediction_distribution: list
        """
        pass

    def _init_pc_uncertainty(self, path_to_uncertainty):
        with Path(path_to_uncertainty).open() as json_file:
            self.pc_uncertainties = json.load(json_file)

    @staticmethod
    def gen_pred_dist(
        triage_code: float, 
        pc_uncertainty: float, 
        pred_count: int = 7000,
        max_urgency: int = 1,
        min_urgency: int = 5
        ) -> list:
        pred_dist = np.random.normal(triage_code, pc_uncertainty, pred_count)
        pred_dist = pred_dist[(max_urgency <= pred_dist) & (pred_dist <= min_urgency)]
        pred_dist = pred_dist.tolist()
        return pred_dist



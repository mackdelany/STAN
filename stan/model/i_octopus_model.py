"""
"""

from abc import ABC, abstractmethod
from typing import Tuple

from ..core.triage_request import TriageRequest


class IOctopusModel(ABC):
    @abstractmethod
    def triage(self, triage_request: TriageRequest) -> Tuple[float, float, list]:
        """
        Returns
            - triage_code: float
            - model_code: float
            - prediction_distribution: list
        """
        pass
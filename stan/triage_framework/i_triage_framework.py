from abc import ABC, abstractmethod
from typing import Tuple

from ..core.triage_request import TriageRequest
from ..core.triage_rules import get_triage_rules_template

class ITriageFramework(ABC):
    @abstractmethod
    def review_request(self, triage_request: TriageRequest) -> Tuple[dict, int]:
        """
        Reviews triage request with given triage framework.

        Returns:
            - triage_rules: dictionary of triage rules for each triage code
            - min_urgency: the minimal triage code the triage framework insists for 
            the given presentation.
        """
        pass
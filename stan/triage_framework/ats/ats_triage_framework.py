
"""
"""

from typing import Tuple

from .ats_abcd_assessment import ats_abcd_assessment
from .ats_general_assessment import ats_general_assessment
from .ats_vital_signs import ats_vital_signs
from ...core.triage_request import TriageRequest
from ...core.triage_rules import combine_triage_rule_dicts
from ..i_triage_framework import ITriageFramework


class ATSTriageFramework(ITriageFramework):
    def __init__(self, adult_age: int = 17):
        """
        Args:
            - adult_age: adult age prescribed by the triage framework in years.
        """
        self.adult_age = 17

    def review_request(self, triage_request, min_urgency: int = 5) -> Tuple[dict, int]:
        """
        Returns:
            - triage_rules: dictionary of triage rules for each triage code
            - min_urgency: the minimal triage code the triage framework insists for 
            the given presentation.
        """
        # Vital signs
        vital_sign_rules, vital_sign_urgency = ats_vital_signs(triage_request, self.adult_age)

        # ABCD
        abcd_rules, abcd_urgency = ats_abcd_assessment(triage_request, self.adult_age)

        # Others...
        general_rules, general_urgency = ats_general_assessment(triage_request, self.adult_age)

        triage_rules = combine_triage_rule_dicts(
            vital_sign_rules,
            abcd_rules,
            general_rules,
        )
        min_urgency = min(min_urgency, vital_sign_urgency, abcd_urgency, general_urgency)

        return triage_rules, min_urgency


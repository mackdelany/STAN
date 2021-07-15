"""
"""


from typing import Tuple

from ..core.triage_request import TriageRequest
from .adult_ews import adult_ews
from .maternal_ews import maternal_ews
from .paed_0_3_months_ews import paed_0_3_months_ews
from .paed_4_11_months_ews import paed_4_11_months_ews
from .paed_1_4_years_ews import paed_1_4_years_ews
from .paed_5_11_years_ews import paed_5_11_years_ews
from .paed_12_years_adult_ews import paed_12_years_adult_ews


class EarlyWarningScore():
    def __init__(self, adult_age=17):
        """
        """
        self.adult_age = 17
        self.mews_presenting_complaints = [
            'Labour',
            'Postpartum complication',
            'Pregnancy problem'
            ]

    def calculate_ews(self, triage_request: TriageRequest) -> Tuple[str, int, str]:
        """
        """
        if triage_request.presenting_complaint in self.mews_presenting_complaints:  # maternal
            ews_type = 'MEWS'
            ews_est, ews_message = maternal_ews(triage_request)
        elif 0 <= triage_request.age_in_months <= 3:   # 0 - 3 months
            ews_type = 'PEWS'
            ews_est, ews_message = paed_0_3_months_ews(triage_request)
        elif 4 <= triage_request.age_in_months <= 11:   # 4 - 11 months
            ews_type = 'PEWS'
            ews_est, ews_message = paed_4_11_months_ews(triage_request)
        elif (1*12) <= triage_request.age_in_months < (5*12):   # 1 - 4 years
            ews_type = 'PEWS'
            ews_est, ews_message = paed_1_4_years_ews(triage_request)
        elif (5*12) <= triage_request.age_in_months < (12*12):   # 5 - 11 years
            ews_type = 'PEWS'
            ews_est, ews_message = paed_5_11_years_ews(triage_request)
        elif (12*12) <= triage_request.age_in_months < (12*self.adult_age):   # 12 years - adult
            ews_type = 'PEWS'
            ews_est, ews_message = paed_12_years_adult_ews(triage_request)
        elif (12*self.adult_age) <= triage_request.age_in_months:  # adults
            ews_type = 'EWS'
            ews_est, ews_message = adult_ews(triage_request)
        else :
            raise UnknownEarlyWarningScoreTypeError(
                triage_request.age_in_months, triage_request.presenting_complaint
                )
        return ews_type, ews_est, ews_message

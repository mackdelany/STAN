"""
"""

from collections import namedtuple
from datetime import datetime
from typing import List, Optional, Tuple

import torch


TriageRequestTuple = namedtuple(
    'TriageRequestTuple',
    [
        'event_id',             # required
        'method',
        'hospital',
        'dhb',
        'present_date_time',
        'present_date_time_local',
        'dob',
        'age_in_months',
        'gender',
        'presenting_complaint',
        'presenting_complaint_group',
        'triage_assessment',
        'nurse_triage_code',
        'vital_signs_pulse',            # vitals
        'respiratory_rate',
        'blood_pressure_systolic',
        'blood_pressure_diastolic',
        'temperature',
        'sats',
        'airway_altered',           # ABCD and friends
        'breathing_altered',
        'circulation_altered',
        'disability_gcs',
        'pain_scale',
        'neuro_altered',
        'mental_health_concerns',
        'immunocompromised',
        'airway_was_measured',      # measurements
        'breathing_was_measured',
        'circulation_was_measured',
        'disability_gcs_was_measured',
        'pain_was_measured',
        'neuro_was_measured',
        'vital_signs_pulse_was_measured',
        'respiratory_rate_was_measured',
        'blood_pressure_was_measured',
        'temperature_was_measured',
        'sats_was_measured',
        'mental_health_was_measured',
        'immunocompromised_was_measured',
    ]
)


def tr_dict_to_named_tuple(triage_request_dict: dict) -> TriageRequestTuple:
    """Converts a triage request dictionary into a TriageRequest namedtuple.

    Args:
        - triage_request_dict, dict to convert

    Returns:
        - triage_request, new TriageRequest namedtuple
    """
    triage_request_tuple = TriageRequestTuple(
        event_id=triage_request_dict['event_id'],
        method=triage_request_dict['method'],
        hospital=triage_request_dict['hospital'],
        dhb=triage_request_dict['dhb'],
        present_date_time=triage_request_dict['present_date_time'],
        present_date_time_local=triage_request_dict['present_date_time_local'],
        dob=triage_request_dict['dob'],
        age_in_months=triage_request_dict['age_in_months'],
        gender=triage_request_dict['gender'],
        presenting_complaint=triage_request_dict['presenting_complaint'],
        presenting_complaint_group=triage_request_dict['presenting_complaint_group'],
        triage_assessment=triage_request_dict['triage_assessment'],
        nurse_triage_code=triage_request_dict['nurse_triage_code'],
        vital_signs_pulse=triage_request_dict['vital_signs_pulse'],
        respiratory_rate=triage_request_dict['respiratory_rate'],
        blood_pressure_systolic=triage_request_dict['blood_pressure_systolic'],
        blood_pressure_diastolic=triage_request_dict['blood_pressure_diastolic'],
        temperature=triage_request_dict['temperature'],
        sats=triage_request_dict['sats'],
        airway_altered=triage_request_dict['airway_altered'],
        breathing_altered=triage_request_dict['breathing_altered'],
        circulation_altered=triage_request_dict['circulation_altered'],
        disability_gcs=triage_request_dict['disability_gcs'],
        pain_scale=triage_request_dict['pain_scale'],
        neuro_altered=triage_request_dict['neuro_altered'],
        mental_health_concerns=triage_request_dict['mental_health_concerns'],
        immunocompromised=triage_request_dict['immunocompromised'],
        vital_signs_pulse_was_measured=triage_request_dict['vital_signs_pulse_was_measured'],
        respiratory_rate_was_measured=triage_request_dict['respiratory_rate_was_measured'],
        blood_pressure_was_measured=triage_request_dict['blood_pressure_was_measured'],
        temperature_was_measured=triage_request_dict['temperature_was_measured'],
        sats_was_measured=triage_request_dict['sats_was_measured'],
        airway_was_measured=triage_request_dict['airway_was_measured'],
        breathing_was_measured=triage_request_dict['breathing_was_measured'],
        circulation_was_measured=triage_request_dict['circulation_was_measured'],
        disability_gcs_was_measured=triage_request_dict['disability_gcs_was_measured'],
        pain_was_measured=triage_request_dict['pain_was_measured'],
        neuro_was_measured=triage_request_dict['neuro_was_measured'],
        mental_health_was_measured=triage_request_dict['mental_health_was_measured'],
        immunocompromised_was_measured=triage_request_dict['immunocompromised_was_measured'],
    )
    return triage_request_tuple


class TriageRequest():
    """STAN triage event
    """

    def __init__(
        self,
        event_id: Optional[str] = None,
        method: Optional[str] = None,
        hospital: Optional[str] = None,
        dhb: Optional[str] = None,
        present_date_time: datetime = None,
        present_date_time_local: datetime = None,
        dob: str = None,
        age_in_months: int = None,
        gender: str = None,
        presenting_complaint: str = None,
        presenting_complaint_group: Optional[str] = None,
        triage_assessment: Optional[str] = None,
        nurse_triage_code: Optional[int] = None,
        vital_signs_pulse: Optional[int] = None,
        respiratory_rate: Optional[int] = None,
        blood_pressure_systolic: Optional[int] = None,
        blood_pressure_diastolic: Optional[int] = None,
        temperature: Optional[float] = None,
        sats: Optional[float] = None,
        airway_altered: Optional[bool] = None,
        breathing_altered: Optional[bool] = None,
        circulation_altered: Optional[bool] = None,
        disability_gcs: Optional[int] = None,
        pain_scale: Optional[int] = None,
        neuro_altered: Optional[bool] = None,
        mental_health_concerns: Optional[bool] = None,
        immunocompromised: Optional[bool] = None,
        airway_was_measured: Optional[bool] = None,
        breathing_was_measured: Optional[bool] = None,
        circulation_was_measured: Optional[bool] = None,
        disability_gcs_was_measured: Optional[bool] = None,
        pain_was_measured: Optional[bool] = None,
        neuro_was_measured: Optional[bool] = None,
        vital_signs_pulse_was_measured: Optional[bool] = None,
        respiratory_rate_was_measured: Optional[bool] = None,
        blood_pressure_was_measured: Optional[bool] = None,
        temperature_was_measured: Optional[bool] = None,
        sats_was_measured: Optional[bool] = None,
        mental_health_was_measured: Optional[bool] = None,
        immunocompromised_was_measured: Optional[bool] = None
    ) -> None:
        self.event_id = event_id
        self.method = method
        self.hospital = hospital
        self.dhb = dhb
        self.present_date_time = present_date_time
        self.present_date_time_local = present_date_time_local
        self.dob = dob
        self.age_in_months = age_in_months
        self.gender = gender
        self.presenting_complaint = presenting_complaint
        self.presenting_complaint_group = presenting_complaint_group
        self.triage_assessment = triage_assessment
        self.nurse_triage_code = nurse_triage_code
        self.vital_signs_pulse = vital_signs_pulse
        self.respiratory_rate = respiratory_rate
        self.blood_pressure_systolic = blood_pressure_systolic
        self.blood_pressure_diastolic = blood_pressure_diastolic
        self.temperature = temperature
        self.sats = sats
        self.airway_altered = airway_altered
        self.breathing_altered = breathing_altered
        self.circulation_altered = circulation_altered
        self.disability_gcs = disability_gcs
        self.pain_scale = pain_scale
        self.neuro_altered = neuro_altered
        self.mental_health_concerns = mental_health_concerns
        self.immunocompromised = immunocompromised
        self.airway_was_measured = airway_was_measured
        self.breathing_was_measured = breathing_was_measured
        self.circulation_was_measured = circulation_was_measured
        self.disability_gcs_was_measured = disability_gcs_was_measured
        self.pain_was_measured = pain_was_measured
        self.neuro_was_measured = neuro_was_measured
        self.vital_signs_pulse_was_measured = vital_signs_pulse_was_measured
        self.respiratory_rate_was_measured = respiratory_rate_was_measured
        self.blood_pressure_was_measured = blood_pressure_was_measured
        self.temperature_was_measured = temperature_was_measured
        self.sats_was_measured = sats_was_measured
        self.mental_health_was_measured = mental_health_was_measured
        self.immunocompromised_was_measured = immunocompromised_was_measured
        self.tc_probs = None

    def set_tc_probs(self, tc_probs: torch.Tensor):
        self.tc_probs = tc_probs

    def review_airway_prediction(self, airway_was_altered_pred: bool):
        if not self.airway_was_measured:
            self.airway_altered = airway_was_altered_pred

    def review_breathing_prediction(self, breathing_was_altered_pred: bool):
        if not self.breathing_was_measured:
            self.breathing_altered = breathing_was_altered_pred

    def review_circulation_prediction(self, circulation_was_altered_pred: bool):
        if not self.circulation_was_measured:
            self.circulation_altered = circulation_was_altered_pred

    def review_disability_prediction(self, disability_was_altered_pred: bool):
        # TODO review this..
        if not self.disability_gcs_was_measured:
            if disability_was_altered_pred:
                self.disability_gcs = 12
            else:
                self.disability_gcs = 15

    def review_neuro_prediction(self, neuro_was_altered_pred: bool):
        if not self.neuro_was_measured:
            self.neuro_was_measured = neuro_was_altered_pred

    def review_immuno_prediction(self, immunocompromised_pred: bool):
        if not self.immunocompromised_was_measured:
            self.immunocompromised = immunocompromised_pred

    def review_mh_prediction(self, mh_concerns_pred: bool):
        if not self.mental_health_was_measured:
            self.mental_health_was_measured = mh_concerns_pred

    def review_outcome_prediction(self, outcomes: dict):
        self.sepsis_prediction = outcomes['sepsis_pred']

    def get_triage_distribution(
        self, min_urgency: int, dist_size: int = 1500
    ) -> Tuple[int, int, List[int]]:
        # TODO write test for code below..
        model_code = self.tc_probs.argmax().item() + 1   # 0-4 vs 1-5
        if min_urgency < 5:
            self.tc_probs[min_urgency:] = 0
            self.tc_probs = self.tc_probs * (1 / sum(self.tc_probs))
        stan_code = self.tc_probs.argmax().item() + 1   # may have changed

        pred_dist = []
        pred_dist_count = dist_size * self.tc_probs
        for i, count in enumerate(pred_dist_count):
            tc = i + 1                                   # 0-4 vs 1-5
            pred_dist += [tc] * int(count.item())
            pred_dist += [tc-0.01] * int(count.item())   #

        return stan_code, model_code, pred_dist

    def get_triage_event_dict(self) -> dict:
        """Returns dictionary of parameters
        """
        # HACK --> unhack now...
        triage_event_dict = {
            'event_id': self.event_id,
            'method': self.method,
            'hospital': self.hospital,
            'dhb': self.dhb,
            'present_date_time': self.present_date_time,
            'present_date_time_local': self.present_date_time_local,
            'dob': self.dob,
            'age_in_months': self.age_in_months,
            'gender': self.gender,
            'presenting_complaint': self.presenting_complaint,
            'presenting_complaint_group': self.presenting_complaint_group,
            'triage_assessment': self.triage_assessment,
            'nurse_triage_code': self.nurse_triage_code,
            'vital_signs_pulse': self.vital_signs_pulse,
            'respiratory_rate': self.respiratory_rate,
            'blood_pressure_systolic': self.blood_pressure_systolic,
            'blood_pressure_diastolic': self.blood_pressure_diastolic,
            'temperature': self.temperature,
            'sats': self.sats,
            'airway_altered': self.airway_altered,
            'breathing_altered': self.breathing_altered,
            'circulation_altered': self.circulation_altered,
            'disability_gcs': self.disability_gcs,
            'pain_scale': self.pain_scale,
            'neuro_altered': self.neuro_altered,
            'mental_health_concerns': self.mental_health_concerns,
            'immunocompromised': self.immunocompromised,
            'airway_was_measured': self.airway_was_measured,
            'breathing_was_measured': self.breathing_was_measured,
            'circulation_was_measured': self.circulation_was_measured,
            'disability_gcs_was_measured': self.disability_gcs_was_measured,
            'pain_was_measured': self.pain_was_measured,
            'neuro_was_measured': self.neuro_was_measured,
            'vital_signs_pulse_was_measured': self.vital_signs_pulse_was_measured,
            'respiratory_rate_was_measured': self.respiratory_rate_was_measured,
            'blood_pressure_was_measured': self.blood_pressure_was_measured,
            'temperature_was_measured': self.temperature_was_measured,
            'sats_was_measured': self.sats_was_measured,
            'mental_health_was_measured': self.mental_health_was_measured,
            'immunocompromised_was_measured': self.immunocompromised_was_measured,
        }
        return triage_event_dict

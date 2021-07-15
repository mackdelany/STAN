"""
"""

from typing import Tuple

from ..core.triage_request import TriageRequest


def paed_1_4_years_ews(triage_request: TriageRequest) -> str:
    """
    """
    pews, critical = calculate_paed_1_4_years_ews(triage_request)
    pews_message = gen_pews_1_4_years_message(triage_request, pews, critical)
    return pews, pews_message

def calculate_paed_1_4_years_ews(triage_request: TriageRequest) -> Tuple[int, bool]:
    """
    """
    rr_ews, rr_critical = paed_1_4_years_rr_ews(triage_request.respiratory_rate)
    resp_ews = paed_1_4_years_resp_ews(triage_request.airway_altered, triage_request.breathing_altered)
    sats_ews = paed_1_4_years_sats_ews(triage_request.sats)
    pulse_ews, pulse_critical = paed_1_4_years_pulse_ews(triage_request.vital_signs_pulse)
    bp_sys_ews, bp_sys_critical = paed_1_4_years_bp_sys_ews(triage_request.blood_pressure_systolic)
    loc_ews, loc_critical = paed_1_4_years_loc_ews(triage_request.disability_gcs)
    pews = rr_ews + resp_ews + sats_ews + pulse_ews + bp_sys_ews + loc_ews
    critical = any((rr_critical, pulse_critical, bp_sys_critical, loc_critical))
    return pews, critical

def gen_pews_1_4_years_message(triage_request: TriageRequest, pews: int, critical: bool) -> str:
    """
    """
    if critical:
        return 'Estimated PEWS Score: 10+'

    measurements = (
        #TODO
        triage_request.respiratory_rate_was_measured +
        triage_request.sats_was_measured +
        triage_request.vital_signs_pulse_was_measured +
        triage_request.blood_pressure_was_measured +
        triage_request.disability_gcs_was_measured
        )

    if measurements == 5:
        return 'Estimated PEWS Score: {}'.format(pews)
    elif 2 <= measurements < 5:
        message = 'Estimated PEWS Score: {}. Add '.format(pews)
        if not triage_request.respiratory_rate_was_measured:
            message += 'RR, '
        if not triage_request.sats_was_measured:
            message += 'sats, '
        if not triage_request.vital_signs_pulse_was_measured:
            message += 'pulse, '
        if not triage_request.blood_pressure_was_measured:
            message += 'bp, '
        if not triage_request.disability_gcs_was_measured:
            message += 'loc, '
        message += 'for better estimate.'
        return message
    elif measurements <= 1:
        return 'Not enough data for PEWS estimate'
    else:
        #TODO add error here?
        pass

def paed_1_4_years_rr_ews(respiratory_rate: int) -> Tuple[int, bool]:
    """
    """
    rr_ews = 0
    rr_critical = False
    if respiratory_rate:
        if 15 <= respiratory_rate < 35:
            rr_ews = 0
        elif 35 <= respiratory_rate < 40:
            rr_ews = 1
        elif 40 <= respiratory_rate < 50:
            rr_ews = 2
        elif 10 <= respiratory_rate < 15:
            rr_ews = 2
        elif 50 <= respiratory_rate:
            rr_ews = 3
        elif 5 < respiratory_rate <= 10:
            rr_ews = 3
        elif respiratory_rate <= 5:
            rr_ews = 10
            rr_critical = True
    return rr_ews, rr_critical

def paed_1_4_years_resp_ews(airway_altered: str, breathing_altered: str) -> int:
    """
    """
    resp_ews = 0
    if airway_altered:
        resp_ews = 3
    elif breathing_altered:
        resp_ews = 2
    return resp_ews

def paed_1_4_years_sats_ews(sats: float) -> int:
    """
    """
    sats_ews = 0
    if sats:
        if 93 <= sats:
            sats_ews = 0
        elif 89 <= sats < 93:
            sats_ews = 1
        elif 85 <= sats < 89:
            sats_ews = 2
        elif sats < 85:
            sats_ews = 3
    return sats_ews

def paed_1_4_years_pulse_ews(vital_signs_pulse: int) -> Tuple[int, bool]:
    """
    """
    pulse_ews = 0
    pulse_critical = False
    if vital_signs_pulse:
        if 90 <= vital_signs_pulse < 140:
            pulse_ews = 0
        elif 140 <= vital_signs_pulse < 160:
            pulse_ews = 1
        elif 80 <= vital_signs_pulse < 90:
            pulse_ews = 1
        elif 160 <= vital_signs_pulse < 170:
            pulse_ews = 2
        elif 70 <= vital_signs_pulse <= 80:
            pulse_ews = 2
        elif 60 <= vital_signs_pulse <= 70:
            pulse_ews = 3
        elif 170 <= vital_signs_pulse:
            pulse_ews = 3
        elif vital_signs_pulse < 60:
            pulse_ews = 10
            pulse_critical = True
    return pulse_ews, pulse_critical

def paed_1_4_years_bp_sys_ews(bp_sys: int) -> Tuple[int, bool]:
    """
    """
    bp_sys_ews = 0
    bp_sys_critical = False
    if bp_sys_ews:
        if 80 <= bp_sys <= 120:
            bp_sys_ews = 0
        elif 70 <= bp_sys <= 80:
            bp_sys_ews = 1
        elif 65 <= bp_sys <= 70:
            bp_sys_ews = 2
        elif 120 <= bp_sys:
            bp_sys_ews = 2
        elif 55 < bp_sys <= 65:
            bp_sys_ews = 3
        elif bp_sys <= 55:
            bp_sys_ews = 10
            bp_sys_critical = True
    return bp_sys_ews, bp_sys_critical

def paed_1_4_years_loc_ews(disability_gcs: str) -> int:
    """
    """
    loc_ews = 0
    loc_critical = False
    if disability_gcs:
        if disability_gcs >= 14:
            loc_ews = 0
        if 14 > disability_gcs >= 11:
            loc_ews = 1
        if 11 > disability_gcs >= 9:
            loc_ews = 3
        if 9 > disability_gcs:
            loc_ews = 10
            loc_critical = True
        else:
            #TODO add error here ?
            pass
    return loc_ews, loc_critical

"""
"""

from typing import Tuple

from stan.core.triage_request import TriageRequest


def adult_ews(triage_request: TriageRequest) -> str:
    """Calculates early warning score and message for an adult.

    Args:
        - triage_request, TriageRequest object for the presentation
    """
    ews, critical = calculate_adult_ews(triage_request)
    ews_message = adult_ews_message(triage_request, ews, critical)
    return ews, ews_message

def calculate_adult_ews(triage_request: TriageRequest) -> Tuple[int, bool]:
    """Calculates early warning score for an adult.

    Args:
        - triage_request, TriageRequest object for the presentation
    """
    rr_ews, rr_critical = adult_rr_ews(triage_request.respiratory_rate)
    sats_ews = adult_sats_ews(triage_request.sats)
    pulse_ews, pulse_critical = adult_pulse_ews(triage_request.vital_signs_pulse)
    bp_sys_ews, bp_sys_critical = adult_bp_sys_ews(triage_request.blood_pressure_systolic)
    temp_ews = adult_temp_ews(triage_request.temperature)
    loc_ews, loc_critical = adult_loc_ews(triage_request.disability_gcs)
    ews = rr_ews + sats_ews + pulse_ews + bp_sys_ews + temp_ews + loc_ews
    critical = any((rr_critical, pulse_critical, bp_sys_critical, loc_critical))
    return ews, critical

def adult_ews_message(triage_request: TriageRequest, ews: int, critical: bool) -> str:
    """Generates early warning score message for an adult.

    Args:
        - triage_request, TriageRequest object for the presentation
        - ews, early warning score the presentation
        - critical, whether the presentation is in a critical state
    """
    if critical:
        return 'Estimated EWS Score: {}'.format(ews)

    measurements = (
        #TODO
        triage_request.respiratory_rate_was_measured +
        triage_request.sats_was_measured +
        triage_request.vital_signs_pulse_was_measured +
        triage_request.blood_pressure_was_measured +
        triage_request.temperature_was_measured +
        triage_request.disability_gcs_was_measured
        )

    if measurements == 6:
        return 'Estimated EWS Score: {}'.format(ews)
    elif 3 <= measurements < 5:
        message = 'Estimated EWS Score: {}. Add '.format(ews)
        if not triage_request.respiratory_rate_was_measured:
            message += 'RR, '
        if not triage_request.sats_was_measured:
            message += 'sats, '
        if not triage_request.vital_signs_pulse_was_measured:
            message += 'pulse, '
        if not triage_request.blood_pressure_was_measured:
            message += 'bp, '
        if not triage_request.temperature_was_measured:
            message += 'temp, '
        if not triage_request.disability_gcs_was_measured:
            message += 'loc, '
        message += 'for better estimate.'
        return message
    elif measurements <= 3:
        return 'Not enough data for EWS estimate'
    else:
        #TODO add error here?
        pass

def adult_rr_ews(respiratory_rate: int) -> Tuple[int, bool]:
    """
    """
    rr_ews = 0
    rr_critical = False
    if respiratory_rate:
        if 12 <= respiratory_rate <= 20:
            rr_ews = 0
        elif 9 <= respiratory_rate < 12:
            rr_ews = 1
        elif 20 < respiratory_rate <= 24:
            rr_ews = 2
        elif 24 < respiratory_rate <= 35:
            rr_ews = 3
        elif 5 <= respiratory_rate < 9:
            rr_ews = 3
        elif 35 < respiratory_rate:
            rr_ews = 10
            rr_critical = True
        elif respiratory_rate < 5:
            rr_ews = 10
            rr_critical = True
    return rr_ews, rr_critical

def adult_sats_ews(sats: float) -> int:
    """Calculates sats ews score for an adult.

    Args: 
        - sats, the presentations oxygen saturation

    Returns:
        - sats_ews, the presentations ews score for sats
    """
    sats_ews = 0
    if sats:
        if 96 <= sats:
            sats_ews = 0
        elif 94 <= sats < 96:
            sats_ews = 1
        elif 91 < sats < 94:
            sats_ews = 2
        elif sats <= 91:
            sats_ews = 3
    return sats_ews

def adult_pulse_ews(vital_signs_pulse: int) -> Tuple[int, bool]:
    """Calculates pulse ews score for an adult.

    Args: 
        - vital_signs_pulse, the presentations heart rate

    Returns:
        - pulse_ews, the presentations ews score for pulse
        - pulse_critical, whether the presentation has a critical pulse
    """
    pulse_ews = 0
    pulse_critical = False
    if vital_signs_pulse:
        if 50 <= vital_signs_pulse < 90:
            pulse_ews = 0
        elif 90 <= vital_signs_pulse < 110:
            pulse_ews = 1
        elif 40 <= vital_signs_pulse < 50:
            pulse_ews = 2
        elif 110 <= vital_signs_pulse < 130:
            pulse_ews = 2
        elif vital_signs_pulse <= 50:
            pulse_ews = 3
        elif 130 <= vital_signs_pulse < 140:
            pulse_ews = 3
        elif 140 <= vital_signs_pulse:
            pulse_ews = 10
            pulse_critical = True
        elif vital_signs_pulse < 40:
            pulse_ews = 10
            pulse_critical = True
    return pulse_ews, pulse_critical

def adult_bp_sys_ews(bp_sys: int) -> Tuple[int, bool]:
    """
    """
    bp_sys_ews = 0
    bp_sys_critical = False
    if bp_sys:
        if 110 <= bp_sys < 220:
            bp_sys_ews = 0
        elif 100 <= bp_sys <= 110:
            bp_sys_ews = 1
        elif 90 <= bp_sys <= 100:
            bp_sys_ews = 2
        elif 220 <= bp_sys:
            bp_sys_ews = 2
        elif 70 <= bp_sys <= 90:
            bp_sys_ews = 3
        elif bp_sys < 70:
            bp_sys_ews = 10
            bp_sys_critical = True
    return bp_sys_ews, bp_sys_critical

def adult_temp_ews(temp: float) -> int:
    """
    """
    temp_ews = 0
    if temp:
        if 36 <= temp < 38:
            temp_ews = 0
        elif 35 <= temp < 36:
            temp_ews = 1
        elif 38 <= temp < 39:
            temp_ews = 1
        elif temp < 35:
            temp_ews = 2
        elif 39 <= temp:
            temp_ews = 2
    return temp_ews

def adult_loc_ews(disability_gcs: str) -> int:
    """
    """
    loc_ews = 0
    loc_critical = False
    if disability_gcs:
        if disability_gcs >= 14:
            loc_ews = 0
        if 14 > disability_gcs >= 11:
            loc_ews = 3
        if 11 > disability_gcs >= 9:
            loc_ews = 3
        if 9 > disability_gcs:
            loc_ews = 10
            loc_critical = True
        else:
            #TODO add error here ?
            pass
    return loc_ews, loc_critical

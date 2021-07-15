"""
"""

from typing import Tuple

from ..core.triage_request import TriageRequest


def maternal_ews(triage_request: TriageRequest) -> str:
    """
    """
    mews, critical = calculate_maternal_ews(triage_request)
    mews_message = gen_mews_message(triage_request, mews, critical)
    return mews, mews_message

def calculate_maternal_ews(triage_request: TriageRequest) -> Tuple[int, bool]:
    """
    """
    rr_ews, rr_critical = maternal_rr_ews(triage_request.respiratory_rate)
    sats_ews = maternal_sats_ews(triage_request.sats)
    pulse_ews, pulse_critical = maternal_pulse_ews(triage_request.vital_signs_pulse)
    bp_sys_ews, bp_sys_critical = maternal_bp_sys_ews(triage_request.blood_pressure_systolic)
    bp_dia_ews = maternal_bp_dia_ews(triage_request.blood_pressure_diastolic)
    temp_ews = maternal_temp_ews(triage_request.temperature)
    loc_ews = maternal_loc_ews(triage_request.disability_gcs)
    mews = rr_ews + sats_ews + pulse_ews + bp_sys_ews + bp_dia_ews + temp_ews + loc_ews
    critical = any((rr_critical, pulse_critical, bp_sys_critical))
    return mews, critical

def gen_mews_message(triage_request: TriageRequest, mews: int, critical: bool) -> str:
    """
    """
    if critical:
        return 'Estimated MEWS Score: 10+'

    measurements = (
        triage_request.respiratory_rate_was_measured +
        triage_request.sats_was_measured +
        triage_request.vital_signs_pulse_was_measured +
        triage_request.blood_pressure_was_measured +
        triage_request.temperature_was_measured +
        triage_request.disability_gcs_was_measured
        )

    if measurements == 6:
        return 'Estimated MEWS Score: {}'.format(mews)
    elif 3 <= measurements < 6:
        message = 'Estimated MEWS Score: {}. Add '.format(mews)
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
    elif measurements <= 2:
        return 'Not enough data for MEWS estimate'
    else:
        #TODO add error here?
        pass

def maternal_rr_ews(respiratory_rate: int) -> Tuple[int, bool]:
    """
    """
    rr_ews = 0
    rr_critical = False
    if respiratory_rate:
        if 10 <= respiratory_rate <= 20:
            rr_ews = 0
        elif 21 <= respiratory_rate <= 25:
            rr_ews = 2
        elif 26 <= respiratory_rate <= 30:
            rr_ews = 3
        elif 6 <= respiratory_rate <= 9:
            rr_ews = 3
        elif 31 <= respiratory_rate:
            rr_ews = 10
            rr_critical = True
        elif respiratory_rate <= 5:
            rr_ews = 10
            rr_critical = True
    return rr_ews, rr_critical

def maternal_sats_ews(sats: float) -> int:
    """
    """
    sats_ews = 0
    if sats:
        if 95 <= sats:
            sats_ews = 0
        elif 92 <= sats < 95:
            sats_ews = 2
        elif sats < 92:
            sats_ews = 3
    return sats_ews

def maternal_pulse_ews(vital_signs_pulse: int) -> Tuple[int, bool]:
    """
    """
    pulse_ews = 0
    pulse_critical = False
    if vital_signs_pulse:
        if 60 <= vital_signs_pulse <= 99:
            pulse_ews = 0
        elif 100 <= vital_signs_pulse <= 119:
            pulse_ews = 1
        elif 50 <= vital_signs_pulse <= 59:
            pulse_ews = 1
        elif 120 <= vital_signs_pulse <= 129:
            pulse_ews = 2
        elif 40 <= vital_signs_pulse <= 49:
            pulse_ews = 3
        elif 130 <= vital_signs_pulse <= 139:
            pulse_ews = 3
        elif 140 <= vital_signs_pulse:
            pulse_ews = 10
            pulse_critical = True
        elif vital_signs_pulse < 40:
            pulse_ews = 10
            pulse_critical = True
    return pulse_ews, pulse_critical

def maternal_bp_sys_ews(bp_sys: int) -> Tuple[int, bool]:
    """
    """
    bp_sys_ews = 0
    bp_sys_critical = False
    if bp_sys_ews:
        if 100 <= bp_sys <= 139:
            bp_sys_ews = 0
        elif 90 <= bp_sys <= 99:
            bp_sys_ews = 1
        elif 140 <= bp_sys <= 159:
            bp_sys_ews = 2
        elif 80 <= bp_sys <= 89:
            bp_sys_ews = 2
        elif 160 <= bp_sys <= 199:
            bp_sys_ews = 3
        elif 70 <= bp_sys <= 79:
            bp_sys_ews = 3
        elif 200 <= bp_sys:
            bp_sys_ews = 10
            bp_sys_critical = True
        elif bp_sys <= 69:
            bp_sys_ews = 10
            bp_sys_critical = True
    return bp_sys_ews, bp_sys_critical

def maternal_bp_dia_ews(bp_dia: int) -> int:
    """
    """
    bp_dia_ews = 0
    if bp_dia:
        if bp_dia < 90:
            bp_dia_ews = 0
        elif 90 < bp_dia < 110:
            bp_dia_ews = 2
        elif 110 < bp_dia:
            bp_dia_ews = 3
    return bp_dia_ews

def maternal_temp_ews(temp: float) -> int:
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
            temp_ews = 3
        elif 39 <= temp:
            temp_ews = 3
    return temp_ews

def maternal_loc_ews(disability_gcs: str) -> int:
    """
    """
    loc_ews = 0
    if disability_gcs:
        if disability_gcs >= 14:
            loc_ews = 0
        elif disability_gcs < 14:
            loc_ews = 3
        else:
            #TODO add error here ?
            pass
    return loc_ews
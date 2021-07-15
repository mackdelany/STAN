
from typing import Tuple

from ...core.triage_request import TriageRequest
from ...core.triage_rules import get_triage_rules_template


def ats_vital_signs(triage_request: TriageRequest, adult_age: int = 17) -> Tuple[dict, int]:
    """
    Assesses a triage presentations' vital signs as per the Australiasian Triage Scale.

    Returns:
        - triage_rules: dictionary of triage rules for each triage code wrt to 
        ats vital sign guidelines
        - min_urgency: the minimal triage code the triage framework insists for 
        the given presentation wrt to ats vital sign guidelines
    """
    if 0 <= triage_request.age_in_months <= 3:   # 0 - 3 months
        vital_rules, vital_urgency = ats_paediatric_vital_signs_0_3_months(triage_request)
    elif 4 <= triage_request.age_in_months <= 11:   # 4 - 11 months
        vital_rules, vital_urgency = ats_paediatric_vital_signs_4_11_months(triage_request)
    elif (1*12) <= triage_request.age_in_months < (5*12):   # 1 - 4 years
        vital_rules, vital_urgency = ats_paediatric_vital_signs_1_4_years(triage_request)
    elif (5*12) <= triage_request.age_in_months < (12*12):   # 5 - 11 years
        vital_rules, vital_urgency = ats_paediatric_vital_signs_5_11_years(triage_request)
    elif (12*12) <= triage_request.age_in_months < (12*adult_age):   # 12 years - adult
        vital_rules, vital_urgency = ats_paediatric_vital_signs_12_years_adult(triage_request)
    elif (12*adult_age) <= triage_request.age_in_months:  # adults
        vital_rules, vital_urgency = ats_adult_vital_signs(triage_request)
    else :
        pass
        #TODO add relevant exception here
    return vital_rules, vital_urgency


def ats_paediatric_vital_signs_0_3_months(
    triage_request: TriageRequest, 
    min_urgency: int = 5
    ) -> Tuple[dict, int]:
    """
    Assesses a 0-3 month year old triage presentations' vital signs as per 
    the Australiasian Triage Scale. 

    Returns:
        - triage_rules: dictionary of triage rules for each triage code wrt to 
        ats vital sign guidelines
        - min_urgency: the minimal triage code the triage framework guides for 
        the given presentation wrt to ats vital sign guidelines
    """
    vital_urgency = 5
    vital_rules = get_triage_rules_template()
    
    # respiratory_rate
    if triage_request.respiratory_rate:
        if triage_request.respiratory_rate <= 15:
            vital_urgency = min(vital_urgency, 1)
            vital_rules['Code1'].append(
                'Low Respiratory Rate for 0-3 month old: {}/min'.format(triage_request.respiratory_rate)
                )
        elif triage_request.respiratory_rate >= 80:
            vital_urgency = min(vital_urgency, 1)
            vital_rules['Code1'].append(
                'High Respiratory Rate for 0-3 month old: {}/min'.format(triage_request.respiratory_rate)
                )
        elif 15 <= triage_request.respiratory_rate <= 20:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'Low Respiratory Rate for 0-3 month old: {}/min'.format(triage_request.respiratory_rate)
                )
        elif 70 <= triage_request.respiratory_rate <= 80:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'High Respiratory Rate for 0-3 month old: {}/min'.format(triage_request.respiratory_rate)
                )

    # pulse
    if triage_request.vital_signs_pulse:
        if triage_request.vital_signs_pulse <= 60:
            vital_urgency = min(vital_urgency, 1)
            vital_rules['Code1'].append(
                'Low Heart Rate for 0-3 month old: {} bpm'.format(triage_request.vital_signs_pulse)
                )
        elif triage_request.vital_signs_pulse >= 190:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'High Heart Rate for 0-3 month old: {} bpm'.format(triage_request.vital_signs_pulse)
                )

    # bp systolic
    if triage_request.blood_pressure_systolic:
        if triage_request.blood_pressure_systolic <= 50:
            vital_urgency = min(vital_urgency, 1)
            vital_rules['Code1'].append(
                'Low systolic blood pressure for 0-3 month old: {} mmHg'.format(triage_request.blood_pressure_systolic)
                )
        elif 50 < triage_request.blood_pressure_systolic <= 55:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'Low systolic blood pressure for 0-3 month old: {} mmHg'.format(triage_request.blood_pressure_systolic)
                )

    return vital_rules, vital_urgency

def ats_paediatric_vital_signs_4_11_months(
    triage_request: TriageRequest, 
    min_urgency: int = 5
    ) -> Tuple[dict, int]:
    """
    Assesses a 4-11 month year old triage presentations' vital signs as per 
    the Australiasian Triage Scale.

    Returns:
        - triage_rules: dictionary of triage rules for each triage code wrt to 
        ats vital sign guidelines
        - min_urgency: the minimal triage code the triage framework insists for 
        the given presentation wrt to ats vital sign guidelines
    """
    vital_urgency = 5
    vital_rules = get_triage_rules_template()
    
    # respiratory_rate
    if triage_request.respiratory_rate:
        if triage_request.respiratory_rate <= 10:
            vital_urgency = min(vital_urgency, 1)
            vital_rules['Code1'].append(
                'Low Respiratory Rate for 4-11 month old: {}/min'.format(triage_request.respiratory_rate)
                )
        elif triage_request.respiratory_rate >= 55:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'High Respiratory Rate for 4-11 month old: {}/min'.format(triage_request.respiratory_rate)
                )
        elif 10 <= triage_request.respiratory_rate <= 15:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'Low Respiratory Rate for 4-11 month old: {}/min'.format(triage_request.respiratory_rate)
                )

    # pulse
    if triage_request.vital_signs_pulse:
        if triage_request.vital_signs_pulse <= 60:
            vital_urgency = min(vital_urgency, 1)
            vital_rules['Code1'].append(
                'Low Heart Rate for 4-11 month old: {} bpm'.format(triage_request.vital_signs_pulse)
                )
        elif triage_request.vital_signs_pulse >= 190:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'High Heart Rate for 4-11 month old: {} bpm'.format(triage_request.vital_signs_pulse)
                )
        elif 60 < triage_request.vital_signs_pulse < 80:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'Low Heart Rate for 4-11 month old: {} bpm'.format(triage_request.vital_signs_pulse)
                )

    # bp systolic
    if triage_request.blood_pressure_systolic:
        if triage_request.blood_pressure_systolic <= 50:
            vital_urgency = min(vital_urgency, 1)
            vital_rules['Code1'].append(
                'Low systolic blood pressure for 4-11 month old: {} mmHg'.format(triage_request.blood_pressure_systolic)
                )
        elif 50 < triage_request.blood_pressure_systolic <= 55:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'Low systolic blood pressure for 4-11 month old: {} mmHg'.format(triage_request.blood_pressure_systolic)
                )

    return vital_rules, vital_urgency

def ats_paediatric_vital_signs_1_4_years(
    triage_request: TriageRequest, 
    min_urgency: int = 5
    ) -> Tuple[dict, int]:
    """
    Assesses a 1-4 year old triage presentations' vital signs as per 
    the Australiasian Triage Scale. 

    Returns:
        - triage_rules: dictionary of triage rules for each triage code wrt to 
        ats vital sign guidelines
        - min_urgency: the minimal triage code the triage framework insists for 
        the given presentation wrt to ats vital sign guidelines
    """
    vital_urgency = 5
    vital_rules = get_triage_rules_template()
    
    # respiratory_rate
    if triage_request.respiratory_rate:
        if triage_request.respiratory_rate <= 5:
            vital_urgency = min(vital_urgency, 1)
            vital_rules['Code1'].append(
                'Low Respiratory Rate for 1-4 year old: {}/min'.format(triage_request.respiratory_rate)
                )
        elif triage_request.respiratory_rate >= 50:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'High Respiratory Rate for 1-4 year old: {}/min'.format(triage_request.respiratory_rate)
                )
        elif 10 <= triage_request.respiratory_rate <= 10:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'Low Respiratory Rate for 1-4 year old: {}/min'.format(triage_request.respiratory_rate)
                )

    # pulse
    if triage_request.vital_signs_pulse:
        if triage_request.vital_signs_pulse <= 60:
            vital_urgency = min(vital_urgency, 1)
            vital_rules['Code1'].append(
                'Low Heart Rate for 1-4 year old: {} bpm'.format(triage_request.vital_signs_pulse)
                )
        elif triage_request.vital_signs_pulse >= 170:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'High Heart Rate for 1-4 year old: {} bpm'.format(triage_request.vital_signs_pulse)
                )
        elif 60 < triage_request.vital_signs_pulse < 70:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'Low Heart Rate for 1-4 year old: {} bpm'.format(triage_request.vital_signs_pulse)
                )

    # bp systolic
    if triage_request.blood_pressure_systolic:
        if triage_request.blood_pressure_systolic <= 55:
            vital_urgency = min(vital_urgency, 1)
            vital_rules['Code1'].append(
                'Low systolic blood pressure for 1-4 year old: {} mmHg'.format(triage_request.blood_pressure_systolic)
                )
        elif 50 < triage_request.blood_pressure_systolic <= 65:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'Low systolic blood pressure for 1-4 year old: {} mmHg'.format(triage_request.blood_pressure_systolic)
                )

    return vital_rules, vital_urgency

def ats_paediatric_vital_signs_5_11_years(
    triage_request: TriageRequest, 
    min_urgency: int = 5
    ) -> Tuple[dict, int]:
    """
    Assesses a 5-11 year old triage presentations' vital signs as per 
    the Australiasian Triage Scale.

    Returns:
        - triage_rules: dictionary of triage rules for each triage code wrt to 
        ats vital sign guidelines
        - min_urgency: the minimal triage code the triage framework insists for 
        the given presentation wrt to ats vital sign guidelines 
    """    
    vital_urgency = 5
    vital_rules = get_triage_rules_template()

    # respiratory_rate
    if triage_request.respiratory_rate:
        if triage_request.respiratory_rate <= 5:
            vital_urgency = min(vital_urgency, 1)
            vital_rules['Code1'].append(
                'Low Respiratory Rate for 5-11 year old: {}/min'.format(triage_request.respiratory_rate)
                )
        elif triage_request.respiratory_rate >= 45:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'High Respiratory Rate for 5-11 year old: {}/min'.format(triage_request.respiratory_rate)
                )

    # pulse
    if triage_request.vital_signs_pulse:
        if triage_request.vital_signs_pulse <= 60:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'Low Heart Rate for 5-11 year old: {} bpm'.format(triage_request.vital_signs_pulse)
                )
        elif triage_request.vital_signs_pulse >= 170:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'High Heart Rate for 5-11 year old: {} bpm'.format(triage_request.vital_signs_pulse)
                )

    # bp systolic
    if triage_request.blood_pressure_systolic:
        if triage_request.blood_pressure_systolic <= 55:
            vital_urgency = min(vital_urgency, 1)
            vital_rules['Code1'].append(
                'Low systolic blood pressure for 5-11 year old: {} mmHg'.format(triage_request.blood_pressure_systolic)
                )
        elif 50 < triage_request.blood_pressure_systolic <= 65:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'Low systolic blood pressure for 5-11 year old: {} mmHg'.format(triage_request.blood_pressure_systolic)
                )

    return vital_rules, vital_urgency

def ats_paediatric_vital_signs_12_years_adult(
    triage_request: TriageRequest, 
    min_urgency: int = 5
    ) -> Tuple[dict, int]:
    """
    Assesses a 12 year old - adult age triage presentations' vital signs 
    as per the Australiasian Triage Scale. 

    Returns:
        - triage_rules: dictionary of triage rules for each triage code wrt to 
        ats vital sign guidelines
        - min_urgency: the minimal triage code the triage framework insists for 
        the given presentation wrt to ats vital sign guidelines
    """
    vital_urgency = 5
    vital_rules = get_triage_rules_template()
    
    # respiratory_rate
    if triage_request.respiratory_rate:
        if triage_request.respiratory_rate <= 5:
            vital_urgency = min(vital_urgency, 1)
            vital_rules['Code1'].append(
                'Low Respiratory Rate for 5-11 year old: {}/min'.format(triage_request.respiratory_rate)
                )
        elif triage_request.respiratory_rate >= 35:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'High Respiratory Rate for 5-11 year old: {}/min'.format(triage_request.respiratory_rate)
                )

    # pulse
    if triage_request.vital_signs_pulse:
        if triage_request.vital_signs_pulse <= 50:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'Low Heart Rate for 5-11 year old: {} bpm'.format(triage_request.vital_signs_pulse)
                )
        elif triage_request.vital_signs_pulse >= 140:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'High Heart Rate for 5-11 year old: {} bpm'.format(triage_request.vital_signs_pulse)
                )

    # bp systolic
    if triage_request.blood_pressure_systolic:
        if triage_request.blood_pressure_systolic <= 70:
            vital_urgency = min(vital_urgency, 1)
            vital_rules['Code1'].append(
                'Low systolic blood pressure for 5-11 year old: {} mmHg'.format(triage_request.blood_pressure_systolic)
                )
        elif 50 < triage_request.blood_pressure_systolic <= 80:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'Low systolic blood pressure for 5-11 year old: {} mmHg'.format(triage_request.blood_pressure_systolic)
                )

    return vital_rules, vital_urgency

def ats_adult_vital_signs(
    triage_request: TriageRequest, 
    min_urgency: int = 5
    ) -> Tuple[dict, int]:
    """
    Assesses an adult triage presentations' vital signs as per the 
    Australiasian Triage Scale. 

    Returns:
        - triage_rules: dictionary of triage rules for each triage code wrt to 
        ats vital sign guidelines
        - min_urgency: the minimal triage code the triage framework insists for 
        the given presentation wrt to ats vital sign guidelines
    """
    vital_urgency = 5
    vital_rules = get_triage_rules_template()
    
    # respiratory_rate
    if triage_request.respiratory_rate:
        if triage_request.respiratory_rate <= 4:
            vital_urgency = min(vital_urgency, 1)
            vital_rules['Code1'].append(
                'Low Respiratory Rate: {}/min'.format(triage_request.respiratory_rate)
                )
        elif triage_request.respiratory_rate >= 36:
            vital_urgency = min(vital_urgency, 1)
            vital_rules['Code1'].append(
                'High Respiratory Rate: {}/min'.format(triage_request.respiratory_rate)
                )
        elif 5 <= triage_request.respiratory_rate <= 8:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'Low Respiratory Rate: {}/min'.format(triage_request.respiratory_rate)
                )

    # pulse
    if triage_request.vital_signs_pulse:
        if triage_request.vital_signs_pulse <= 40:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'Low Heart Rate: {} bpm'.format(triage_request.vital_signs_pulse)
                )
        elif triage_request.vital_signs_pulse >= 140:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'High Heart Rate: {} bpm'.format(triage_request.vital_signs_pulse)
                )

    # bp systolic
    if triage_request.blood_pressure_systolic:
        if triage_request.blood_pressure_systolic <= 80:
            vital_urgency = min(vital_urgency, 1)
            vital_rules['Code1'].append(
                'Low systolic blood pressure: {} mmHg'.format(triage_request.blood_pressure_systolic)
                )
        elif 80 < triage_request.blood_pressure_systolic <= 90:
            vital_urgency = min(vital_urgency, 2)
            vital_rules['Code2'].append(
                'Low systolic blood pressure: {} mmHg'.format(triage_request.blood_pressure_systolic)
                )
    
    return vital_rules, vital_urgency

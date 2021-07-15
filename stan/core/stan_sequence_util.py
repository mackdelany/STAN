"""
"""

from stan.core.triage_request import TriageRequest


def generate_stan_sequence(event: TriageRequest) -> str:
    """
    Create STAN sequence.

    Args:
        event: namedtuple with following fields:
            - present_date_time
            - dob
            - age_in_months
            - presenting_complaint
            - gender
            - airway_altered
            - breathing_altered
            - circulation_altered
            - disability_gcs
            - neuro_altered
            - pain_scale
            - vital_signs_pulse
            - respiratory_rate
            - blood_pressure_systolic
            - blood_pressure_diastolic
            - temperature
            - sats
            - mental_health_concerns
            - immunocompromised
            - triage_assessment
    """
    seq = ''
    seq = bucket_age(seq, event.age_in_months)
    seq = bucket_time(seq, event.present_date_time)
    seq = add_gender_to_seq(seq, event.gender)
    seq = add_complaint_to_seq(seq, event.presenting_complaint)
    seq = add_triage_abcd_to_seq(seq, event)
    seq = add_pain_to_seq(seq, event.pain_scale)
    seq = add_vital_signs_to_seq(seq, event)
    seq = add_immunospressed_to_seq(seq, event.immunocompromised)
    seq = add_mental_health_to_seq(seq, event.mental_health_concerns)
    seq = add_triage_assessment(seq, event.triage_assessment)
    return seq

def bucket_age(seq: str, age_in_months: int) -> str:
    """Categorizes presentation age into a cateogy.

    Args:
        - seq: sentence or set of sentences representing the presentation
        - age_in_months: the presentations age in months

    Returns:
        - seq: sentence or set of sentences representing the presentation
        with age accounted for
    """
    if age_in_months < 4:
        seq += 'Newborn'
    elif age_in_months >= 4 and age_in_months < 12:
        seq += 'Baby'
    elif age_in_months >= 12 and age_in_months < 48:
        seq += 'Kid'
    elif age_in_months >= 48 and age_in_months < 108:
        seq += 'Child'
    elif age_in_months >= 108 and age_in_months < 156:
        seq += 'Juvenile'
    elif age_in_months >= 156 and age_in_months < 204:
        seq += 'Teenager'
    elif age_in_months >= 204 and age_in_months < 300:
        seq += 'Young'
    elif age_in_months >= 300 and age_in_months < 540:
        seq += 'Adult'
    elif age_in_months >= 540 and age_in_months < 780:
        seq += 'Older'
    elif age_in_months >= 780 and age_in_months < 900:
        seq += 'Senior'
    elif age_in_months >= 900 and age_in_months < 1080:
        seq += 'Elderly'
    elif age_in_months >= 1080:
        seq += 'Ancient'
    return seq

def bucket_time(seq, present_date_time):
    """
    """
    return seq

def add_gender_to_seq(seq, gender):
    if gender == 'M':
        seq += ' male.'
    else :  ## Need to fix, but best to ignore edge cases for now
        seq += ' female.'
    return seq

def add_complaint_to_seq(seq, presenting_complaint):
    seq += ' {}.'.format(presenting_complaint)
    return seq

def add_triage_abcd_to_seq(seq, event):
    if event.airway_altered:
        seq += ' Affected airway.'
    if event.breathing_altered:
        seq += ' Distressed breathing.'
    if event.circulation_altered:
        seq += ' Altered circulation.'
    if event.disability_gcs:
        if 14 > event.disability_gcs >= 11:
            seq += ' Can verbalize.'
        elif 11 > event.disability_gcs >= 9:
            seq += ' Responds pain.'
        elif 9 > event.disability_gcs:
            seq += ' Is unconscious.'
    if event.neuro_altered:
        seq += ' Nerves impacted.'
    return seq

def add_vital_signs_to_seq(seq, event, adult_age=17):
    """
    From EWS framework:
        Vital sign in blue zone = critically high/low
        Vital sign in red zone = extremely high/low
        Vital sign in orange zone = very high/low
        Vital sign in yellow zone = high/low
    """
    if (event.age_in_months / 12) >= adult_age:
        seq = add_adult_vital_signs(seq, event)
    elif event.age_in_months <= 3:
        seq = add_paediatric_vital_signs_0_3_months(seq, event)
    elif 4 <= event.age_in_months <= 11:
        seq = add_paediatric_vital_signs_4_11_months(seq, event)
    elif 12 <= event.age_in_months < (5*12):
        seq = add_paediatric_vital_signs_1_4_years(seq, event)
    elif (5*12) <= event.age_in_months < (12*12):
        seq = add_paediatric_vital_signs_5_11_years(seq, event)
    else :
        seq = add_paediatric_vital_signs_12_years_adult(seq, event)
    return seq

def add_pain_to_seq(seq, pain_scale):
    if pain_scale:
        if pain_scale == 0:
            seq += ' No pain.'
        elif 1 <= pain_scale <= 4:
            seq += ' Mild pain.'
        elif 5 <= pain_scale <= 7:
            seq += ' Moderate pain.'
        elif 8 <= pain_scale:
            seq += ' Severe pain.'
    return seq

def add_immunospressed_to_seq(seq, immunocompromised):
    if immunocompromised:
        if immunocompromised == 1:
            seq += ' Immune suppressed.'
    return seq

def add_mental_health_to_seq(seq, mental_health_concerns):
    if mental_health_concerns:
        if mental_health_concerns == 'YES':
            seq += ' Mental health concerns.'
    return seq

def add_triage_assessment(seq, triage_assessment):
    if triage_assessment:
        seq += ' {}'.format(triage_assessment)
    return seq

def add_adult_vital_signs(seq, event):
    """
    Add vital sign indicators to seqeunce for an adult event.
    """
    if event.respiratory_rate:
        if event.respiratory_rate <= 4:
            seq += ' Critically low respiratory rate.'
        elif event.respiratory_rate >= 36:
            seq += ' Critically high respiratory rate.'
        elif (event.respiratory_rate >= 25) & (event.respiratory_rate <= 35):
            seq += ' Extremely high respiratory rate.'    
        elif (event.respiratory_rate >= 5) & (event.respiratory_rate <= 8):
            seq += ' Extremely low respiratory rate.'
        elif (event.respiratory_rate >= 21) & (event.respiratory_rate <= 24):
            seq += ' Very high respiratory rate.'
        elif (event.respiratory_rate >= 10) & (event.respiratory_rate <= 11):
            seq += ' Low Respiratory Rate.'
    
    if event.sats:
        if event.sats <= 91:
            seq += ' Extremely low oxygen saturation.'
        elif (event.sats >= 92) & (event.sats <= 93):
            seq += ' Very low oxygen Saturation.'
        elif (event.sats >= 94) & (event.sats <= 95):
            seq += ' Low oxygen Saturation.'

    if event.vital_signs_pulse:
        if (event.vital_signs_pulse < 40):
            seq += ' Critically low pulse.'
        elif (event.vital_signs_pulse > 140):
            seq += ' Critically high pulse.'
        elif (event.vital_signs_pulse >= 130) & (event.vital_signs_pulse < 140):
            seq += ' Extremely high pulse.'
        elif (event.vital_signs_pulse >= 110) & (event.vital_signs_pulse < 130):
            seq += ' Very high pulse.'
        elif (event.vital_signs_pulse >= 40) & (event.vital_signs_pulse < 50):
            seq += ' Very low pulse.'
        elif (event.vital_signs_pulse >= 90) & (event.vital_signs_pulse < 110):
            seq += ' High pulse.'
    
    if event.blood_pressure_systolic:
        if event.blood_pressure_systolic <= 80: # n.b, lifted from 69 -> 80 to match triage framework
            seq += ' Critically low blood pressure.'
        elif event.blood_pressure_systolic >= 220:
            seq += ' Extemely high blood pressure.'
        elif (event.blood_pressure_systolic >= 80) & (event.blood_pressure_systolic < 90):
            seq += ' Extemely Low blood pressure.'
        elif (event.blood_pressure_systolic >= 90) & (event.blood_pressure_systolic < 100):
            seq += ' Very low blood pressure.'
        elif (event.blood_pressure_systolic >= 100) & (event.blood_pressure_systolic < 110):
            seq += ' Low blood pressure.'

    if event.temperature:
        if event.temperature <= 34:
            seq += ' Extremely low temperature.'
        elif event.temperature >= 39:
            seq += ' Extremely high temperature.'
        elif (event.temperature < 36) & (event.temperature > 34):
            seq += ' Very low temperature.'
        elif (event.temperature < 39) & (event.temperature >= 38):
            seq += ' Very high Temperature.'
        # n.b. below not in EWS, but added for visibility around 36.5, 37.5
        elif (event.temperature <= 36.5) & (event.temperature > 36):
            seq += ' Low temperature.'
        elif (event.temperature < 38) & (event.temperature >= 37.5):
            seq += ' High Temperature.'
        
    return seq


def add_paediatric_vital_signs_0_3_months(seq, event):
    """
    Add vital sign indicators to seqeunce for a newborn event.
    """
    if event.respiratory_rate:
        if event.respiratory_rate <= 15:
            seq += ' Critically low respiratory rate.'
        elif event.respiratory_rate >= 80:
            seq += ' Critically high respiratory rate.'
        elif (event.respiratory_rate >= 70) & (event.respiratory_rate <= 80):
            seq += ' Extremely high respiratory rate.'    
        elif (event.respiratory_rate >= 15) & (event.respiratory_rate <= 20):
            seq += ' Extremely low respiratory rate.'
        elif (event.respiratory_rate >= 65) & (event.respiratory_rate <= 70):
            seq += ' Very high respiratory rate.'
        elif (event.respiratory_rate >= 20) & (event.respiratory_rate <= 25):
            seq += ' Very low respiratory rate.'
        elif (event.respiratory_rate >= 60) & (event.respiratory_rate <= 65):
            seq += ' High respiratory rate.'
        elif (event.respiratory_rate >= 25) & (event.respiratory_rate <= 30):
            seq += ' Low Respiratory Rate.'
    
    if event.sats:
        if event.sats < 85:
            seq += ' Extremely low oxygen saturation.'
        elif (event.sats >= 85) & (event.sats <= 88):
            seq += ' Very low oxygen Saturation.'
        elif (event.sats >= 89) & (event.sats <= 92):
            seq += ' Low oxygen Saturation.'

    if event.vital_signs_pulse:
        if (event.vital_signs_pulse < 60):
            seq += ' Critically low pulse.'
        elif (event.vital_signs_pulse >= 190):
            seq += ' Extremely high pulse.'
        elif (event.vital_signs_pulse >= 170) & (event.vital_signs_pulse < 190):
            seq += ' Very high pulse.'
        elif (event.vital_signs_pulse >= 60) & (event.vital_signs_pulse < 90):
            seq += ' Very low pulse.'    
        elif (event.vital_signs_pulse >= 160) & (event.vital_signs_pulse < 170):
            seq += ' High pulse.'
        elif (event.vital_signs_pulse >= 90) & (event.vital_signs_pulse < 100):
            seq += ' Low pulse.'
    
    if event.blood_pressure_systolic:
        if event.blood_pressure_systolic <= 50:
            seq += ' Critically low blood pressure.'
        elif (event.blood_pressure_systolic >= 50) & (event.blood_pressure_systolic < 55):
            seq += ' Extemely Low blood pressure.'
        elif (event.blood_pressure_systolic >= 55) & (event.blood_pressure_systolic < 65):
            seq += ' Very low blood pressure.'
        elif event.blood_pressure_systolic >= 120:
            seq += ' Very high blood pressure.'
        elif (event.blood_pressure_systolic >= 65) & (event.blood_pressure_systolic < 75):
            seq += ' Low blood pressure.'

    # n.b no ews scores for paediatric temperature, but is still considered at triage
    # so maintain consistency with adult ews
    if event.temperature:
        if event.temperature <= 34:
            seq += ' Extremely low temperature.'
        elif event.temperature >= 39:
            seq += ' Extremely high temperature.'
        elif (event.temperature < 36) & (event.temperature > 34):
            seq += ' Very low temperature.'
        elif (event.temperature < 39) & (event.temperature >= 38):
            seq += ' Very high Temperature.'
        # n.b. below not in EWS, but added for visibility around 36.5, 37.5
        elif (event.temperature <= 36.5) & (event.temperature > 36):
            seq += ' Low temperature.'
        elif (event.temperature < 38) & (event.temperature >= 37.5):
            seq += ' High Temperature.'

    return seq
    
    

def add_paediatric_vital_signs_4_11_months(seq, event):
    """
    Add vital sign indicators to seqeunce for a baby event.
    """
    if event.respiratory_rate:
        if event.respiratory_rate <= 10:
            seq += ' Critically low respiratory rate.'
        elif (event.respiratory_rate >= 55):
            seq += ' Extremely high respiratory rate.'    
        elif (event.respiratory_rate >= 10) & (event.respiratory_rate <= 15):
            seq += ' Extremely low respiratory rate.'
        elif (event.respiratory_rate >= 50) & (event.respiratory_rate <= 55):
            seq += ' Very high respiratory rate.'
        elif (event.respiratory_rate >= 15) & (event.respiratory_rate <= 20):
            seq += ' Very low respiratory rate.'
        elif (event.respiratory_rate >= 45) & (event.respiratory_rate <= 50):
            seq += ' High respiratory rate.'
    
    if event.sats:
        if event.sats < 85:
            seq += ' Extremely low oxygen saturation.'
        elif (event.sats >= 85) & (event.sats <= 88):
            seq += ' Very low oxygen Saturation.'
        elif (event.sats >= 89) & (event.sats <= 92):
            seq += ' Low oxygen Saturation.'

    if event.vital_signs_pulse:
        if (event.vital_signs_pulse < 60):
            seq += ' Critically low pulse.'
        elif (event.vital_signs_pulse >= 190):
            seq += ' Extremely high pulse.'
        elif (event.vital_signs_pulse >= 60) & (event.vital_signs_pulse < 80):
            seq += ' Extremely low pulse.'
        elif (event.vital_signs_pulse >= 170) & (event.vital_signs_pulse < 190):
            seq += ' Very high pulse.'
        elif (event.vital_signs_pulse >= 80) & (event.vital_signs_pulse < 90):
            seq += ' Very low pulse.'
        elif (event.vital_signs_pulse >= 160) & (event.vital_signs_pulse < 170):
            seq += ' High pulse.'
        elif (event.vital_signs_pulse >= 90) & (event.vital_signs_pulse < 100):
            seq += ' Low pulse.'
    
    if event.blood_pressure_systolic:
        if event.blood_pressure_systolic <= 50:
            seq += ' Critically low blood pressure.'
        elif (event.blood_pressure_systolic >= 50) & (event.blood_pressure_systolic < 55):
            seq += ' Extemely low blood pressure.'
        elif (event.blood_pressure_systolic >= 55) & (event.blood_pressure_systolic < 65):
            seq += ' Very low blood pressure.'
        elif event.blood_pressure_systolic >= 120:
            seq += ' Very high blood pressure.'
        elif (event.blood_pressure_systolic >= 65) & (event.blood_pressure_systolic < 75):
            seq += ' Low blood pressure.'

    # n.b no ews scores for paediatric temperature, but is still considered at triage
    # so maintain consistency with adult ews
    if event.temperature:
        if event.temperature <= 34:
            seq += ' Extremely low temperature.'
        elif event.temperature >= 39:
            seq += ' Extremely high temperature.'
        elif (event.temperature < 36) & (event.temperature > 34):
            seq += ' Very low temperature.'
        elif (event.temperature < 39) & (event.temperature >= 38):
            seq += ' Very high Temperature.'
        # n.b. below not in EWS, but added for visibility around 36.5, 37.5
        elif (event.temperature <= 36.5) & (event.temperature > 36):
            seq += ' Low temperature.'
        elif (event.temperature < 38) & (event.temperature >= 37.5):
            seq += ' High Temperature.'
    
    return seq


def add_paediatric_vital_signs_1_4_years(seq, event):
    """
    Add vital sign indicators to seqeunce for a child event.
    """
    if event.respiratory_rate:
        if event.respiratory_rate <= 5:
            seq += ' Critically low respiratory rate.'
        elif (event.respiratory_rate >= 50):
            seq += ' Extremely high respiratory rate.'    
        elif (event.respiratory_rate >= 5) & (event.respiratory_rate <= 10):
            seq += ' Extremely low respiratory rate.'
        elif (event.respiratory_rate >= 40) & (event.respiratory_rate <= 50):
            seq += ' Very high respiratory rate.'
        elif (event.respiratory_rate >= 10) & (event.respiratory_rate <= 15):
            seq += ' Very low respiratory rate.'
        elif (event.respiratory_rate >= 35) & (event.respiratory_rate <= 40):
            seq += ' High respiratory rate.'
    
    if event.sats:
        if event.sats < 85:
            seq += ' Extremely low oxygen saturation.'
        elif (event.sats >= 85) & (event.sats <= 88):
            seq += ' Very low oxygen Saturation.'
        elif (event.sats >= 89) & (event.sats <= 92):
            seq += ' Low oxygen Saturation.'

    if event.vital_signs_pulse:
        if (event.vital_signs_pulse < 60):
            seq += ' Critically low pulse.'
        elif (event.vital_signs_pulse >= 170):
            seq += ' Extremely high pulse.'
        elif (event.vital_signs_pulse >= 60) & (event.vital_signs_pulse < 70):
            seq += ' Extremely low pulse.'
        elif (event.vital_signs_pulse >= 160) & (event.vital_signs_pulse < 170):
            seq += ' Very high pulse.'
        elif (event.vital_signs_pulse >= 70) & (event.vital_signs_pulse < 80):
            seq += ' Very low pulse.'    
        elif (event.vital_signs_pulse >= 140) & (event.vital_signs_pulse < 160):
            seq += ' High pulse.'
        elif (event.vital_signs_pulse >= 80) & (event.vital_signs_pulse < 90):
            seq += ' Low pulse.'
    
    if event.blood_pressure_systolic:
        if event.blood_pressure_systolic <= 55:
            seq += ' Critically low blood pressure.'
        elif (event.blood_pressure_systolic >= 55) & (event.blood_pressure_systolic < 65):
            seq += ' Extemely low blood pressure.'
        elif (event.blood_pressure_systolic >= 65) & (event.blood_pressure_systolic < 70):
            seq += ' Very low blood pressure.'
        elif event.blood_pressure_systolic >= 120:
            seq += ' Very high blood pressure.'
        elif (event.blood_pressure_systolic >= 70) & (event.blood_pressure_systolic < 80):
            seq += ' Low blood pressure.'

    # n.b no ews scores for paediatric temperature, but is still considered at triage
    # so maintain consistency with adult ews
    if event.temperature:
        if event.temperature <= 34:
            seq += ' Extremely low temperature.'
        elif event.temperature >= 39:
            seq += ' Extremely high temperature.'
        elif (event.temperature < 36) & (event.temperature > 34):
            seq += ' Very low temperature.'
        elif (event.temperature < 39) & (event.temperature >= 38):
            seq += ' Very high Temperature.'
        # n.b. below not in EWS, but added for visibility around 36.5, 37.5
        elif (event.temperature <= 36.5) & (event.temperature > 36):
            seq += ' Low temperature.'
        elif (event.temperature < 38) & (event.temperature >= 37.5):
            seq += ' High Temperature.'

    return seq



def add_paediatric_vital_signs_5_11_years(seq, event):
    """
    Add vital sign indicators to seqeunce for a youth event.
    """
    if event.respiratory_rate:
        if event.respiratory_rate <= 5:
            seq += ' Critically low respiratory rate.'
        elif (event.respiratory_rate >= 45):
            seq += ' Extremely high respiratory rate.'    
        elif (event.respiratory_rate >= 5) & (event.respiratory_rate <= 10):
            seq += ' Very low respiratory rate.'
        elif (event.respiratory_rate >= 40) & (event.respiratory_rate <= 45):
            seq += ' Very high respiratory rate.'
        elif (event.respiratory_rate >= 10) & (event.respiratory_rate <= 15):
            seq += ' Low respiratory rate.'
        elif (event.respiratory_rate >= 30) & (event.respiratory_rate <= 40):
            seq += ' High respiratory rate.'
    
    if event.sats:
        if event.sats < 85:
            seq += ' Extremely low oxygen saturation.'
        elif (event.sats >= 85) & (event.sats <= 88):
            seq += ' Very low oxygen Saturation.'
        elif (event.sats >= 89) & (event.sats <= 92):
            seq += ' Low oxygen Saturation.'

    if event.vital_signs_pulse:
        if (event.vital_signs_pulse < 30):  # n.b not in ews but add to match adult
            seq += ' Critically low pulse.'
        elif (event.vital_signs_pulse >= 170):
            seq += ' Extremely high pulse.'
        elif (event.vital_signs_pulse >= 30) & (event.vital_signs_pulse < 60):
            seq += ' Extremely low pulse.'
        elif (event.vital_signs_pulse >= 150) & (event.vital_signs_pulse < 170):
            seq += ' Very high pulse.'
        elif (event.vital_signs_pulse >= 60) & (event.vital_signs_pulse < 70):
            seq += ' Very low pulse.'    
        elif (event.vital_signs_pulse >= 130) & (event.vital_signs_pulse < 150):
            seq += ' High pulse.'
        elif (event.vital_signs_pulse >= 70) & (event.vital_signs_pulse < 80):
            seq += ' Low pulse.'
    
    if event.blood_pressure_systolic:
        if event.blood_pressure_systolic <= 55:
            seq += ' Critically low blood pressure.'
        elif (event.blood_pressure_systolic >= 55) & (event.blood_pressure_systolic < 65):
            seq += ' Extemely low blood pressure.'
        elif (event.blood_pressure_systolic >= 65) & (event.blood_pressure_systolic < 75):
            seq += ' Very low blood pressure.'
        elif event.blood_pressure_systolic >= 120:
            seq += ' Very high blood pressure.'
        elif (event.blood_pressure_systolic >= 75) & (event.blood_pressure_systolic < 85):
            seq += ' Low blood pressure.'

    # n.b no ews scores for paediatric temperature, but is still considered at triage
    # so maintain consistency with adult ews
    if event.temperature:
        if event.temperature <= 34:
            seq += ' Extremely low temperature.'
        elif event.temperature >= 39:
            seq += ' Extremely high temperature.'
        elif (event.temperature < 36) & (event.temperature > 34):
            seq += ' Very low temperature.'
        elif (event.temperature < 39) & (event.temperature >= 38):
            seq += ' Very high Temperature.'
        # n.b. below not in EWS, but added for visibility around 36.5, 37.5
        elif (event.temperature <= 36.5) & (event.temperature > 36):
            seq += ' Low temperature.'
        elif (event.temperature < 38) & (event.temperature >= 37.5):
            seq += ' High Temperature.'

    return seq


def add_paediatric_vital_signs_12_years_adult(seq, event):
    """
    Add vital sign indicators to seqeunce for a youth event.
    """
    if event.respiratory_rate:
        if event.respiratory_rate <= 5:
            seq += ' Critically low respiratory rate.'
        elif (event.respiratory_rate >= 35):
            seq += ' Extremely high respiratory rate.'    
        elif (event.respiratory_rate >= 5) & (event.respiratory_rate <= 10):
            seq += ' Very low respiratory rate.'
        elif (event.respiratory_rate >= 30) & (event.respiratory_rate <= 35):
            seq += ' Very high respiratory rate.'
        elif (event.respiratory_rate >= 10) & (event.respiratory_rate <= 15):
            seq += ' Low respiratory rate.'
        elif (event.respiratory_rate >= 25) & (event.respiratory_rate <= 30):
            seq += ' High respiratory rate.'
    
    if event.sats:
        if event.sats < 85:
            seq += ' Extremely low oxygen saturation.'
        elif (event.sats >= 85) & (event.sats <= 88):
            seq += ' Very low oxygen Saturation.'
        elif (event.sats >= 89) & (event.sats <= 92):
            seq += ' Low oxygen Saturation.'

    if event.vital_signs_pulse:
        if (event.vital_signs_pulse < 30):  # n.b not in ews but add to match adult
            seq += ' Critically low pulse.'
        elif (event.vital_signs_pulse >= 140):
            seq += ' Extremely high pulse.'
        elif (event.vital_signs_pulse >= 30) & (event.vital_signs_pulse < 50):
            seq += ' Extremely low pulse.'
        elif (event.vital_signs_pulse >= 120) & (event.vital_signs_pulse < 140):
            seq += ' Very high pulse.'  
        elif (event.vital_signs_pulse >= 110) & (event.vital_signs_pulse < 120):
            seq += ' High pulse.'
        elif (event.vital_signs_pulse >= 50) & (event.vital_signs_pulse < 60):
            seq += ' Low pulse.'
    
    if event.blood_pressure_systolic:
        if event.blood_pressure_systolic <= 70:
            seq += ' Critically low blood pressure.'
        elif (event.blood_pressure_systolic >= 70) & (event.blood_pressure_systolic < 80):
            seq += ' Extemely low blood pressure.'
        elif (event.blood_pressure_systolic >= 80) & (event.blood_pressure_systolic < 85):
            seq += ' Very low blood pressure.'
        elif event.blood_pressure_systolic >= 145:
            seq += ' Very high blood pressure.'
        elif (event.blood_pressure_systolic >= 85) & (event.blood_pressure_systolic < 90):
            seq += ' Low blood pressure.'

    # n.b no ews scores for paediatric temperature, but is still considered at triage
    # so maintain consistency with adult ews
    if event.temperature:
        if event.temperature <= 34:
            seq += ' Extremely low temperature.'
        elif event.temperature >= 39:
            seq += ' Extremely high temperature.'
        elif (event.temperature < 36) & (event.temperature > 34):
            seq += ' Very low temperature.'
        elif (event.temperature < 39) & (event.temperature >= 38):
            seq += ' Very high Temperature.'
        # n.b. below not in EWS, but added for visibility around 36.5, 37.5
        elif (event.temperature <= 36.5) & (event.temperature > 36):
            seq += ' Low temperature.'
        elif (event.temperature < 38) & (event.temperature >= 37.5):
            seq += ' High Temperature.'

    return seq


 
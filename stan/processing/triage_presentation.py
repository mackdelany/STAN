from collections import namedtuple

TriagePresentation = namedtuple(
    'TriagePresentation',
    ['present_date_time', 
    'dob', 
    'age_in_months',
    'presenting_complaint',
    'gender',
    'airway_altered',
    'breathing_altered',
    'circulation_altered',
    'disability_gcs',
    'neuro_assessment',
    'pain_scale',
    'vital_signs_pulse',
    'respiratory_rate',
    'blood_pressure_systolic',
    'blood_pressure_diastolic',
    'temperature',
    'sats',
    'mental_health_concerns',
    'immunocompromised',
    'triage_assessment',
    'nurse_triage_code'
    ]
    )
import datetime
from pathlib import Path

DATA_FOLDER_PATH = '/Users/mackdelany/Documents/STAN/stan_model/data/'
EDAAG_RAW = 'raw.csv'
# input('What is the stan production data filename?')
STAN_PROD = 'STAN_PROD_DATA_18_04_21.csv'
SNOMED_ENCODING = 'snomed_encoding.csv'

EDAAG_RAW_PATH = Path(DATA_FOLDER_PATH, EDAAG_RAW)
STAN_PROD_PATH = Path(DATA_FOLDER_PATH, STAN_PROD)
SNOMED_ENCODING_PATH = Path(DATA_FOLDER_PATH, SNOMED_ENCODING)

TRIAGE_PRESENTION_COLS = [
    'origin_id',
    'event_id',
    'data_class',
    'present_date_time',
    'dob',
    'age_in_months',
    'gender',
    'presenting_complaint',
    'triage_assessment',
    'airway_altered',
    'breathing_altered',
    'circulation_altered',
    'disability_gcs',
    'neuro_altered',
    'pain_scale',
    'vital_signs_pulse',
    'respiratory_rate',
    'blood_pressure_systolic',
    'blood_pressure_diastolic',
    'temperature',
    'sats',
    'mental_health_concerns',
    'immunocompromised',
    'nurse_triage_code',
    'stan_triage_code',
    'final_triage_record',
    'first_nurse_code',
    'final_nurse_code',
    'diagnosis'
]

FAST_COLS = [
    'origin_id',
    'event_id',
    'data_class',
    'present_date_time',
    'dob',
    'age_in_months',
    'gender',
    'presenting_complaint',
    'triage_assessment',
    'nurse_triage_code',
    'stan_triage_code',
    'diagnosis'
]

VITAL_COLS = [
    'origin_id',
    'event_id',
    'data_class',
    'present_date_time',
    'dob',
    'age_in_months',
    'gender',
    'presenting_complaint',
    'triage_assessment',
    'vital_signs_pulse',
    'respiratory_rate',
    'blood_pressure_systolic',
    'blood_pressure_diastolic',
    'temperature',
    'sats',
    'nurse_triage_code'
    'stan_triage_code',
    'diagnosis'
]

FULL_COLS = [
    'origin_id',
    'event_id',
    'data_class',
    'present_date_time',
    'dob',
    'age_in_months',
    'gender',
    'presenting_complaint',
    'triage_assessment',
    'airway_altered',
    'breathing_altered',
    'circulation_altered',
    'disability_gcs',
    'neuro_altered',
    'pain_scale',
    'vital_signs_pulse',
    'respiratory_rate',
    'blood_pressure_systolic',
    'blood_pressure_diastolic',
    'temperature',
    'sats',
    'mental_health_concerns',
    'immunocompromised',
    'final_triage_record',
    'first_nurse_code',
    'final_nurse_code',
    'nurse_triage_code',
    'stan_triage_code',
    'diagnosis'
]

TARGET_COLS = [
    'y1_triage_code',
    'y2_airway_altered',
    'y3_breathing_altered',
    'y4_circulation_altered',
    'y5_disability_altered',
    'y6_neuro_altered',
    'y7_immunocompromised',
    'y8_mental_health',
    'y9_sepsis'
]

MENTAL_HEALTH_CPC = [
    'Aggressive behaviour',
    'Abnormal behaviour',
    'Altered mental state/confusion',
    'Aggressive behaviour',
    'Mental health problem',
    'Situational crisis',
    'Suicidal thoughts',
    'Anxiety',
    'Self harm',
    'Insomnia',
    'Overdose of drug'
]

SEPSIS_DIAGNOSIS = [
    'Neutropaenic sepsis',
    'Sepsis (add source if known)',
    'Septic shock (add source if known)'
]

TEST_SET_SIZE = 0.05

today = datetime.datetime.today().day
month = datetime.datetime.today().month
CLEAN_FILENAME = 'stan_full_{}_{}.csv'.format(today, month)

TRAIN_FILENAME = 'stan_train_{}_{}.csv'.format(today, month)

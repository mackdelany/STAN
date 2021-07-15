from .custom_functions import *
from .triage_framework import enforce_triage_framework_adherance


TARGET_FEATURE = {'TriageCode': int}

DATA_FEATURES = {
    'PresentingComplaint': str,
    'PresentDateTime': str,
    'DOB': str,
    'Gender': str,
    'Airway': str,
    'Breathing': str,
    'NeuroAssessment': str,
    'PainScale': int,
    'CirculatorySkin': str,
    'MentalHealthConcerns': str,
    'DisabilityValue': str,
    'VitalSignsPulse': float,
    'RespiratoryRate': float,
    'BloodPressure_systolic': float,
    'BloodPressure_diastolic': float,
    'Temperature': float,
    'Sats': float,
    'PainScale_was_measured': int,
    'Airway_was_measured': int,
    'Breathing_was_measured': int,
    'CirculatorySkin_was_measured': int,
    'DisabilityValue_was_measured': int,
    'NeuroAssessment_was_measured': int,
    'MentalHealthConcerns_was_measured': int,
    'Immunocompromised_was_measured': int,
    'VitalSignsPulse_was_measured': int,
    'RespiratoryRate_was_measured': int,
    'BloodPressure_was_measured': int,
    'Sats_was_measured': int,
    'Temperature_was_measured': int,
    'Immunocompromised': int,
    'TriageCode': int
}

# DROP = drop null columns
# String = fill null with string
# ZEROS = fill null with zero
# Dictionary = run cleaningFunction, dict should hold {'function name': 'parameters'}
GENERAL_FEATURE_IMPUTATION = {
    'PresentDateTime': 'DROP',
    'DOB': 'DROP',
    'Gender': 'U',
    'Airway': 'PATENT',
    'Breathing': 'NO DISTRESS',
    'CirculatorySkin': 'NORMAL',
    'DisabilityValue': 'A',
    'NeuroAssessment': 'INTACT',
    'PainScale': -1,
    'MentalHealthConcerns': 'NO',
    'TriageCode': 'DROP',
    'Immunocompromised': 0,
}

VITAL_SIGN_IMPUTATION = {
    'BloodPressure_systolic': {'mean': 115, 'std_dev': 4, 'sig_fig': 0},
    'BloodPressure_diastolic': {'mean': 70, 'std_dev': 3, 'sig_fig': 0},
    'Temperature': {'mean': 37, 'std_dev': 0.2, 'sig_fig': 1},
    'Sats': {'mean': 97.5, 'std_dev': 1, 'sig_fig': 1}
}


# Dictionary = mapping of values
FEATURE_TRANSFORMATIONS_1 = {

    'Gender': {'M': 'M', 'm': 'M', 'U': 'U', ' ': 'U', 'F': 'F'},
    'Airway': {'PATENT': 'PATENT', 'ASSUMED OK': 'PATENT', 'OBSTRUCTED': 'OTHER', 'OTHER': 'OTHER'},
    'Breathing': {'NO DISTRESS': 'NO DISTRESS', 'NIL RESPIRATORY DISTRESS': 'NO DISTRESS', 'ASSUMED OK': 'NO DISTRESS', 'OTHER': 'OTHER'},
    'NeuroAssessment': {'INTACT': 'INTACT', 'NO': 'INTACT', 'ASSUMED OK': 'INTACT', 'POSSIBLE': 'POSSIBLE', 'OTHER': 'OTHER'},
    'MentalHealthConcerns': {'NO': 'NO', 'ASSUMED NO': 'NO', 'DNS': 'DNS', 'YES': 'YES'},
    'DisabilityValue': {'ASSUMED NO': 'A', 'A': 'A', ' ': 'A', 'V': 'V', 'P': 'P', 'U': 'U'},

    'CirculatorySkin': {
        'NORMAL': 'NORMAL', 'ASSUMED NORMAL': 'NORMAL', '   ': 'NORMAL', 'PINK WARM DRY ': 'NORMAL', 'PALE WARM DRY ': 'NORMAL', 'PINK WARM DRY CAPRF': 'NORMAL', 'PINK WARM  CAPRF': 'NORMAL',
        'PINK WARM  ': 'NORMAL', 'PINK   ': 'NORMAL', ' WARM  ': 'NORMAL', 'PINK   CAPRF': 'NORMAL', ' WARM DRY ': 'NORMAL', ' WARM  CAPRF': 'NORMAL', 'PALE WARM  ': 'NORMAL', 'PINK  DRY ': 'NORMAL',
        'PALE WARM  CAPRF': 'NORMAL', 'PINK  DRY CAPRF': 'NORMAL', '   CAPRF': 'NORMAL', '  DRY CAPRF': 'NORMAL', ' WARM MOIST ': 'NORMAL', ' WARM MOIST CAPRF': 'NORMAL', '  DRY ': 'NORMAL',
        '    ': 'NORMAL', 'PINK WARM   ': 'NORMAL', 'PINK WARM DRY  ': 'NORMAL', 'PALE WARM   ': 'NORMAL', ' WARM DRY CAPRF ': 'NORMAL', 'PALE  DRY CAPRF ': 'NORMAL', ' WARM DRY  ': 'NORMAL',
        '  DRY  ': 'NORMAL', 'PINK WARM DRY CAPRF ': 'NORMAL', 'PALE WARM DRY CAPRF ': 'NORMAL', 'PINK    ': 'NORMAL', 'PALE WARM DRY  ': 'NORMAL', 'PINK  DRY  ': 'NORMAL', 'PINK  DRY CAPRF ': 'NORMAL',
        'PINK WARM   OTH': 'NORMAL', 'PINK   CAPRF ': 'NORMAL', 'PALE WARM  CAPRF ': 'NORMAL', ' WARM   ': 'NORMAL', 'PINK WARM  CAPRF ': 'NORMAL', 'PINK WARM DRY  OTH': 'NORMAL', '  DRY CAPRF ': 'NORMAL',
        ' WARM  CAPRF ': 'NORMAL',

        'ALTERED': 'ALTERED', 'PALE COOL MOIST ': 'ALTERED', ' COOL MOIST CAPRF ': 'ALTERED', 'PALE COOL   ': 'ALTERED', 'PALE  MOIST  ': 'ALTERED', 'PALE COOL MOIST CAPRF': 'ALTERED',
        'PINK COOL DRY  ': 'ALTERED', ' COOL DRY  ': 'ALTERED', 'CYANOSED COOL MOIST  ': 'ALTERED', 'PALE COOL MOIST  ': 'ALTERED', ' COOL MOIST  ': 'ALTERED', 'CYANOSED COOL  CAPRF': 'ALTERED',
        ' COOL  ': 'ALTERED', 'PINK WARM MOIST ': 'ALTERED', 'PINK WARM MOIST CAPRF': 'ALTERED', 'PALE WARM MOIST ': 'ALTERED', 'PINK COOL DRY ': 'ALTERED', 'PALE COOL DRY CAPRF': 'ALTERED',
        'PALE  MOIST CAPRF': 'ALTERED', 'PALE COOL DRY ': 'ALTERED', 'CYANOSED WARM DRY ': 'ALTERED', 'PINK COOL MOIST ': 'ALTERED', ' WARM DRY CAPRF': 'ALTERED', 'PALE WARM MOIST CAPRF': 'ALTERED',
        'PALE   ': 'ALTERED', 'PALE WARM DRY CAPRF': 'ALTERED', ' COOL DRY ': 'ALTERED', 'CYANOSED WARM  ': 'ALTERED', 'PINK COOL MOIST CAPRF': 'ALTERED', 'PINK COOL  ': 'ALTERED', 'PINK COOL DRY CAPRF': 'ALTERED',
        'CYANOSED COOL MOIST ': 'ALTERED', 'PALE COOL  ': 'ALTERED', ' COOL MOIST ': 'ALTERED', 'PALE  DRY ': 'ALTERED', 'PALE  DRY CAPRF': 'ALTERED', 'PINK  MOIST ': 'ALTERED', 'PALE   CAPRF': 'ALTERED',
        'CYANOSED COOL DRY CAPRF': 'ALTERED', 'PALE  MOIST ': 'ALTERED', 'PINK  MOIST CAPRF': 'ALTERED', 'CYANOSED COOL DRY ': 'ALTERED', 'CYANOSED COOL  ': 'ALTERED', 'CYANOSED   ': 'ALTERED',
        '  MOIST ': 'ALTERED', 'PINK COOL  CAPRF': 'ALTERED', ' COOL DRY CAPRF': 'ALTERED', 'CYANOSED WARM  CAPRF': 'ALTERED', 'PALE COOL  CAPRF': 'ALTERED', 'CYANOSED WARM DRY CAPRF': 'ALTERED',
        ' COOL MOIST CAPRF': 'ALTERED', 'CYANOSED COOL MOIST CAPRF': 'ALTERED', 'PALE COOL MOIST CAPRF ': 'ALTERED', 'PINK WARM MOIST CAPRF OTH': 'ALTERED',
        'CYANOSED WARM DRY  ': 'ALTERED', 'PALE COOL DRY CAPRF ': 'ALTERED', 'PINK COOL DRY CAPRF ': 'ALTERED', 'PALE COOL DRY  ': 'ALTERED', 'PINK WARM DRY CAPRF OTH': 'ALTERED',
        ' WARM DRY  OTH': 'ALTERED', 'PALE  DRY  ': 'ALTERED', 'PINK WARM MOIST  ': 'ALTERED', 'PINK WARM MOIST CAPRF ': 'ALTERED', 'PALE    ': 'ALTERED', 'CYANOSED WARM MOIST ': 'ALTERED',
        'CYANOSED COOL DRY CAPRF ': 'ALTERED', 'CYANOSED WARM MOIST  ': 'ALTERED', 'PINK COOL MOIST  ': 'ALTERED', ' COOL  CAPRF': 'ALTERED', 'CYANOSED WARM DRY  OTH': 'ALTERED',
        '   CAPRF ': 'ALTERED', 'PINK  MOIST CAPRF ': 'ALTERED', 'CYANOSED  DRY ': 'ALTERED', 'PINK COOL   ': 'ALTERED', 'PALE WARM DRY CAPRF OTH': 'ALTERED', 'CYANOSED WARM MOIST CAPRF': 'ALTERED',
        'CYANOSED WARM DRY CAPRF ': 'ALTERED', ' WARM MOIST  ': 'ALTERED', 'PALE WARM MOIST  ': 'ALTERED', 'PINK  MOIST  ': 'ALTERED', 'PALE COOL  CAPRF ': 'ALTERED', 'PALE COOL DRY  OTH': 'ALTERED'
    },
}


FEATURE_TRANSFORMATIONS_2 = {
    'Gender': {'M': 0, 'U': 0.5, 'F': 1},
    'Airway': {'PATENT': 0, 'OTHER': 1},
    'Breathing': {'NO DISTRESS': 0, 'OTHER': 1},
    'NeuroAssessment': {'INTACT': 0, 'POSSIBLE': 0.5, 'OTHER': 1},
    'MentalHealthConcerns': {'NO': 0, 'DNS': 0.5, 'YES': 1},
    'DisabilityValue': {'A': 0, 'V': 0.5, 'P': 0.75, 'U': 1},
    'CirculatorySkin': {'NORMAL': 0, 'ALTERED': 1},
    # 'PainScale': {0: 0, 1: 0, 2: 3, 3: 3, 4: 3, 5: 6, 6: 6, 7: 6, 8: 9, 9: 9, 10:10}  # To introduce when pain scale variability changes
}

FEATURE_TRANSFORMATIONS_3 = {
    'Gender': {'M': 0, 'U': 0.5, 'F': 1},
    'Airway': {'PATENT': False, 'OTHER': 1},
    'Breathing': {'NO DISTRESS': False, 'OTHER': 1},
    'NeuroAssessment': {'INTACT': False, 'POSSIBLE': 0.5, 'OTHER': 1},
    'MentalHealthConcerns': {'NO': False, 'DNS': False, 'YES': True},
    'DisabilityValue': {'A': 0, 'V': 0.5, 'P': 0.75, 'U': 1},
    'CirculatorySkin': {'NORMAL': 0, 'ALTERED': 1},
    # 'PainScale': {0: 0, 1: 0, 2: 3, 3: 3, 4: 3, 5: 6, 6: 6, 7: 6, 8: 9, 9: 9, 10:10}  # To introduce when pain scale variability changes
}

FEATURES_TO_HOT_ENCODE = ['PresentingComplaint', 'PresentingComplaintGroup']

# Custom functions to be run, should be a list of lists -> each list should be [feature, [function, parameters]]

CPC_CATEGORY_INDICES = {
    'CNS': 0,
    'CVS': 1,
    'ENV': 2,
    'EYE': 3,
    'GI': 4,
    'GU': 5,
    'HEAD/NECK': 6,
    'MENTAL HEALTH': 7,
    'MISC': 8,
    'MSK': 9,
    'O&G': 10,
    'RESP': 11,
    'SKIN': 12,
    'TOX': 13,
    'TRAUMA/INJURY': 14
}

CPC_CATEGORIES = {
    'Altered mental state/confusion': 'CNS',
    'Altered sensation': 'CNS',
    'Ataxia': 'CNS',
    'Dizziness/vertigo': 'CNS',
    'Fall(s) - no significant injury': 'CNS',
    'Headache': 'CNS',
    'Memory loss': 'CNS',
    'Seizure': 'CNS',
    'Speech problem': 'CNS',
    'Tremor': 'CNS',
    'Weakness of face muscles': 'CNS',
    'Weakness of limb': 'CNS',

    'Cardiac arrest': 'CVS',
    'Chest pain': 'CVS',
    'Collapse/syncope': 'CVS',
    'Palpitations': 'CVS',
    'Shock from internal defibrillator': 'CVS',
    'Swollen leg (single)': 'CVS',
    'Swollen legs (both)': 'CVS',
    'Vascular disorder of limb': 'CVS',

    'Chemical exposure': 'ENV',
    'Drowning': 'ENV',
    'Electrical injury': 'ENV',
    'Frostbite': 'ENV',
    'Hypothermia': 'ENV',
    'Noxious inhalation': 'ENV',
    'Toxic inhalation injury': 'ENV',  # Additional to form

    'Discharge from eye': 'EYE',
    'Foreign body in eye': 'EYE',
    'Pain in eye': 'EYE',
    'Photophobia': 'EYE',
    'Red eye': 'EYE',
    'Visual disturbance': 'EYE',

    'Abdominal distension': 'GI',
    'Abdominal pain': 'GI',
    'Altered bowel habit': 'GI',
    'Feeding problem': 'GI',
    'Foreign body in gastrointestinal tract (swallowed)': 'GI',
    'Foreign body in rectum': 'GI',
    'Foreign body in throat': 'GI',
    'Hiccoughs': 'GI',
    'Jaundice': 'GI',
    'Loss of appetite': 'GI',
    'Mouth problem (not dental)': 'GI',
    'Nausea/vomiting/diarrhoea': 'GI',
    'Pain in anus/rectum': 'GI',
    'Pain in groin': 'GI',
    'Rectal bleed': 'GI',
    'Stoma problem': 'GI',
    'Swallowing problem': 'GI',
    'Vomiting blood': 'GI',
    'Constipation': 'GI',  # Addtional to form

    'Blood in urine': 'GU',
    'Complication of urinary catheter': 'GU',
    'Excessive urine output': 'GU',
    'Foreign body in genitourinary tract': 'GU',
    'Male genital problem': 'GU',
    'Reduced urine output': 'GU',
    'Urethral discharge': 'GU',
    'Urinary retention': 'GU',
    'UTI symptoms': 'GU',


    'Discharge from ear': 'HEAD/NECK',
    'Earache': 'HEAD/NECK',
    'Foreign body in ear canal': 'HEAD/NECK',
    'Foreign body in nose': 'HEAD/NECK',
    'Hearing loss/tinnitus': 'HEAD/NECK',
    'Nose bleed': 'HEAD/NECK',
    'Pain in face': 'HEAD/NECK',
    'Swelling of face': 'HEAD/NECK',
    'Swelling of tongue': 'HEAD/NECK',
    'Toothache/dental infection': 'HEAD/NECK',

    'Abnormal behaviour': 'MENTAL HEALTH',
    'Aggressive behaviour': 'MENTAL HEALTH',
    'Anxiety': 'MENTAL HEALTH',
    'Insomnia': 'MENTAL HEALTH',
    'Mental health problem': 'MENTAL HEALTH',
    'Self harm': 'MENTAL HEALTH',
    'Situational crisis': 'MENTAL HEALTH',
    'Suicidal thoughts': 'MENTAL HEALTH',

    'Abnormal vital sign(s)': 'MISC',
    'Administration of medication': 'MISC',
    'Certificate or paperwork requested': 'MISC',
    'Complication of device (not catheter)': 'MISC',
    'Crying baby': 'MISC',
    'Exposure to blood/body fluid': 'MISC',
    'Exposure to communicable disease': 'MISC',
    'Fever symptoms': 'MISC',
    'Follow-up visit': 'MISC',
    'General weakness/fatigue/unwell': 'MISC',
    'Hyperglycaemia': 'MISC',
    'Hypoglycaemia': 'MISC',
    'Postoperative complication': 'MISC',
    'Referral for investigation': 'MISC',
    'Script request': 'MISC',
    'Wound complication': 'MISC',  # Additional to form

    'Back pain (no recent injury)': 'MSK',
    'Difficulty weight bearing': 'MSK',
    'Increased muscle tone': 'MSK',
    'Neck pain (no recent injury)': 'MSK',
    'Pain in hip': 'MSK',
    'Pain in lower limb (no recent injury)': 'MSK',
    'Pain in upper limb (no recent injury)': 'MSK',
    'Plaster cast problem': 'MSK',
    'Swelling of joint (no recent injury)': 'MSK',

    'Breast problem': 'O&G',
    'Female genital problem': 'O&G',
    'Labour': 'O&G',
    'Postpartum complication': 'O&G',
    'Pregnancy problem': 'O&G',
    'Sexual assault': 'O&G',
    'Vaginal bleeding - not pregnant': 'O&G',
    'Vaginal discharge': 'O&G',
    'Pain in breast': 'O&G',  # Additional to form

    'Cough': 'RESP',
    'Cyanosis': 'RESP',
    'Foreign body in respiratory tract (inhaled)': 'RESP',
    'Coughing up blood': 'RESP',
    'Nasal congestion': 'RESP',
    'Noisy breathing': 'RESP',
    'Periods of not breathing': 'RESP',
    'Respiratory arrest': 'RESP',
    'Shortness of breath': 'RESP',
    'Sore throat': 'RESP',
    'Episodes of not breathing (apnoea)': 'RESP',  # Additional to form

    'Bite': 'SKIN',
    'Burn': 'SKIN',
    'Change of dressing': 'SKIN',
    'Foreign body in skin': 'SKIN',
    'Itching': 'SKIN',
    'Localised lump/redness/swelling of skin': 'SKIN',
    'Open wound (abrasion/laceration/puncture)': 'SKIN',
    'Rash': 'SKIN',
    'Removal of skin sutures or staples': 'SKIN',
    'Spontaneous bruising': 'SKIN',  # Additional to form

    'Alcohol/drug intoxication or withdrawal': 'TOX',
    'Ingestion of potentially harmful substance': 'TOX',
    'Overdose of drug': 'TOX',
    'Sting': 'TOX',

    'Cardiac arrest due to trauma': 'TRAUMA/INJURY',
    'Injury of abdomen': 'TRAUMA/INJURY',
    'Injury of back': 'TRAUMA/INJURY',
    'Injury of buttock': 'TRAUMA/INJURY',
    'Injury of chest': 'TRAUMA/INJURY',
    'Injury of ear': 'TRAUMA/INJURY',
    'Injury of eye': 'TRAUMA/INJURY',
    'Injury of face': 'TRAUMA/INJURY',
    'Injury of genitalia': 'TRAUMA/INJURY',
    'Injury of head': 'TRAUMA/INJURY',
    'Injury of hip': 'TRAUMA/INJURY',
    'Injury of lower limb': 'TRAUMA/INJURY',
    'Injury of neck': 'TRAUMA/INJURY',
    'Injury of nose': 'TRAUMA/INJURY',
    'Injury of perineum': 'TRAUMA/INJURY',
    'Injury of upper limb': 'TRAUMA/INJURY',
    'Multiple injuries - major': 'TRAUMA/INJURY',
    'Multiple injuries - minor': 'TRAUMA/INJURY'
}

CUSTOM_FUNCTIONS_TO_BE_RUN = {
    identify_and_save_cpc_variance:  'NO ADDITIONAL ARGUMENTS',
    encode_cyclical_time_of_day: 'PresentDateTime',
    mean_triage_code: 'NO ADDITIONAL ARGUMENTS',
    add_cpc_groupings: [CPC_CATEGORIES, CPC_CATEGORY_INDICES, '/Users/mackdelany/Documents/STAN/stan_model/mappings/', 'CPC_CATEGORIES.txt', 'CPC_CATEGORY_INDICES.txt'],
}

FINAL_FEATURES = [
    'Gender',
    'PresentingComplaint',
    'Airway',
    'Breathing',
    'NeuroAssessment',
    'PainScale',
    'CirculatorySkin',
    'MentalHealthConcerns',
    'VitalSignsPulse',
    'RespiratoryRate',
    'DisabilityValue',
    'Temperature',
    'Sats',
    'Immunocompromised',
    'TriageCode',
    'Airway_was_measured',
    'Breathing_was_measured',
    'CirculatorySkin_was_measured',
    'DisabilityValue_was_measured',
    'NeuroAssessment_was_measured',
    'PainScale_was_measured',
    'MentalHealthConcerns_was_measured',
    'BloodPressure_was_measured',
    'Temperature_was_measured',
    'Sats_was_measured',
    'Immunocompromised_was_measured',
    'RespiratoryRate_was_measured',
    'VitalSignsPulse_was_measured',
    'AgeInMonths',
    'hour_sin',
    'hour_cos',
    'BloodPressure_systolic',
    'BloodPressure_diastolic',
    'mean_triage_code',
    'PresentingComplaintGroup',
    'ews_emergency_zone',
    'ews_estimate',
    'respiratory_rate_ews',
    'sats_ews',
    'vital_signs_pulse_ews',
    'blood_pressure_systolic_ews',
    'blood_pressure_diastolic_ews',
    'temperature_ews',
    'disability_value_ews'
]

STAN_DB = {
    'user': 'reader',
    'password': 'flickMEupWELL2083709283',
    'db': 'stan',
    'host': 'stan.crce0dy1gqyj.ap-southeast-2.rds.amazonaws.com',
    'port': '5432'
}

STAN_DATABASE_URI = ('postgresql://' +
                     STAN_DB['user'] + ':' +
                     STAN_DB['password'] + '@' +
                     STAN_DB['host'] + ':' +
                     STAN_DB['port'] + '/' +
                     STAN_DB['db']
                     )

PRODUCTION_DHB = 3

RAW_COLUMNS = ['ID', 'DOB', 'Gender', 'PresentingComplaint', 'PresentDateTime',
               'TriageDateTime', 'PhysicalDischarge', 'Airway', 'Breathing',
               'NeuroAssessment', 'PainScale', 'CirculatorySkin',
               'MentalHealthConcerns', 'VitalSignsPulse', 'RespiratoryRate',
               'DisabilityValue', 'BloodPressure', 'Temperature', 'Sats',
               'Immunocompromised', 'TriageCode']

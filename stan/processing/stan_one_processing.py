"""
stan_one data processing
raw edaag + stan production --> stan training data

X | sequences
Y1 | triage code
Y2 | airway altered
Y3 | breathing altered
Y4 | circulation altered
Y5 | disability gcs
Y6 | neuro altered
Y7 | immunocompromised
Y8 | mental health concerns
Y9 | sepsis

eps | edaag pre snomed
epsi | edaag pre snomed imputed to snomed
esno | edaag snomed
stan | stan production

then duplicate and drop vitals for rows with vital measurements ?

ensure test set from recent EDaag data ie ESNO
"""

import sys
from pathlib import Path

import pandas as pd

from .processing_config import *  # ok cause config
from .triage_framework import enforce_triage_framework_adherance
from .snomed_encode import multiple_injuries_imputation, snomed_encode_dataset
from .imputation import (
    check_if_measured, BloodPressure_clean, null_invalid_values,
    impute_general_features, drop_invalid_triage_codes, calculate_patient_age
)
from .data_parameters import GENERAL_FEATURE_IMPUTATION, DATA_FEATURES, FEATURE_TRANSFORMATIONS_1
from .altered_functions import impute_airway, impute_breathing, impute_circulation, impute_disability_gcs, impute_neuro, impute_mental

from ..core.stan_sequence_util import generate_stan_sequence


def load_files(raw, stan_prod, snomed):
    raw = pd.read_csv(raw)
    stan_prod = pd.read_csv(stan_prod)
    snomed = pd.read_csv(snomed)
    return raw, stan_prod, snomed


def classify_columns(cpc, snomed_cpc_list):
    """
    eps | edaag pre snomed
    epsi | edaag pre snomed imputed to snomed
    esno | edaag snomed
    stan | stan production
    """
    if cpc in snomed_cpc_list:
        return 'ESNO'
    return 'EPS'


def set_datatypes(dataset, DATA_FEATURES):
    print()
    print('Setting datatypes')
    for feature in DATA_FEATURES.keys():
        dataset[feature] = dataset[feature].astype(DATA_FEATURES[feature])
    return dataset


def transform_features(dataset, feature_transformations):
    print()
    print('Transforming features')
    for feature in feature_transformations:
        dataset[feature] = dataset[feature].map(
            feature_transformations[feature])
    return dataset


if __name__ == '__main__':
    raw, stan_prod, snomed = load_files(
        EDAAG_RAW_PATH, STAN_PROD_PATH, SNOMED_ENCODING_PATH
    )
    raw['origin_id'] = raw.index + 1
    origin_max = raw.shape[0] + 1
    stan_prod['origin_id'] = stan_prod.index + origin_max

    snomed_cpc_list = snomed.final_encoding.unique().tolist()

    ################
    # Imputation
    ################
    raw = check_if_measured(raw)
    raw = BloodPressure_clean(raw)
    raw = null_invalid_values(raw)
    raw = impute_general_features(raw, GENERAL_FEATURE_IMPUTATION)
    raw = drop_invalid_triage_codes(raw)
    raw = calculate_patient_age(raw)
    raw = raw.reset_index(drop=True)

    # drop Notes next time raw created
    raw = raw.drop('Notes', axis=1)

    # classifiy columns and set temp id
    raw['data_class'] = raw.PresentingComplaint.apply(
        classify_columns, args=[snomed_cpc_list])

    # create null event_id + stan_triage_code columns
    raw['event_id'] = None
    raw['stan_triage_code'] = None

    # set types
    raw = set_datatypes(raw, DATA_FEATURES)

    # feature transformations 1
    raw = transform_features(raw, FEATURE_TRANSFORMATIONS_1)

    # duplicate EPS
    eps_view = raw[raw.data_class == 'EPS']
    eps_data = eps_view.copy(deep=True)

    # snomed encode...  EPS categoery changed to EPSI post imputation
    raw = snomed_encode_dataset(raw, DATA_FOLDER_PATH)
    raw = multiple_injuries_imputation(raw)
    raw['data_class'] = raw.data_class.apply(
        lambda x: 'EPSI' if x == 'EPS' else x)

    ################
    # triage framework
    ################
    raw = enforce_triage_framework_adherance(raw)

    # same triage changes to ESP as we did to ESPI...
    espi_triage_codes = pd.Series(
        raw.TriageCode.values, index=raw.origin_id
    ).to_dict()

    def apply_mapping_if_exists(row, mapping_dict):
        if row['origin_id'] in mapping_dict:
            return mapping_dict[row['origin_id']]
        return row['TriageCode']

    eps_data['TriageCode'] = eps_data.apply(
        apply_mapping_if_exists, args=[espi_triage_codes], axis=1
    )

    ################
    # concat?
    ################
    edaag = pd.concat([raw, eps_data])
    assert edaag.shape[0] == (raw.shape[0] + eps_data.shape[0])

    ################
    # create _altered columns...
    ################
    edaag['airway_altered'] = edaag.Airway.apply(impute_airway)
    edaag['breathing_altered'] = edaag.Breathing.apply(impute_breathing)
    edaag['circulation_altered'] = edaag.CirculatorySkin.apply(
        impute_circulation)
    edaag['disability_gcs'] = edaag.DisabilityValue.apply(
        impute_disability_gcs)
    edaag['neuro_altered'] = edaag.NeuroAssessment.apply(impute_neuro)
    edaag['mental_health_concerns'] = edaag.MentalHealthConcerns.apply(
        impute_mental)

    ################
    # make like TriagePresentation......
    ################
    edaag = edaag.rename(
        columns={
            'PresentDateTime': 'present_date_time',
            'DOB': 'dob',
            'AgeInMonths': 'age_in_months',
            'PresentingComplaint': 'presenting_complaint',
            'Gender': 'gender',
            'PainScale': 'pain_scale',
            'VitalSignsPulse': 'vital_signs_pulse',
            'RespiratoryRate': 'respiratory_rate',
            'BloodPressure_systolic': 'blood_pressure_systolic',
            'BloodPressure_diastolic': 'blood_pressure_diastolic',
            'Temperature': 'temperature',
            'Sats': 'sats',
            'Immunocompromised': 'immunocompromised',
            'TriageAssessment': 'triage_assessment',
            'TriageCode': 'nurse_triage_code',
            'DiagnosisDescrip': 'diagnosis'
        })

    edaag['final_nurse_code'] = None
    edaag['first_nurse_code'] = None
    edaag['final_triage_record'] = None
    edaag = edaag[TRIAGE_PRESENTION_COLS]

    # STAN prod data
    stan_prod['data_class'] = 'STAN'
    stan_prod['DOB'] = stan_prod['dob']
    stan_prod['PresentDateTime'] = stan_prod['present_date_time']
    stan_prod = calculate_patient_age(stan_prod)
    stan_prod = stan_prod.rename(columns={'AgeInMonths': 'age_in_months'})
    stan_prod['diagnosis'] = None
    stan_prod = stan_prod[TRIAGE_PRESENTION_COLS]

    ################
    # concat to final
    ################
    final = pd.concat([edaag, stan_prod])
    final = final.reset_index(drop=True)
    assert final.shape[0] == (edaag.shape[0] + stan_prod.shape[0])
    assert final.shape[1] == edaag.shape[1] == stan_prod.shape[1]

    ################
    # make target columns
    ################
    """
    'y1_triage_code',
    'y2_airway_altered',
    'y3_breathing_altered',
    'y4_circulation_altered',
    'y5_disability_altered',
    'y6_neuro_altered',
    'y7_immunocompromised',
    'y8_mental_health',
    'y9_sepsis'
    """

    final['y1_triage_code'] = final['nurse_triage_code']
    final['y2_airway_altered'] = final['airway_altered'].astype(int)
    final['y3_breathing_altered'] = final['breathing_altered'].astype(int)
    final['y4_circulation_altered'] = final['circulation_altered'].astype(int)

    def change_disability_gcs_to_altered(disability_gcs):
        if disability_gcs < 15:
            return True
        return False

    final['y5_disability_altered'] = final['disability_gcs'].astype(
        int).apply(change_disability_gcs_to_altered)
    final['y6_neuro_altered'] = final['neuro_altered'].astype(int)
    final['y7_immunocompromised'] = final['immunocompromised'].astype(int)

    def identify_mental_health(row):
        if row.presenting_complaint in MENTAL_HEALTH_CPC or row.mental_health_concerns:
            return 1
        return 0

    final['y8_mental_health'] = final.apply(identify_mental_health, axis=1)

    def identify_sepsis(diagnosis):
        if diagnosis in SEPSIS_DIAGNOSIS:
            return 1
        return 0

    final['y9_sepsis'] = final.diagnosis.apply(identify_sepsis)

    """
    FAST	Age, gender, cpc, notes
    VITAL	FAST + a vital sign taken
    FULL	FAST or VITAL + ABCD information
    """
    fast = final.copy(deep=True)
    vital = final.copy(deep=True)
    full = final.copy(deep=True)

    ################
    # fast
    ################
    cols_to_null = [x for x in TRIAGE_PRESENTION_COLS if x not in FAST_COLS]
    fast[cols_to_null] = None
    fast['data_class'] = fast['data_class'] + '_FAST'

    ################
    # vital
    ################
    def has_vital(row):
        if any([
            pd.notna(row.vital_signs_pulse),
            pd.notna(row.respiratory_rate),
            pd.notna(row.temperature),
            pd.notna(row.sats),
            pd.notna(row.blood_pressure_systolic),
            pd.notna(row.blood_pressure_diastolic)
        ]):
            return True
        return False

    vital['has_vital'] = vital.apply(has_vital, axis=1)
    vital = vital[vital.has_vital]
    cols_to_null = [x for x in TRIAGE_PRESENTION_COLS if x not in VITAL_COLS]
    vital = vital.drop('has_vital', axis=1)
    vital[cols_to_null] = None
    vital['data_class'] = vital['data_class'] + '_VITAL'

    ################
    # full
    ################
    def has_abcd(row):
        if any([
            (row.airway_altered),
            (row.breathing_altered),
            (row.circulation_altered),
            (row.disability_gcs < 15),
            (row.neuro_altered),
            pd.notna(row.pain_scale),
            (row.immunocompromised)
        ]):
            return True
        return False

    full['has_abcd'] = full.apply(has_abcd, axis=1)
    full = full[full.has_abcd]
    full = full.drop('has_abcd', axis=1)
    full['data_class'] = full['data_class'] + '_FULL'

    processed = pd.concat([fast, vital, full]).reset_index(drop=True)
    assert processed.shape[0] == (fast.shape[0] + vital.shape[0] + full.shape[0])

    processed['X'] = processed.apply(lambda x: generate_stan_sequence(x), axis=1)
    processed.to_csv(str(Path(DATA_FOLDER_PATH, CLEAN_FILENAME)), index=False)

    import pdb; pdb.set_trace()
    
    processed = processed[processed.final_triage_record != False]
    train = processed[['origin_id', 'data_class', 'X']+TARGET_COLS]

    ################
    # do index wizardry to create good general test set...
    ################
    train['test_set'] = False
    train.loc[train.origin_id % (1/TEST_SET_SIZE) == 0, 'test_set'] = True

    print('\nTrain set size: {}\nTest set size: {}'.format(
        train[~train.test_set].shape, train[train.test_set].shape
    ))

    train.to_csv(str(Path(DATA_FOLDER_PATH, TRAIN_FILENAME)), index=False)

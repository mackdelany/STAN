import datetime
import re
from dateutil.relativedelta import relativedelta

import numpy as np
import pandas as pd


def sample_from_gaussian(mean, sigma, sig_fig):
    return round(np.random.normal(mean, sigma), sig_fig)


def impute_features(dataset, GENERAL_FEATURE_IMPUTATION, VITAL_SIGN_IMPUTATION, random_seed=69):
    print()
    print('Mapping nulls')
    print('Shape before mapping: {}'.format(dataset.shape))
    print('Setting random seed to {}'.format(random_seed))
    np.random.seed(69)

    dataset = check_if_features_measured_prior_to_mapping(dataset)
    dataset = BloodPressure_clean(dataset)
    dataset = null_invalid_values(dataset)
    dataset = impute_general_features(dataset, GENERAL_FEATURE_IMPUTATION)
    dataset = drop_invalid_triage_codes(dataset)
    dataset = calculate_patient_age(dataset)
    dataset = impute_vital_signs(dataset, VITAL_SIGN_IMPUTATION)
    dataset = dataset.reset_index(drop=True)

    print('Shape after mapping: {}'.format(dataset.shape))
    return dataset


def check_if_measured(dataset):
    print('Checking if features were measured\n')

    features_to_check = ['Airway', 'Breathing', 'CirculatorySkin', 'DisabilityValue', 
                        'NeuroAssessment', 'PainScale', 'MentalHealthConcerns', 
                        'BloodPressure', 'Temperature', 'Sats', 'Immunocompromised',
                        'RespiratoryRate', 'VitalSignsPulse'] ## Note these two get overwritten later 

    def check_for_value(cell):
        if pd.isna(cell) | (cell == ''):
            return 0
        else :
            return 1

    for feature in features_to_check:
        
        dataset[(feature + '_was_measured')] = dataset[feature].apply(check_for_value)

    return dataset


def BloodPressure_clean(dataset):
    dataset['BloodPressure'] = dataset['BloodPressure'].fillna('')
    dataset['BloodPressure'] = dataset['BloodPressure'].astype(str)

    def split_blood_pressure_systolic(pressure):
        return pressure.split('/')[0]
    def split_blood_pressure_diastolic(pressure):
        try :
            return pressure.split('/')[1]
        except :
            return '0'
    def remove_non_numbers(pressure):
        return re.sub('[^0-9]','', pressure)

    dataset['BloodPressure_systolic'] = dataset['BloodPressure'].apply(split_blood_pressure_systolic)
    dataset['BloodPressure_systolic'] = dataset['BloodPressure_systolic'].apply(remove_non_numbers)

    dataset['BloodPressure_diastolic'] = dataset['BloodPressure'].apply(split_blood_pressure_diastolic)
    dataset['BloodPressure_diastolic'] = dataset['BloodPressure_diastolic'].apply(remove_non_numbers)

    dataset['BloodPressure_systolic'] = dataset['BloodPressure_systolic'].apply(lambda x: '0' if x == '' else x)
    dataset['BloodPressure_diastolic'] = dataset['BloodPressure_diastolic'].apply(lambda x: '0' if x == '' else x)

    dataset = dataset.astype({'BloodPressure_systolic': 'int64', 'BloodPressure_diastolic': 'int64'})

    return dataset


def null_invalid_values(dataset):
    print('Nulling invalid values\n')

    def null_invalid_blood_pressure_systolic(row):
        if (row['BloodPressure_systolic'] < 30) | (row['BloodPressure_systolic'] > 300) | \
            pd.isna(row['BloodPressure_systolic']) | (row['BloodPressure_systolic'] == 'nan'):
            return None
        else :
            return row['BloodPressure_systolic']

    def null_invalid_blood_pressure_diastolic(row):
        if (row['BloodPressure_diastolic'] < 10) | (row['BloodPressure_diastolic'] > 170) | \
            pd.isna(row['BloodPressure_diastolic']) | (row['BloodPressure_diastolic'] == 'nan'):
            return None
        else :
            return row['BloodPressure_diastolic']

    def null_invalid_vital_signs_pulse(row):
        if (row['VitalSignsPulse'] <= 24) | (row['VitalSignsPulse'] > 208) | \
            pd.isna(row['VitalSignsPulse']) | (row['VitalSignsPulse'] == 'nan'):
            return None
        else :
            return row['VitalSignsPulse']

    def null_invalid_respiratory_rate(row):
        if (row['RespiratoryRate'] < 7) | (row['RespiratoryRate'] > 80) | \
            pd.isna(row['RespiratoryRate']) | (row['RespiratoryRate'] == 'nan'):
            return None
        else :
            return row['RespiratoryRate']

    def null_invalid_temperature(row):
        if (row['Temperature'] < 30) | (row['Temperature'] > 44) | \
            pd.isna(row['Temperature']) | (row['Temperature'] == 'nan'):
            return None
        else :
            return row['Temperature']

    def null_invalid_sats(row):
        if (row['Sats'] > 100) | (row['Sats'] < 60):
            return None
        else :
            return row['Sats']

    
    dataset['BloodPressure_systolic'] = dataset.apply(null_invalid_blood_pressure_systolic, axis=1)
    dataset['BloodPressure_diastolic'] = dataset.apply(null_invalid_blood_pressure_diastolic, axis=1)
    dataset['VitalSignsPulse'] = dataset.apply(null_invalid_vital_signs_pulse, axis=1)
    dataset['RespiratoryRate'] = dataset.apply(null_invalid_respiratory_rate, axis=1)
    dataset['Temperature'] = dataset.apply(null_invalid_temperature, axis=1)
    dataset['Sats'] = dataset.apply(null_invalid_sats, axis=1)

    return dataset


def impute_general_features(dataset, GENERAL_FEATURE_IMPUTATION):
    print('Imputing general features\n')
    
    for feature in GENERAL_FEATURE_IMPUTATION:

        if feature in dataset.columns:

            if GENERAL_FEATURE_IMPUTATION[feature] == 'DROP':
                dataset = dataset.dropna(subset = [feature])

            elif GENERAL_FEATURE_IMPUTATION[feature] == 'ZEROS':
                dataset[feature] = dataset[feature].fillna(value=0)

            elif GENERAL_FEATURE_IMPUTATION[feature] == 'MEAN':
                dataset[feature] = dataset[feature].fillna(value=dataset[feature].mean())

            elif callable(GENERAL_FEATURE_IMPUTATION[feature]):
                dataset[feature] = mappings_for_nulls[feature](dataset)

            else :
                fill_value = GENERAL_FEATURE_IMPUTATION[feature]
                dataset[feature].fillna(value=fill_value, inplace=True)

    return dataset


def drop_invalid_triage_codes(dataset):

    dataset = dataset[dataset['TriageCode'] >= 1]
    dataset = dataset[dataset['TriageCode'] <= 5]

    dataset = dataset.reset_index(drop=True)

    return dataset


def calculate_patient_age(dataset):

    dataset['DOB'] = pd.to_datetime(dataset['DOB'])
    dataset['PresentDateTime'] = pd.to_datetime(dataset['PresentDateTime'])

    def get_age_in_month(row):
        return (relativedelta(row['PresentDateTime'], row['DOB']).years * 12) + (relativedelta(row['PresentDateTime'], row['DOB']).months)

    dataset['AgeInMonths'] = dataset.apply(get_age_in_month, axis=1)        

    return dataset


def impute_vital_signs(dataset, VITAL_SIGN_IMPUTATION):
    print('Imputing vital signs\n')

    dataset['Temperature'] = dataset['Temperature'].apply(impute_temperature)
    dataset['BloodPressure_diastolic'] = dataset['BloodPressure_systolic'].apply(impute_blood_pressure_diastolic)
    dataset['Sats'] = dataset['Sats'].apply(impute_sats)

    dataset['VitalSignsPulse'] = dataset.apply(impute_vital_signs_pulse, axis=1)
    dataset['RespiratoryRate'] = dataset.apply(impute_respiratory_rate, axis=1)
    dataset['BloodPressure_systolic'] = dataset.apply(impute_blood_pressure_systolic, axis=1)

    dataset['Sats'] = dataset['Sats'].apply(lambda x: x if x <= 100 else 99)

    return dataset





def impute_temperature(temperature):
    if (not pd.isna(temperature)):
        return temperature
    else :
        return sample_from_gaussian(37, 0.2, 1)

def impute_blood_pressure_diastolic(blood_pressure_diastolic):
    if (not pd.isna(blood_pressure_diastolic)):
        return blood_pressure_diastolic
    else :
        return sample_from_gaussian(70, 5, 0)

def impute_sats(sats):
    if (not pd.isna(sats)):
        return sats
    else :
        return sample_from_gaussian(97.5, 1, 1)


def impute_blood_pressure_systolic(row):
    if (row['BloodPressure_systolic'] < 30) | \
        (row['BloodPressure_systolic'] > 300) | \
        (pd.isna(row['BloodPressure_systolic'])):

        if row['AgeInMonths'] < 12:
            return sample_from_gaussian(100, 5, 0)
        elif row['AgeInMonths'] < (5*12):
            return sample_from_gaussian(100, 5, 0)
        elif row['AgeInMonths'] < (12*12):
            return sample_from_gaussian(105, 5, 0)
        elif row['AgeInMonths'] < (16*12):
            return sample_from_gaussian(115, 5, 0)
        else :
            return sample_from_gaussian(135, 5, 0)

    else :
        return row['BloodPressure_systolic']



def impute_vital_signs_pulse(row):
    if (row['VitalSignsPulse'] <= 24) | \
        (row['VitalSignsPulse'] > 205) | \
        (pd.isna(row['VitalSignsPulse'])):

        if row['AgeInMonths'] < 12:
            return sample_from_gaussian(130, 5, 0)
        elif row['AgeInMonths'] < (5*12):
            return sample_from_gaussian(115, 5, 0)
        elif row['AgeInMonths'] < (12*12):
            return sample_from_gaussian(105, 5, 0)
        elif row['AgeInMonths'] < (16*12):
            return sample_from_gaussian(85, 5, 0)
        else :
            return sample_from_gaussian(75, 5, 0)

    else :
        return row['VitalSignsPulse']


def impute_respiratory_rate(row):
    if (row['RespiratoryRate'] < 7) | \
        (row['RespiratoryRate'] > 80) | \
        (pd.isna(row['RespiratoryRate'])) :
        
        if row['AgeInMonths'] <= 3:
            return sample_from_gaussian(45, 2, 0)
        elif row['AgeInMonths'] < 12:
            return sample_from_gaussian(32.5, 2, 0)
        elif row['AgeInMonths'] < (5*12):
            return sample_from_gaussian(25, 2, 0)
        elif row['AgeInMonths'] < (12*12):
            return sample_from_gaussian(25.5, 2, 0)
        elif row['AgeInMonths'] < (17*12):
            return sample_from_gaussian(20, 2, 0)
        else :
            return sample_from_gaussian(16, 2, 0)

    else :
        return row['RespiratoryRate']


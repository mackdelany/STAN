import time
import datetime
import json
from pathlib import Path
from joblib import dump

import numpy as np 
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

from custom_functions import encode_cyclical_time_of_day, mean_triage_code, add_cpc_groupings, \
    identify_and_save_cpc_variance

from data_parameters import TARGET_FEATURE, DATA_FEATURES,\
    FEATURE_TRANSFORMATIONS_1, FEATURE_TRANSFORMATIONS_2, CPC_CATEGORY_INDICES, \
    CPC_CATEGORIES, CUSTOM_FUNCTIONS_TO_BE_RUN, FINAL_FEATURES, \
    FEATURES_TO_HOT_ENCODE, VITAL_SIGN_IMPUTATION, GENERAL_FEATURE_IMPUTATION

from early_warning_score import add_ews_to_dataset

from encode_cpc import hot_encode 

from imputation import impute_features

from triage_framework import enforce_triage_framework_adherance

from production_data import imitate_raw_data

from snomed_encode import multiple_injuries_imputation, snomed_encode_dataset


def clean_and_return_dataset(filename, path_to_data, mapping_path, snomed_encode=True, snomed_name='snomed_encoding.csv'):
    dataset = process_dataset(filename, path_to_data, mapping_path, snomed_encode=snomed_encode, snomed_name=snomed_name)
    dataset_name = 'stan_clean_{}.csv'.format(datetime.datetime.today().strftime('%d_%m_%y'))
    dataset.to_csv(Path(path_to_data, dataset_name), encoding='utf-8', index=False)
    print('Saved to {}'.format(path_to_data))

    """
    Delete the below once tested
    """
    dataset['PainScale'] = dataset['PainScale'].map({
        0.0: 0.0,
        1.0: 0.0,
        2.0: 3.0,
        3.0: 3.0,
        4.0: 3.0,
        5.0: 6.0,
        6.0: 6.0,
        7.0: 6.0,
        8.0: 9.0,
        9.0: 9.0,
        10.0: 9.0
        })
    dataset_name = 'stan_clean_pain_binned_{}.csv'.format(datetime.datetime.today().strftime('%d_%m_%y'))
    dataset.to_csv(Path(path_to_data, dataset_name), encoding='utf-8', index=False)
    print('Saved to {}'.format(path_to_data))


def process_dataset(filename, path_to_data, mapping_path, set_feature_dict=True, feature_dict_name='feature_mappings.txt', snomed_encode=True, snomed_name='snomed_encoding.csv'):
    dataset = load_data(path_to_data, filename)
    dataset = impute_features(dataset, GENERAL_FEATURE_IMPUTATION, VITAL_SIGN_IMPUTATION)
    if snomed_encode:
        dataset = snomed_encode_dataset(dataset, mapping_path, snomed_name)
        dataset = multiple_injuries_imputation(dataset)

    dataset = set_datatypes(dataset, DATA_FEATURES, TARGET_FEATURE)
    dataset = transform_features(dataset, FEATURE_TRANSFORMATIONS_1)
    dataset = custom_functions(dataset, CUSTOM_FUNCTIONS_TO_BE_RUN)
    dataset = enforce_triage_framework_adherance(dataset)
    dataset = add_ews_to_dataset(dataset)
    dataset = transform_features(dataset, FEATURE_TRANSFORMATIONS_2)   
    dataset = dataset[FINAL_FEATURES]
    dataset = hot_encode_features(dataset, FEATURES_TO_HOT_ENCODE)

    print('dataset has ' + str(dataset.isna().sum().sum()) + ' null values after processing')
    print('dataset shape: ' + str(dataset.shape))

    dataset = dataset.drop(columns=["Airway_was_measured", 
                                    "Breathing_was_measured", 
                                    "CirculatorySkin_was_measured", 
                                    "DisabilityValue_was_measured", 
                                    'NeuroAssessment_was_measured', 
                                    'PainScale_was_measured',
                                    "MentalHealthConcerns_was_measured",
                                    "Immunocompromised_was_measured"])

    feature_dict = create_feature_dict(dataset)
    with open(Path(mapping_path, (feature_dict_name)), 'w+') as json_file:
        json.dump(feature_dict, json_file)

    return dataset


def load_data(path_to_data, filename, additional_data=True, additional_data_filename='nz_triage_course_data.csv', production_data=True):
    print()
    print('Loading data')
    dataset = pd.read_csv(Path(path_to_data, filename))
    if additional_data:
        additional_data = pd.read_csv(Path(path_to_data, additional_data_filename))
        dataset = pd.concat([dataset, additional_data]).sort_values(by='PresentDateTime', ascending=True).reset_index(drop=True)
    if production_data:
        prod_data_path = input("Production data filename?\n")
        prod_data = pd.read_csv(Path(path_to_data, prod_data_path))
        prod_data_raw_encoded = imitate_raw_data(prod_data)
        dataset = pd.concat([dataset, prod_data_raw_encoded]).sort_values(by='PresentDateTime', ascending=True).reset_index(drop=True)

    return dataset


def set_datatypes(dataset, DATA_FEATURES, TARGET_FEATURE):
    print()
    print('Setting datatypes')
    for feature in DATA_FEATURES.keys():
        dataset[feature] = dataset[feature].astype(DATA_FEATURES[feature])

    for feature in TARGET_FEATURE.keys():
        dataset[feature] = dataset[feature].astype(TARGET_FEATURE[feature])
    return dataset


def transform_features(dataset, feature_transformations):
    print()
    print('Transforming features')
    for feature in feature_transformations:
        dataset[feature] = dataset[feature].map(feature_transformations[feature])
    return dataset


def custom_functions(dataset, CUSTOM_FUNCTIONS_TO_BE_RUN):
    print()
    print('Executing custom functions')
    for custom_function in CUSTOM_FUNCTIONS_TO_BE_RUN:
        print('Running {}'.format(custom_function))
        if (CUSTOM_FUNCTIONS_TO_BE_RUN[custom_function]) == 'NO ADDITIONAL ARGUMENTS':
            dataset = custom_function(dataset)
        else:
            dataset = custom_function(dataset, CUSTOM_FUNCTIONS_TO_BE_RUN[custom_function])
    return dataset




def create_feature_dict(dataset):
    feature_dict = {}
    feature_set = dataset.drop(list(TARGET_FEATURE.keys()), axis=1)
    for column in feature_set.columns:
        feature_dict[column] = feature_set.columns.get_loc(column)
    return feature_dict


def encode_presenting_complaint(dataset, mapping_path):
    dataset = create_cpc_encodings(dataset, mapping_path)
    dataset = encode_presenting_complaints(dataset, mapping_path)
    return dataset


def hot_encode_features(dataset, FEATURES_TO_HOT_ENCODE):
    dataset = hot_encode(dataset, FEATURES_TO_HOT_ENCODE)
    return dataset


def process_dataset_for_seq(path_to_data, filename, mapping_path, set_feature_dict=True, feature_dict_name='feature_mappings.txt', snomed_encode=True, snomed_name='snomed_encoding.csv'):
    dataset = load_data(path_to_data, filename, production_data=False)
    dataset = impute_features(dataset, GENERAL_FEATURE_IMPUTATION, VITAL_SIGN_IMPUTATION)
    if snomed_encode:
        dataset = snomed_encode_dataset(dataset, mapping_path, snomed_name)
        dataset = multiple_injuries_imputation(dataset)

    dataset = set_datatypes(dataset, DATA_FEATURES, TARGET_FEATURE)
    dataset = transform_features(dataset, FEATURE_TRANSFORMATIONS_1)
    dataset = custom_functions(dataset, CUSTOM_FUNCTIONS_TO_BE_RUN)
    dataset = enforce_triage_framework_adherance(dataset)
    #dataset = add_ews_to_dataset(dataset) may need... not right now

    return dataset


if __name__ == '__main__':
    start_time = time.time()
    data_path = str(Path.cwd().parent) + '/data/'
    mapping_path = str(Path.cwd().parent) + '/mappings/'
    clean_and_return_dataset('raw.csv', data_path, mapping_path)
    print()
    print('Total processing time: {} minutes'.format((time.time() - start_time)/60))


import datetime
from dateutil.relativedelta import relativedelta
import re
import json
import logging
from pathlib import Path

from sklearn.utils import resample
import pandas as pd
import numpy as np


def identify_and_save_cpc_variance(dataset):
    cpc_variance = dataset.groupby('PresentingComplaint').std()['TriageCode'].to_dict()

    with open(Path('/Users/mackdelany/Documents/STAN/stan_model/mappings', 'cpc_variance.txt'), 'w+') as json_file:
        json.dump(cpc_variance, json_file)

    return dataset

def encode_cyclical_time_of_day(dataset, PresentDateTime):
    dataset['hour_of_day'] = pd.to_datetime(dataset[PresentDateTime]).dt.hour
    dataset['hour_sin'] = np.sin(2 * np.pi * dataset['hour_of_day']/23.0)
    dataset['hour_cos'] = np.cos(2 * np.pi * dataset['hour_of_day']/23.0)
    dataset = dataset.drop(columns=['hour_of_day'])
    return dataset

def save_pain_scale_dict(dataset, pain_scale_dict_path='/Users/mackdelany/Documents/STAN/stan_model/mappings'):
    pain_scale_dict = dataset.groupby('PresentingComplaint')['PainScale'].mean().fillna(5).to_dict()

    with open(Path(pain_scale_dict_path, 'pain_scale_dict.txt'), 'w+') as json_file:
        json.dump(pain_scale_dict, json_file)

    return dataset

def mean_triage_code(dataset, mapping_path='/Users/mackdelany/Documents/STAN/stan_model/mappings' , mean_triage_name='cpc_mean_triage_code.txt'):
    mean_triage_code_dict = dataset.groupby('PresentingComplaint').mean()['TriageCode'].to_dict()

    with open(Path(mapping_path, mean_triage_name), 'w+') as json_file:
        json.dump(mean_triage_code_dict, json_file)

    def insert_mean_triage_code(cpc):
        return mean_triage_code_dict[cpc]

    dataset['mean_triage_code'] = dataset['PresentingComplaint'].apply(insert_mean_triage_code)

    return dataset

def add_cpc_groupings(dataset, cpc_info_list):

    CPC_CATEGORIES = cpc_info_list[0]
    CPC_CATEGORY_INDICES = cpc_info_list[1]
    mapping_path = cpc_info_list[2]
    CPC_CATEGORIES_name = cpc_info_list[3]
    CPC_CATEGORY_INDICES_name = cpc_info_list[4]

    with open(Path(mapping_path, CPC_CATEGORIES_name), 'w+') as json_file:
        json.dump(CPC_CATEGORIES, json_file)

    with open(Path(mapping_path, CPC_CATEGORY_INDICES_name), 'w+') as json_file:
        json.dump(CPC_CATEGORY_INDICES, json_file)

    def apply_CPC_CATEGORIES(cpc):
        #return CPC_CATEGORY_INDICES[CPC_CATEGORIES[cpc]]
        return CPC_CATEGORIES[cpc]

    dataset['PresentingComplaintGroup'] = dataset['PresentingComplaint'].apply(apply_CPC_CATEGORIES)

    return dataset


def fill_pain_scale_na_with_cpc_mean(dataset):
    pain_scale = (dataset['PainScale'].fillna(dataset.
                 groupby('PresentingComplaint')['PainScale'].transform("mean")))
    pain_scale = pain_scale.fillna(3)
    return pain_scale









    


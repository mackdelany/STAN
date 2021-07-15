import json
from pathlib import Path

import pandas as pd


def create_cpc_encodings(dataset, mapping_path, cpc_encoding_name='cpc_encodings.txt'):

    cpcs = dataset.groupby('PresentingComplaint').mean()['TriageCode'].sort_values().index

    cpc_encoding = {}
    numeric = 0

    for cpc in cpcs:
        cpc_encoding.update({cpc : numeric})
        numeric += 1 

    with open(Path(mapping_path, cpc_encoding_name), 'w+') as json_file:
        json.dump(cpc_encoding, json_file)

    return dataset


def encode_presenting_complaints(dataset, mapping_path, cpc_encoding_name='cpc_encodings.txt'):

    with open(Path(mapping_path, cpc_encoding_name)) as json_file:
        cpc_encoding = json.load(json_file)

    def apply_cpc_encoding(cpc):
        return cpc_encoding[cpc]

    dataset['PresentingComplaint'] = dataset['PresentingComplaint'].apply(apply_cpc_encoding)

    return dataset



def hot_encode(dataset, FEATURES_TO_HOT_ENCODE):
    """Hot encode chosen features using a preset mapping
    Keyword arguments:
    dataset -- DataFrame to operate on
    FEATURES_TO_HOT_ENCODE -- List of features to be hot encoded
    """
    for feature in FEATURES_TO_HOT_ENCODE:
        dummies = pd.get_dummies(dataset[feature])
        dataset.reset_index(drop=True, inplace=True)
        dummies.reset_index(drop=True, inplace=True)
        dataset = pd.concat([dummies, dataset],axis=1, sort=False)
        dataset = dataset.drop(feature, axis=1)
    return dataset

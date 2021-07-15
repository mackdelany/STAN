import pandas as pd

def snomed_encode_dataset(dataset, mapping_path, snomed_name='snomed_encoding.csv'):
    print()
    print('SNOMED Encoding PresentingComplaints circa 2018')
    print('Shape before encoding: {}'.format(dataset.shape))

    dataset['PresentingComplaint'] = dataset['PresentingComplaint'].astype(str)

    path_to_encodings = mapping_path + snomed_name
    snomed_encodings = pd.read_csv(path_to_encodings, index_col='edaag_entry')

    snomed_conversions = {}

    for index, row in snomed_encodings.iterrows():
        snomed_conversions.update({index.lower():row['final_encoding']})

    def snomed_encode_cpc(cpc, args=(snomed_conversions)):
        if (cpc == 'nan') | (pd.isna(cpc)):
            return 'DROP_NAN'
        try :
            return snomed_conversions[cpc.lower()]
        except KeyError:
            return 'DROP_NO_ENCODING_SUITABLE'

    dataset['PresentingComplaint'] = dataset['PresentingComplaint'].apply(snomed_encode_cpc, args=(snomed_conversions, ))

    print('{} nans / nulls replaced'.format(dataset[dataset['PresentingComplaint'] == 'DROP_NAN'].shape[0]))
    print('{} unable to be encoded'.format(dataset[dataset['PresentingComplaint'] == 'DROP_NO_ENCODING_SUITABLE'].shape[0]))

    dataset = dataset[dataset['PresentingComplaint'] != 'DROP_NAN']
    dataset = dataset[dataset['PresentingComplaint'] != 'DROP_NO_ENCODING_SUITABLE']

    dataset = dataset.dropna(subset=['PresentingComplaint'])

    print('Shape after encoding: {}'.format(dataset.shape))

    return dataset


def multiple_injuries_imputation(dataset):

    def identify_injury_severity(row):
        if row['PresentingComplaint'] == 'Multiple injuries - ROZZA':
            if row['PainScale'] > 6 :
                return 'Multiple injuries - major'
            elif row['TriageCode'] <= 2:
                return 'Multiple injuries - major'
            else :
                return 'Multiple injuries - minor'
        else :
            return row['PresentingComplaint']
    
    dataset['PresentingComplaint'] = dataset.apply(identify_injury_severity, axis=1)

    print('Unique presenting complaints in dataset: {}'.format(dataset.PresentingComplaint.unique().shape[0]))

    return dataset
    

import pandas as pd
from stan.core.stan_sequence_util import generate_stan_sequence

#from data_parameters import FEATURE_TRANSFORMATIONS_1, GENERAL_FEATURE_IMPUTATION, VITAL_SIGN_IMPUTATION
from data_processing import *
from imputation import impute_features
from triage_presentation import TriagePresentation


"""
Sequence = long string of words with spaces between them... all lower case ? 

X | Age y/o gender with CPC. Airway breathing circulation disability. Vital signs. Pain scale. Immunocompromised. Mental health.
Y | Triage code

Current prod data: STAN_PROD_DATA_03_10_20.csv
"""

PATH_TO_RAW = '/Users/mackdelany/Documents/STAN/stan_model/data/'
RAW_FILENAME = 'raw.csv'

class RawSTANDataToSequence():

    def __init__(self, raw_path, raw_file, mapping_path):
        self.raw_path = raw_path
        self.raw_file = raw_file
        self.mapping_path = mapping_path
        self.req_col = ['DOB', 'PresentDateTime', 'PresentingComplaint']
        self.sequence_col = ['presentation', 'triage_code']

    def load_data(self):
        self.raw = process_dataset_for_seq(self.raw_path, self.raw_file, self.mapping_path)

    def generate_sequences(self):
        sequence_data = []
        for raw in self.raw.itertuples():
            event = RawSTANDataToSequence.raw_tuple_to_triage_presentation(raw)
            sequence_data.append([
                generate_stan_sequence(event),   # sequence
                raw.TriageCode                 # triage_code
                ])
        self.sequences = pd.DataFrame(sequence_data, columns=self.sequence_col)

    @staticmethod
    def raw_tuple_to_triage_presentation(raw):
        presentation = TriagePresentation(
            present_date_time=raw.PresentDateTime, 
            dob=raw.DOB, 
            age_in_months=raw.AgeInMonths,
            presenting_complaint=raw.PresentingComplaint,
            gender=raw.Gender,
            airway=raw.Airway,
            breathing=raw.Breathing,
            circulatory_skin=raw.CirculatorySkin,
            disability_value=raw.DisabilityValue,
            neuro_assessment=raw.NeuroAssessment,
            pain_scale=raw.PainScale,
            vital_signs_pulse=raw.VitalSignsPulse,
            respiratory_rate=raw.RespiratoryRate,
            blood_pressure_systolic=raw.BloodPressure_systolic,
            blood_pressure_diastolic=raw.BloodPressure_diastolic,
            temperature=raw.Temperature,
            sats=raw.Sats,
            mental_health_concerns=raw.MentalHealthConcerns,
            immunocompromised=raw.Immunocompromised,
            triage_assessment=raw.TriageAssessment
            )
        return presentation
        


if __name__ == '__main__':
    mapping_path = str(Path.cwd().parent) + '/mappings/'
    data_converter = RawSTANDataToSequence(PATH_TO_RAW, RAW_FILENAME, mapping_path)
    data_converter.load_data()
    #data_converter.raw = pd.read_csv('raw_for_seq.csv')
    data_converter.generate_sequences()
    for _ in range(25):
        print(data_converter.sequences.sample(1)['presentation'])
    data_converter.sequences.to_csv('stan_sequences.csv', index=False)
    

import sys

import pandas as pd

sys.path.insert(0, '/Users/mackdelany/Documents/STAN/triage_prediction_api/')

from api.ews.early_warning_score import EarlyWarningScore
from api.exceptions import InvalidOptionalFieldError, UnknownEarlyWarningScoreTypeError



def add_ews_to_dataset(dataset):

    print()
    print('Adding early warning signs to dataset')
    print()

    for triage_event in dataset.itertuples():

        if triage_event.Index % 10000 == 0:
            print('{} rows completed'.format(triage_event.Index))

        ews_framework = EarlyWarningScore()

        ews_framework.presenting_complaint = triage_event.PresentingComplaint
        ews_framework.airway = triage_event.Airway
        ews_framework.breathing = triage_event.Breathing
        ews_framework.circulatory_skin = triage_event.CirculatorySkin
        ews_framework.disability_value = triage_event.DisabilityValue
        ews_framework.respiratory_rate = triage_event.RespiratoryRate
        ews_framework.vital_signs_pulse = triage_event.VitalSignsPulse
        ews_framework.temperature = triage_event.Temperature
        ews_framework.sats = triage_event.Sats
        ews_framework.blood_pressure_systolic = triage_event.BloodPressure_systolic
        ews_framework.blood_pressure_diastolic = triage_event.BloodPressure_diastolic
        ews_framework.age_in_months = triage_event.AgeInMonths

        ews_framework.estimate_adult_early_warning_score()

        dataset.loc[triage_event.Index, 'ews_type'] = ews_framework.early_warning_score_type
        dataset.loc[triage_event.Index, 'ews_emergency_zone'] = int(ews_framework.ews_red_zone) + int(ews_framework.ews_blue_zone)
        dataset.loc[triage_event.Index, 'ews_estimate'] = ews_framework.early_warning_score_estimated

        dataset.loc[triage_event.Index, 'respiratory_rate_ews'] = ews_framework.respiratory_rate_ews
        dataset.loc[triage_event.Index, 'respiratory_distress_ews'] = ews_framework.respiratory_distress_ews
        dataset.loc[triage_event.Index, 'sats_ews'] = ews_framework.sats_ews
        dataset.loc[triage_event.Index, 'vital_signs_pulse_ews'] = ews_framework.vital_signs_pulse_ews
        dataset.loc[triage_event.Index, 'capillary_refill_ews'] = ews_framework.capillary_refill_ews
        dataset.loc[triage_event.Index, 'blood_pressure_systolic_ews'] = ews_framework.blood_pressure_systolic_ews
        dataset.loc[triage_event.Index, 'blood_pressure_diastolic_ews'] = ews_framework.blood_pressure_diastolic_ews
        dataset.loc[triage_event.Index, 'temperature_ews'] = ews_framework.temperature_ews
        dataset.loc[triage_event.Index, 'disability_value_ews'] = ews_framework.disability_value_ews

    print()
    print('Early warning signs added to dataset')
    print()

    return dataset

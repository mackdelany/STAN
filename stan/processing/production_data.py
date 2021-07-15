from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from pytz import timezone
from sqlalchemy import create_engine

from .data_parameters import STAN_DATABASE_URI, PRODUCTION_DHB, RAW_COLUMNS


def query_stan_database(STAN_DATABASE_URI):
    print('\nQuerying triage event table\n')
    engine = create_engine(STAN_DATABASE_URI)
    table = pd.read_sql('triageevent', engine)
    return table


def filter_production_data(table, PRODUCTION_DHB):
    table = table[(table.dhb_id == PRODUCTION_DHB)]
    table = table[(table.method == 'RECORD') | (table.method == 'PREDICT')]
    return table


def convert_timezones_to_nzt(table):
    print("Converting timezones\n")
    table['present_date_time'] = pd.to_datetime(table['present_date_time'])
    table['present_date_time'] = table['present_date_time'].apply(
        lambda x: x.tz_convert(timezone('Pacific/Auckland')).tz_convert(None))
    table['dob'] = table['dob'].apply(lambda x: x.tz_convert(
        timezone('Pacific/Auckland')).tz_convert(None))
    return table


def assign_final_triage_records(table):
    print('Assigning final triage records for events\n')
    table['final_triage_record'] = False
    for event in table.event_id.unique():
        first_nurse_code = table[table.event_id == event].sort_values(
            'present_date_time', ascending=True).head(1).nurse_triage_code.values[0]
        final_nurse_code = table[table.event_id == event].sort_values(
            'present_date_time', ascending=True).tail(1).nurse_triage_code.values[0]
        first_stan_code = table[table.event_id == event].sort_values(
            'present_date_time', ascending=True).head(1).stan_triage_code.values[0]
        final_stan_code = table[table.event_id == event].sort_values(
            'present_date_time', ascending=True).tail(1).stan_triage_code.values[0]
        final_record_idx = table[table.event_id == event].sort_values(
            'present_date_time', ascending=True).tail(1).index[0]
        table.loc[final_record_idx, 'final_triage_record'] = True
        table.loc[table.event_id == event,
                  'first_nurse_code'] = first_nurse_code
        table.loc[table.event_id == event,
                  'final_nurse_code'] = final_nurse_code
        table.loc[table.event_id == event, 'first_stan_code'] = first_stan_code
        table.loc[table.event_id == event, 'final_stan_code'] = final_stan_code
    return table


def imitate_raw_data(table):
    table = table[table.final_triage_record == True]
    print('Adding {} records from production to training set'.format(
        table.shape[0]))
    table_raw_encoded = pd.DataFrame(columns=RAW_COLUMNS)

    for row in table.itertuples():
        if row.blood_pressure_was_measured:
            blood_pressure = '{}/{}'.format(row.blood_pressure_systolic,
                                            row.blood_pressure_diastolic)
        else:
            blood_pressure = None

        table_raw_encoded = table_raw_encoded.append({
            'ID': None,
            'DOB': row.dob,
            'Gender': row.gender,
            'PresentingComplaint': row.presenting_complaint,
            'PresentDateTime': row.present_date_time,
            'TriageDateTime': None,
            'PhysicalDischarge': None,
            'Airway': row.airway if row.airway_was_measured else None,
            'Breathing': row.breathing,
            'NeuroAssessment': row.neuro_assessment if row.neuro_assessment else None,
            'PainScale': row.pain_scale if row.pain_scale_was_measured else np.nan,
            'CirculatorySkin': row.circulatory_skin if row.circulatory_skin_was_measured else None,
            'MentalHealthConcerns': row.mental_health_concerns if row.mental_health_concerns_was_measured else None,
            'VitalSignsPulse': row.vital_signs_pulse if row.vital_signs_pulse_was_measured else np.nan,
            'RespiratoryRate': row.respiratory_rate if row.respiratory_rate_was_measured else np.nan,
            'DisabilityValue': row.disability_value if row.disability_value_was_measured else None,
            'BloodPressure': blood_pressure,
            'Temperature': row.temperature if row.temperature_was_measured else np.nan,
            'Sats': row.sats if row.sats_was_measured else np.nan,
            'Immunocompromised': row.immunocompromised if row.immunocompromised_was_measured else np.nan,
            'TriageCode': row.nurse_triage_code,
            'StanTriageCode': row.stan_triage_code
        }, ignore_index=True
        )

    return table_raw_encoded


def group_triage_events(table, time_window=(30*60)):
    print('Grouping triage events\n')

    table['triage_id'] = -1
    triage_id = 0

    for idx in table.index:
        if table.loc[idx, 'triage_id'] == -1:
            table.loc[((table.dob == table.loc[idx, 'dob']) &
                       (table.presenting_complaint == table.loc[idx, 'presenting_complaint']) &
                       (table.gender == table.loc[idx, 'gender']) &
                       ((table.present_date_time - table.loc[idx, 'present_date_time']).apply(lambda x: abs(x.total_seconds())) < time_window)),
                      'triage_id'] = triage_id

            triage_id += 1

    return table


if __name__ == '__main__':
    table = query_stan_database(STAN_DATABASE_URI)
    table = filter_production_data(table, PRODUCTION_DHB)
    table = convert_timezones_to_nzt(table)
    table = assign_final_triage_records(table)

    table_name = 'STAN_PROD_DATA_{}.csv'.format(
        datetime.today().strftime('%d_%m_%y'))

    table.to_csv(table_name, index=False)
    print(f'STAN Production data saved to {Path.cwd()}')

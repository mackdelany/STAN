
def _record_value_change(dataset, triage_code_value_counts, rule, record_each_change=False):
    new_value_counts = dataset.TriageCode.value_counts()

    if record_each_change:
        print()
        print('Net change for {}'.format(rule))
        print(new_value_counts - triage_code_value_counts)

    return new_value_counts

def enforce_triage_framework_adherance(dataset, record_each_change=False):
    print()
    print('Enforcing Triage Framework')
    print('Dataset has {} entires'.format(dataset.shape[0]))
    print('Initial class distribution shape:')
    print(dataset.TriageCode.value_counts())

    adult_age = 16
    original_value_counts = dataset.TriageCode.value_counts()
    triage_code_value_counts = original_value_counts.copy()

    dataset, triage_code_value_counts = nz_adult(dataset, triage_code_value_counts)
    dataset, triage_code_value_counts = nz_paediatric(dataset, triage_code_value_counts)

    dataset, triage_code_value_counts = paediatric_vitals_0_3_months(dataset, triage_code_value_counts)
    dataset, triage_code_value_counts = paediatric_vitals_4_11_months(dataset, triage_code_value_counts)
    dataset, triage_code_value_counts = paediatric_vitals_1_4_years(dataset, triage_code_value_counts)
    dataset, triage_code_value_counts = paediatric_vitals_5_11_years(dataset, triage_code_value_counts)
    dataset, triage_code_value_counts = paediatric_vitals_12_adult_age(dataset, triage_code_value_counts)

    dataset, triage_code_value_counts = ats_indicators(dataset, triage_code_value_counts)

    print('\nInitial class distribution shape:\n{}'.format(original_value_counts))
    print('\nFinal class distribution shape:\n{}'.format(triage_code_value_counts))
    print('\nTotal change:\n{}'.format(triage_code_value_counts - original_value_counts))

    return dataset


def nz_adult(dataset, triage_code_value_counts, adult_age=16, pain=False):
    ## NZ Adult Category 1
    dataset.loc[(dataset['AgeInMonths'] >= (adult_age*12)) & (dataset['DisabilityValue'] == 1) & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'unconcious adult')
    dataset.loc[(dataset['AgeInMonths'] >= (adult_age*12)) & (dataset['DisabilityValue'] == 0.75) & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'adult responds to pain')
    
    ## NZ Adult Category 2
    dataset.loc[(dataset['AgeInMonths'] >= (adult_age*12)) & (dataset['Airway'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'adult altered airway')
    
    ## NZ Adult Category 3
    dataset.loc[(dataset['AgeInMonths'] >= (adult_age*12)) & (dataset['Breathing'] == 1) & (dataset['TriageCode'] > 3), ['TriageCode']] = 3
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'adult altered breathing')
    
    ## NZ Adult Category 4
    dataset.loc[(dataset['AgeInMonths'] >= (adult_age*12)) & (dataset['NeuroAssessment'] == 1) & (dataset['TriageCode'] > 4), ['TriageCode']] = 4
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'adult altered neuro')
    
    ## pain scale -- subjective ?
    if pain:
        dataset.loc[(dataset['AgeInMonths'] >= (adult_age*12)) & (dataset['PainScale'] >= 8) & (dataset['PainScale_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
        triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'adult severe pain')
        dataset.loc[(dataset['AgeInMonths'] >= (adult_age*12)) & (dataset['PainScale'] <= 7) & (dataset['PainScale'] >= 5) & (dataset['PainScale_was_measured'] == 1) & (dataset['TriageCode'] > 3), ['TriageCode']] = 3
        triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'adult moderate pain')
        dataset.loc[(dataset['AgeInMonths'] >= (adult_age*12)) & (dataset['PainScale'] <= 4) & (dataset['PainScale'] >= 2) & (dataset['PainScale_was_measured'] == 1) & (dataset['TriageCode'] > 4), ['TriageCode']] = 4
        triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'adult mild pain')

    return dataset, triage_code_value_counts


def nz_paediatric(dataset, triage_code_value_counts, adult_age=16, pain=False):
    ## NZ Paediatric Category 1
    dataset.loc[(dataset['AgeInMonths'] < (adult_age*12)) & (dataset['DisabilityValue'] == 1) & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'child unconcious')

    ## NZ Paediatric Category 2
    dataset.loc[(dataset['AgeInMonths'] < (adult_age*12)) & (dataset['Airway'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'child altered airway')
    dataset.loc[(dataset['AgeInMonths'] < (adult_age*12)) & (dataset['DisabilityValue'] == 0.75) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'child responds to pain')

    ## NZ Paediatric Category 3

    ## NZ Paediatric Category 4
    dataset.loc[(dataset['AgeInMonths'] < (adult_age*12)) & (dataset['Breathing'] == 1) & (dataset['TriageCode'] > 4), ['TriageCode']] = 4
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'child altered breathing')
    dataset.loc[(dataset['AgeInMonths'] < (adult_age*12)) & (dataset['NeuroAssessment'] == 1) & (dataset['TriageCode'] > 4), ['TriageCode']] = 4
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'child altered neuro')

    ## pain scale -- subjective ?
    if pain:
        dataset.loc[(dataset['AgeInMonths'] < (adult_age*12)) & (dataset['PainScale'] >= 8) & (dataset['PainScale_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
        triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'child severe pain')
        dataset.loc[(dataset['AgeInMonths'] < (adult_age*12)) & (dataset['PainScale'] <= 7) & (dataset['PainScale'] >= 5) & (dataset['PainScale_was_measured'] == 1) & (dataset['TriageCode'] > 3), ['TriageCode']] = 3
        triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'child moderate pain')
        dataset.loc[(dataset['AgeInMonths'] < (adult_age*12)) & (dataset['PainScale'] <= 4) & (dataset['PainScale'] >= 2) & (dataset['PainScale_was_measured'] == 1) & (dataset['TriageCode'] > 4), ['TriageCode']] = 4
        triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'child mild pain')

    return dataset, triage_code_value_counts


def adult_vitals(dataset, triage_code_value_counts, adult_age=16):
    adult_mask = (dataset['AgeInMonths'] > (adult_age*12))

    dataset.loc[adult_mask & (dataset['RespiratoryRate'] <= 4) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    dataset.loc[adult_mask & (dataset['RespiratoryRate'] >= 36) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    dataset.loc[adult_mask & (dataset['RespiratoryRate'] >= 5) & (dataset['RespiratoryRate'] <= 8) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2

    dataset.loc[adult_mask & (dataset['VitalSignsPulse'] < 50) & (dataset['VitalSignsPulse_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
    dataset.loc[adult_mask & (dataset['VitalSignsPulse'] > 140) & (dataset['VitalSignsPulse_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2

    dataset.loc[adult_mask & (dataset['BloodPressure_systolic'] < 80) & (dataset['BloodPressure_was_measured'] == 1) & (dataset['TriageCode'] > 1), ['TriageCode']] = 1

    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'adult vital signs')



def paediatric_vitals_0_3_months(dataset, triage_code_value_counts, adult_age=16):
    ## NZ Paediatric Category 2 | Vital signs 0-3 months
    paediatric_0_3_months_mask = (dataset['AgeInMonths'] <= 3)

    dataset.loc[paediatric_0_3_months_mask & (dataset['RespiratoryRate'] <= 15) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    dataset.loc[paediatric_0_3_months_mask & (dataset['RespiratoryRate'] >= 80) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    dataset.loc[paediatric_0_3_months_mask & (dataset['RespiratoryRate'] > 15) & (dataset['RespiratoryRate'] <= 25) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
    dataset.loc[paediatric_0_3_months_mask & (dataset['RespiratoryRate'] >= 60) & (dataset['RespiratoryRate'] < 80) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2

    dataset.loc[paediatric_0_3_months_mask & (dataset['VitalSignsPulse'] <= 90) & (dataset['VitalSignsPulse_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
    dataset.loc[paediatric_0_3_months_mask & (dataset['VitalSignsPulse'] >= 170) & (dataset['VitalSignsPulse_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2

    dataset.loc[paediatric_0_3_months_mask & (dataset['BloodPressure_systolic'] <= 50) & (dataset['BloodPressure_was_measured'] == 1) & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    dataset.loc[paediatric_0_3_months_mask & (dataset['BloodPressure_systolic'] <= 55) & (dataset['BloodPressure_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2

    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, '0-3 month vital signs')

    return dataset, triage_code_value_counts


def paediatric_vitals_4_11_months(dataset, triage_code_value_counts, adult_age=16):
    ## NZ Paediatric Category 2 | Vital signs 4-11 months
    paediatric_4_11_months_mask = (dataset['AgeInMonths'] >= 4) & (dataset['AgeInMonths'] <= 11)

    dataset.loc[paediatric_4_11_months_mask & (dataset['RespiratoryRate'] <= 10) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    dataset.loc[paediatric_4_11_months_mask & (dataset['RespiratoryRate'] >= 50) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
    dataset.loc[paediatric_4_11_months_mask & (dataset['RespiratoryRate'] > 10) & (dataset['RespiratoryRate'] <= 20) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2

    dataset.loc[paediatric_4_11_months_mask & (dataset['VitalSignsPulse'] <= 90) & (dataset['VitalSignsPulse_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
    dataset.loc[paediatric_4_11_months_mask & (dataset['VitalSignsPulse'] >= 170) & (dataset['VitalSignsPulse_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2

    dataset.loc[paediatric_4_11_months_mask & (dataset['BloodPressure_systolic'] <= 50) & (dataset['BloodPressure_was_measured'] == 1) & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    dataset.loc[paediatric_4_11_months_mask & (dataset['BloodPressure_systolic'] <= 55) & (dataset['BloodPressure_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2

    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, '4-11 month vital signs')

    return dataset, triage_code_value_counts

    
def paediatric_vitals_1_4_years(dataset, triage_code_value_counts, adult_age=16):
    ## NZ Paediatric Category 2 | Vital signs 1-4 years
    paediatric_1_4_years_mask = (dataset['AgeInMonths'] >= 12) & (dataset['AgeInMonths'] < (5*12))

    dataset.loc[paediatric_1_4_years_mask & (dataset['RespiratoryRate'] <= 10) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    dataset.loc[paediatric_1_4_years_mask & (dataset['RespiratoryRate'] >= 40) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
    dataset.loc[paediatric_1_4_years_mask & (dataset['RespiratoryRate'] > 10) & (dataset['RespiratoryRate'] <= 15) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2

    dataset.loc[paediatric_1_4_years_mask & (dataset['VitalSignsPulse'] <= 80) & (dataset['VitalSignsPulse_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
    dataset.loc[paediatric_1_4_years_mask & (dataset['VitalSignsPulse'] >= 150) & (dataset['VitalSignsPulse_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2

    dataset.loc[paediatric_1_4_years_mask & (dataset['BloodPressure_systolic'] <= 55) & (dataset['BloodPressure_was_measured'] == 1) & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    dataset.loc[paediatric_1_4_years_mask & (dataset['BloodPressure_systolic'] <= 65) & (dataset['BloodPressure_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2

    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, '1-4 years vital signs')

    return dataset, triage_code_value_counts


def paediatric_vitals_5_11_years(dataset, triage_code_value_counts, adult_age=16):
    ## NZ Paediatric Category 2 | Vital signs 5-11 years
    paediatric_5_11_years_mask = (dataset['AgeInMonths'] >= (5*12)) & (dataset['AgeInMonths'] < (12*12))

    dataset.loc[paediatric_5_11_years_mask & (dataset['RespiratoryRate'] <= 10) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    dataset.loc[paediatric_5_11_years_mask & (dataset['RespiratoryRate'] >= 45) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
    dataset.loc[paediatric_5_11_years_mask & (dataset['RespiratoryRate'] > 10) & (dataset['RespiratoryRate'] <= 15) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2

    dataset.loc[paediatric_5_11_years_mask & (dataset['VitalSignsPulse'] <= 60) & (dataset['VitalSignsPulse_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
    dataset.loc[paediatric_5_11_years_mask & (dataset['VitalSignsPulse'] >= 150) & (dataset['VitalSignsPulse_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2

    dataset.loc[paediatric_5_11_years_mask & (dataset['BloodPressure_systolic'] <= 55) & (dataset['BloodPressure_was_measured'] == 1) & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    dataset.loc[paediatric_5_11_years_mask & (dataset['BloodPressure_systolic'] <= 65) & (dataset['BloodPressure_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2

    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, '5-11 years vital signs')

    return dataset, triage_code_value_counts


def paediatric_vitals_12_adult_age(dataset, triage_code_value_counts, adult_age=16):
    ## NZ Paediatric Category 2 | Vital signs 12+ years
    paediatric_12_adult_age_mask = (dataset['AgeInMonths'] >= (12*12)) & (dataset['AgeInMonths'] < (adult_age*12))

    dataset.loc[paediatric_12_adult_age_mask & (dataset['RespiratoryRate'] <= 5) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    dataset.loc[paediatric_12_adult_age_mask & (dataset['RespiratoryRate'] >= 35) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
    dataset.loc[paediatric_12_adult_age_mask & (dataset['RespiratoryRate'] > 5) & (dataset['RespiratoryRate'] <= 10) & (dataset['RespiratoryRate_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2

    dataset.loc[paediatric_12_adult_age_mask & (dataset['VitalSignsPulse'] <= 50) & (dataset['VitalSignsPulse_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
    dataset.loc[paediatric_12_adult_age_mask & (dataset['VitalSignsPulse'] >= 140) & (dataset['VitalSignsPulse_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2

    dataset.loc[paediatric_12_adult_age_mask & (dataset['BloodPressure_systolic'] <= 80) & (dataset['BloodPressure_was_measured'] == 1) & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    dataset.loc[paediatric_12_adult_age_mask & (dataset['BloodPressure_systolic'] <= 90) & (dataset['BloodPressure_was_measured'] == 1) & (dataset['TriageCode'] > 2), ['TriageCode']] = 2

    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, '12-adult age vital signs')

    return dataset, triage_code_value_counts


    
def ats_indicators(dataset, triage_code_value_counts):

    ## ATS Category 1
    dataset.loc[(dataset['PresentingComplaint'] == 'Cardiac arrest') & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'cardiac arrest')
    dataset.loc[(dataset['PresentingComplaint'] == 'Cardiac arrest due to trauma') & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'cardiac arrest due to trauma')
    dataset.loc[(dataset['PresentingComplaint'] == 'Respiratory arrest') & (dataset['TriageCode'] > 1), ['TriageCode']] = 1
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'respiratory arrest')
    

    ## ATS Category 2
    """dataset.loc[(dataset['PresentingComplaint'] == 'Chest pain') & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'chest pain')"""
    dataset.loc[(dataset['PresentingComplaint'] == 'Multiple injuries - major') & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'multiple injuries major')
    dataset.loc[(dataset['PresentingComplaint'] == 'Aggresive behaviour') & (dataset['TriageCode'] > 2), ['TriageCode']] = 2
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'aggresive behavior')
    

    ## ATS Category 3
    dataset.loc[(dataset['PresentingComplaint'] == 'Abdominal pain') & (dataset['AgeInMonths'] > (65*12)) & (dataset['TriageCode'] > 3), ['TriageCode']] = 3
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'abdo pain and over 65')
    dataset.loc[(dataset['AgeInMonths'] < (4)) & (dataset['TriageCode'] > 3), ['TriageCode']] = 3
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'neonate')

    ## ATS Category 4
    dataset.loc[(dataset['PresentingComplaint'] == 'Injury of chest') & (dataset['TriageCode'] > 4), ['TriageCode']] = 4
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'injury of chest')
    dataset.loc[(dataset['PresentingComplaint'] == 'Injury of head') & (dataset['TriageCode'] > 4), ['TriageCode']] = 4
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'injury of head')
    dataset.loc[(dataset['PresentingComplaint'] == 'Foreign body in ear canal') & (dataset['TriageCode'] > 4), ['TriageCode']] = 4
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'foreign body in ear canal')
    dataset.loc[(dataset['PresentingComplaint'] == 'Foreign body in eye') & (dataset['TriageCode'] > 4), ['TriageCode']] = 4
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'foreign body in eye')
    dataset.loc[(dataset['PresentingComplaint'] == 'Foreign body in gastrointestinal tract (swallowed)') & (dataset['TriageCode'] > 4), ['TriageCode']] = 4
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'foreign body in gastro tract')
    dataset.loc[(dataset['PresentingComplaint'] == 'Foreign body in genitourinary tract') & (dataset['TriageCode'] > 4), ['TriageCode']] = 4
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'foreign body in geni tract')
    dataset.loc[(dataset['PresentingComplaint'] == 'Foreign body in nose') & (dataset['TriageCode'] > 4), ['TriageCode']] = 4
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'foreign body in nose')
    dataset.loc[(dataset['PresentingComplaint'] == 'Foreign body in rectum') & (dataset['TriageCode'] > 4), ['TriageCode']] = 4
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'foreign body in rectum')
    dataset.loc[(dataset['PresentingComplaint'] == 'Foreign body in respiratory tract (inhaled)') & (dataset['TriageCode'] > 4), ['TriageCode']] = 4
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'foreign body in resp tract')
    dataset.loc[(dataset['PresentingComplaint'] == 'Foreign body in skin') & (dataset['TriageCode'] > 4), ['TriageCode']] = 4
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'foreign body in skin')
    dataset.loc[(dataset['PresentingComplaint'] == 'Foreign body in throat') & (dataset['TriageCode'] > 4), ['TriageCode']] = 4
    triage_code_value_counts = _record_value_change(dataset, triage_code_value_counts, 'foreign body in throat')

    return dataset, triage_code_value_counts

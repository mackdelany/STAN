"""
"""

import datetime
from typing import Union

from dateutil import parser as dateutil_parser
from dateutil.relativedelta import relativedelta
from flask import g

from ..core.exceptions import EmptyRequiredFieldError, InvalidDateOfBirthError, InvalidOptionalFieldError, OutOfRangeNumericalFieldError
from ..core.triage_request import TriageRequest
from ..core.timezones import localize_tz_to_utc, nznow, utcnow
from ..core.util import remove_non_numbers


class RequestParser():
    """
    """
    general_fields = {
        'hospital': 'Hospital',
        'dhb': 'DHB',
        'gender': 'Gender',
        'airway': 'Airway',
        'breathing': 'Breathing',
        'circulatory_skin': 'CirculatorySkin',
        'disability_value': 'DisabilityValue',
        'neuro_assessment': 'NeuroAssessment',
        'pain_scale': 'PainScale',
        'vital_signs_pulse': 'VitalSignsPulse',
        'respiratory_rate': 'RespiratoryRate',
        # n.b this breaks into bps and bpd later
        'blood_pressure': 'BloodPressure',
        'temperature': 'Temperature',
        'sats': 'Sats',
        'mental_health_concerns': 'MentalHealthConcerns',
        'immunocompromised': 'Immunocompromised',
        'triage_assessment': 'TriageAssessment',
        'event_id': 'EventIdentifier',
        'nurse_triage_code': 'NurseTriageCode'
    }

    null_imputations = {
        'gender': 'U',
        'airway': 'PATENT',
        'breathing': 'NO DISTRESS',
        'circulatory_skin': 'NORMAL',
        'disability_value': 'A',
        'neuro_assessment': 'INTACT'
    }

    valid_str_fields = {
        'gender': ['M', 'F'],
        'airway': ['PATENT', 'OTHER'],
        'breathing': ['NO DISTRESS', 'OTHER'],
        'circulatory_skin': ['NORMAL', 'ALTERED'],
        'disability_value': ['A', 'V', 'P', 'U'],
        'neuro_assessment': ['INTACT', 'OTHER'],
    }

    string_field_map = {
        'airway_altered': {'PATENT': False, 'OTHER': True},
        'breathing_altered': {'NO DISTRESS': False, 'OTHER': True},
        'circulation_altered': {'NORMAL': False, 'ALTERED': True},
        'disability_gcs': {'A': 15, 'V': 12, 'P': 9, 'U': 6},
        'pain_scale': {'NIL': 0, 'MILD': 3, 'MODERATE': 6, 'SEVERE': 9},
        'neuro_altered': {'INTACT': False, 'OTHER': True},
        'mental_health_concerns': {'YES': True, 'NO': False}
    }

    valid_numerical_fields = {
        'pain_scale': {'min': 0, 'max': 10},
        'vital_signs_pulse': {'min': 0, 'max': 250},
        'respiratory_rate': {'min': 0, 'max': 120},
        'blood_pressure_systolic': {'min': 30, 'max': 400},
        'blood_pressure_diastolic': {'min': 0, 'max': 400},
        'temperature': {'min': 20, 'max': 50},
        'sats': {'min': 50, 'max': 100},
    }

    presenting_complaint_groups = {
        # MUST FILL -> should this be inherited?
        'Altered mental state/confusion': 'CNS',
        'Altered sensation': 'CNS',
        'Ataxia': 'CNS',
        'Dizziness/vertigo': 'CNS',
        'Fall(s) - no significant injury': 'CNS',
        'Headache': 'CNS',
        'Memory loss': 'CNS',
        'Seizure': 'CNS',
        'Speech problem': 'CNS',
        'Tremor': 'CNS',
        'Weakness of face muscles': 'CNS',
        'Weakness of limb': 'CNS',

        'Cardiac arrest': 'CVS',
        'Chest pain': 'CVS',
        'Collapse/syncope': 'CVS',
        'Palpitations': 'CVS',
        'Shock from internal defibrillator': 'CVS',
        'Swollen leg (single)': 'CVS',
        'Swollen legs (both)': 'CVS',
        'Vascular disorder of limb': 'CVS',

        'Chemical exposure': 'ENV',
        'Drowning': 'ENV',
        'Electrical injury': 'ENV',
        'Frostbite': 'ENV',
        'Hypothermia': 'ENV',
        'Noxious inhalation': 'ENV',
        'Toxic inhalation injury': 'ENV',  # Additional to form

        'Discharge from eye': 'EYE',
        'Foreign body in eye': 'EYE',
        'Pain in eye': 'EYE',
        'Photophobia': 'EYE',
        'Red eye': 'EYE',
        'Visual disturbance': 'EYE',

        'Abdominal distension': 'GI',
        'Abdominal pain': 'GI',
        'Altered bowel habit': 'GI',
        'Feeding problem': 'GI',
        'Foreign body in gastrointestinal tract (swallowed)': 'GI',
        'Foreign body in rectum': 'GI',
        'Foreign body in throat': 'GI',
        'Hiccoughs': 'GI',
        'Jaundice': 'GI',
        'Loss of appetite': 'GI',
        'Mouth problem (not dental)': 'GI',
        'Nausea/vomiting/diarrhoea': 'GI',
        'Pain in anus/rectum': 'GI',
        'Pain in groin': 'GI',
        'Rectal bleed': 'GI',
        'Stoma problem': 'GI',
        'Swallowing problem': 'GI',
        'Vomiting blood': 'GI',
        'Constipation': 'GI',  # Addtional to form

        'Blood in urine': 'GU',
        'Complication of urinary catheter': 'GU',
        'Excessive urine output': 'GU',
        'Foreign body in genitourinary tract': 'GU',
        'Male genital problem': 'GU',
        'Reduced urine output': 'GU',
        'Urethral discharge': 'GU',
        'Urinary retention': 'GU',
        'UTI symptoms': 'GU',

        'Discharge from ear': 'HEAD/NECK',
        'Earache': 'HEAD/NECK',
        'Foreign body in ear canal': 'HEAD/NECK',
        'Foreign body in nose': 'HEAD/NECK',
        'Hearing loss/tinnitus': 'HEAD/NECK',
        'Nose bleed': 'HEAD/NECK',
        'Pain in face': 'HEAD/NECK',
        'Swelling of face': 'HEAD/NECK',
        'Swelling of tongue': 'HEAD/NECK',
        'Toothache/dental infection': 'HEAD/NECK',

        'Abnormal behaviour': 'MENTAL HEALTH',
        'Aggressive behaviour': 'MENTAL HEALTH',
        'Anxiety': 'MENTAL HEALTH',
        'Insomnia': 'MENTAL HEALTH',
        'Mental health problem': 'MENTAL HEALTH',
        'Self harm': 'MENTAL HEALTH',
        'Situational crisis': 'MENTAL HEALTH',
        'Suicidal thoughts': 'MENTAL HEALTH',

        'Abnormal vital sign(s)': 'MISC',
        'Administration of medication': 'MISC',
        'Certificate or paperwork requested': 'MISC',
        'Complication of device (not catheter)': 'MISC',
        'Crying baby': 'MISC',
        'Exposure to blood/body fluid': 'MISC',
        'Exposure to communicable disease': 'MISC',
        'Fever symptoms': 'MISC',
        'Follow-up visit': 'MISC',
        'General weakness/fatigue/unwell': 'MISC',
        'Hyperglycaemia': 'MISC',
        'Hypoglycaemia': 'MISC',
        'Postoperative complication': 'MISC',
        'Referral for investigation': 'MISC',
        'Script request': 'MISC',
        'Wound complication': 'MISC',  # Additional to form

        'Back pain (no recent injury)': 'MSK',
        'Difficulty weight bearing': 'MSK',
        'Increased muscle tone': 'MSK',
        'Neck pain (no recent injury)': 'MSK',
        'Pain in hip': 'MSK',
        'Pain in lower limb (no recent injury)': 'MSK',
        'Pain in upper limb (no recent injury)': 'MSK',
        'Plaster cast problem': 'MSK',
        'Swelling of joint (no recent injury)': 'MSK',

        'Breast problem': 'O&G',
        'Female genital problem': 'O&G',
        'Labour': 'O&G',
        'Postpartum complication': 'O&G',
        'Pregnancy problem': 'O&G',
        'Sexual assault': 'O&G',
        'Vaginal bleeding - not pregnant': 'O&G',
        'Vaginal discharge': 'O&G',
        'Pain in breast': 'O&G',  # Additional to form

        'Cough': 'RESP',
        'Cyanosis': 'RESP',
        'Foreign body in respiratory tract (inhaled)': 'RESP',
        'Coughing up blood': 'RESP',
        'Nasal congestion': 'RESP',
        'Noisy breathing': 'RESP',
        'Periods of not breathing': 'RESP',
        'Respiratory arrest': 'RESP',
        'Shortness of breath': 'RESP',
        'Sore throat': 'RESP',
        'Episodes of not breathing (apnoea)': 'RESP',  # Additional to form

        'Bite': 'SKIN',
        'Burn': 'SKIN',
        'Change of dressing': 'SKIN',
        'Foreign body in skin': 'SKIN',
        'Itching': 'SKIN',
        'Localised lump/redness/swelling of skin': 'SKIN',
        'Open wound (abrasion/laceration/puncture)': 'SKIN',
        'Rash': 'SKIN',
        'Removal of skin sutures or staples': 'SKIN',
        'Spontaneous bruising': 'SKIN',  # Additional to form

        'Alcohol/drug intoxication or withdrawal': 'TOX',
        'Ingestion of potentially harmful substance': 'TOX',
        'Overdose of drug': 'TOX',
        'Sting': 'TOX',

        'Cardiac arrest due to trauma': 'TRAUMA/INJURY',
        'Injury of abdomen': 'TRAUMA/INJURY',
        'Injury of back': 'TRAUMA/INJURY',
        'Injury of buttock': 'TRAUMA/INJURY',
        'Injury of chest': 'TRAUMA/INJURY',
        'Injury of ear': 'TRAUMA/INJURY',
        'Injury of eye': 'TRAUMA/INJURY',
        'Injury of face': 'TRAUMA/INJURY',
        'Injury of genitalia': 'TRAUMA/INJURY',
        'Injury of head': 'TRAUMA/INJURY',
        'Injury of hip': 'TRAUMA/INJURY',
        'Injury of lower limb': 'TRAUMA/INJURY',
        'Injury of neck': 'TRAUMA/INJURY',
        'Injury of nose': 'TRAUMA/INJURY',
        'Injury of perineum': 'TRAUMA/INJURY',
        'Injury of upper limb': 'TRAUMA/INJURY',
        'Multiple injuries - major': 'TRAUMA/INJURY',
        'Multiple injuries - minor': 'TRAUMA/INJURY'
    }

    def __init__(self):
        pass

    def parse_request(self, req_data: dict, method: str) -> TriageRequest:
        """

        Args:
            req_data: dict of json request, with following fields:
                - 'PresentingComplaint'
                - 'DOB'
                ...

            method: 
        """
        method = method     # for completeness
        event_id = self._parse_general(
            req_data, self.general_fields['event_id'])
        hospital = self._parse_general(
            req_data, self.general_fields['hospital'])
        dhb = self._parse_general(req_data, self.general_fields['dhb'])

        present_date_time = utcnow()
        present_date_time_local = nznow()
        dob = self._parse_dob(req_data)
        presenting_complaint, presenting_complaint_group = self._parse_presenting_complaint(
            req_data)

        nurse_triage_code = self._parse_general(
            req_data, self.general_fields['nurse_triage_code'])

        empty_req_fields = []
        if hospital is None:
            empty_req_fields.append('Hospital')
        if dhb is None:
            empty_req_fields.append('DHB')
        if presenting_complaint is None:
            empty_req_fields.append('PresentingComplaint')
        if dob is None:
            empty_req_fields.append('DOB')
        if nurse_triage_code is None and method.upper() in ['RECORD', 'RECORD-TESTING']:
            empty_req_fields.append('NurseTriageCode')
        if len(empty_req_fields) > 1:
            raise EmptyRequiredFieldError(empty_req_fields, method)
        elif len(empty_req_fields) == 1:
            raise EmptyRequiredFieldError(empty_req_fields[0], method)

        triage_assessment = self._parse_general(
            req_data, self.general_fields['triage_assessment'])
        age_in_months = self._get_age_in_months(present_date_time, dob)
        gender = self._parse_general(req_data, self.general_fields['gender'])

        vital_signs_pulse = self._parse_general(
            req_data, self.general_fields['vital_signs_pulse'])
        respiratory_rate = self._parse_general(
            req_data, self.general_fields['respiratory_rate'])
        blood_pressure = self._parse_general(
            req_data, self.general_fields['blood_pressure'])
        blood_pressure_systolic, blood_pressure_diastolic = self._impute_blood_pressure(
            blood_pressure)
        temperature = self._parse_general(
            req_data, self.general_fields['temperature'])
        sats = self._parse_general(req_data, self.general_fields['sats'])

        airway = self._parse_general(req_data, self.general_fields['airway'])
        breathing = self._parse_general(
            req_data, self.general_fields['breathing'])
        circulatory_skin = self._parse_general(
            req_data, self.general_fields['circulatory_skin'])
        disability_value = self._parse_general(
            req_data, self.general_fields['disability_value'])
        pain_scale = self._parse_general(
            req_data, self.general_fields['pain_scale'])
        neuro_assessment = self._parse_general(
            req_data, self.general_fields['neuro_assessment'])
        mental_health_concerns = self._parse_general(
            req_data, self.general_fields['mental_health_concerns'])
        immunocompromised = self._parse_general(
            req_data, self.general_fields['immunocompromised'])

        airway_was_measured = self._check_measurement(airway)
        breathing_was_measured = self._check_measurement(breathing)
        circulation_was_measured = self._check_measurement(circulatory_skin)
        disability_gcs_was_measured = self._check_measurement(disability_value)
        pain_was_measured = self._check_measurement(pain_scale)
        neuro_was_measured = self._check_measurement(neuro_assessment)
        vital_signs_pulse_was_measured = self._check_measurement(
            vital_signs_pulse)
        respiratory_rate_was_measured = self._check_measurement(
            respiratory_rate)
        blood_pressure_was_measured = self._check_measurement(blood_pressure)
        temperature_was_measured = self._check_measurement(temperature)
        sats_was_measured = self._check_measurement(sats)
        mental_health_was_measured = self._check_measurement(
            mental_health_concerns)
        immunocompromised_was_measured = self._check_measurement(
            immunocompromised)

        gender = self._enforce_str_field_validity(gender, 'gender')
        airway = self._enforce_str_field_validity(airway, 'airway')
        breathing = self._enforce_str_field_validity(breathing, 'breathing')
        circulatory_skin = self._enforce_str_field_validity(
            circulatory_skin, 'circulatory_skin')
        disability_value = self._enforce_str_field_validity(
            disability_value, 'disability_value')
        neuro_assessment = self._enforce_str_field_validity(
            neuro_assessment, 'neuro_assessment')

        airway_altered = self._map_string_field('airway_altered', airway)
        breathing_altered = self._map_string_field(
            'breathing_altered', breathing)
        circulation_altered = self._map_string_field(
            'circulation_altered', circulatory_skin)
        disability_gcs = self._map_string_field(
            'disability_gcs', disability_value)
        pain_scale = self._map_string_field('pain_scale', pain_scale)
        neuro_altered = self._map_string_field(
            'neuro_altered', neuro_assessment)
        mental_health_concerns = self._map_string_field(
            'mental_health_concerns', mental_health_concerns)
        # might be received as 1/0 need true/false
        immunocompromised = bool(immunocompromised)

        pain_scale = self._enforce_numerical_validity(pain_scale, 'pain_scale')
        vital_signs_pulse = self._enforce_numerical_validity(
            vital_signs_pulse, 'vital_signs_pulse')
        respiratory_rate = self._enforce_numerical_validity(
            respiratory_rate, 'respiratory_rate')
        blood_pressure_systolic = self._enforce_numerical_validity(
            blood_pressure_systolic, 'blood_pressure_systolic')
        blood_pressure_diastolic = self._enforce_numerical_validity(
            blood_pressure_diastolic, 'blood_pressure_diastolic')
        temperature = self._enforce_numerical_validity(
            temperature, 'temperature')
        sats = self._enforce_numerical_validity(sats, 'sats')

        triage_request = TriageRequest(
            event_id=event_id,
            method=method,
            hospital=hospital,
            dhb=dhb,
            present_date_time=present_date_time,
            present_date_time_local=present_date_time_local,
            dob=dob,
            age_in_months=age_in_months,
            gender=gender,
            presenting_complaint=presenting_complaint,
            presenting_complaint_group=presenting_complaint_group,
            triage_assessment=triage_assessment,
            nurse_triage_code=nurse_triage_code,
            vital_signs_pulse=vital_signs_pulse,
            respiratory_rate=respiratory_rate,
            blood_pressure_systolic=blood_pressure_systolic,
            blood_pressure_diastolic=blood_pressure_diastolic,
            temperature=temperature,
            sats=sats,
            airway_altered=airway_altered,
            breathing_altered=breathing_altered,
            circulation_altered=circulation_altered,
            disability_gcs=disability_gcs,
            pain_scale=pain_scale,
            neuro_altered=neuro_altered,
            mental_health_concerns=mental_health_concerns,
            immunocompromised=immunocompromised,
            airway_was_measured=airway_was_measured,
            breathing_was_measured=breathing_was_measured,
            circulation_was_measured=circulation_was_measured,
            disability_gcs_was_measured=disability_gcs_was_measured,
            pain_was_measured=pain_was_measured,
            neuro_was_measured=neuro_was_measured,
            vital_signs_pulse_was_measured=vital_signs_pulse_was_measured,
            respiratory_rate_was_measured=respiratory_rate_was_measured,
            blood_pressure_was_measured=blood_pressure_was_measured,
            temperature_was_measured=temperature_was_measured,
            sats_was_measured=sats_was_measured,
            mental_health_was_measured=mental_health_was_measured,
            immunocompromised_was_measured=immunocompromised_was_measured,
        )

        return triage_request

    @staticmethod
    def _field_exists(req_data: dict, field: str) -> bool:
        if field in req_data:
            if req_data[field] is not None and str(req_data[field]) not in ['', 'nan', 'NaN']:
                return True
        return False

    @staticmethod
    def _parse_general(req_data: dict, field: str) -> Union[str, int, float, None]:
        if RequestParser._field_exists(req_data, field):
            return req_data[field]
        return None

    def _parse_presenting_complaint(self, req_data: dict, cpc_key: str = 'PresentingComplaint'):
        if RequestParser._field_exists(req_data, cpc_key):
            presenting_complaint = req_data[cpc_key]
            if req_data[cpc_key] in self.presenting_complaint_groups:
                presenting_complaint_group = self.presenting_complaint_groups[presenting_complaint]
            else:
                presenting_complaint_group = 'UNKNOWN'
            return presenting_complaint, presenting_complaint_group
        return None, None

    @staticmethod
    def _check_measurement(field: Union[str, int, float]) -> bool:
        if field is not None:
            return True
        return False

    @staticmethod
    def _parse_dob(req_data: dict, dob_key: str = 'DOB'):
        try:
            if req_data[dob_key] is None:
                return None
            else:
                dob = dateutil_parser.parse(req_data[dob_key])
                dob = localize_tz_to_utc(dob)
                return dob
        except KeyError as ex:
            return None
        except ValueError as ex:
            raise InvalidDateOfBirthError(req_data[dob_key])
        except Exception as ex:
            raise InvalidDateOfBirthError(req_data[dob_key])

    @staticmethod
    def _get_age_in_months(present_date_time: datetime.datetime, dob: datetime.datetime):
        age_rd = relativedelta(present_date_time, dob)
        age_in_months = age_rd.months + (age_rd.years * 12)
        return age_in_months

    @staticmethod
    def _impute_blood_pressure(blood_pressure: Union[str, None]) -> tuple:
        # TODO try clean up woo!
        if blood_pressure is not None:
            if blood_pressure.count('/') == 1:
                pressures = blood_pressure.split('/')
                blood_pressure_systolic = remove_non_numbers(pressures[0])
                blood_pressure_diastolic = remove_non_numbers(pressures[1])
                if len(blood_pressure_systolic) > 0:
                    blood_pressure_systolic = int(blood_pressure_systolic)
                else:
                    blood_pressure_systolic = None
                if len(blood_pressure_diastolic) > 0:
                    blood_pressure_diastolic = int(blood_pressure_diastolic)
                else:
                    blood_pressure_diastolic = None
            elif blood_pressure.count('/') == 0:
                blood_pressure_systolic = remove_non_numbers(blood_pressure)
                if len(blood_pressure_systolic) > 0:
                    blood_pressure_systolic = int(blood_pressure_systolic)
                else:
                    blood_pressure_systolic = None
                blood_pressure_diastolic = None
            else:
                blood_pressure_systolic = None
                blood_pressure_diastolic = None
        else:
            blood_pressure_systolic = None
            blood_pressure_diastolic = None
        return blood_pressure_systolic, blood_pressure_diastolic

    def _enforce_str_field_validity(self, field: str, field_key: str) -> str:
        if field in self.valid_str_fields[field_key]:
            return field
        elif field is None:
            return self.null_imputations[field_key]
        else:
            invalid_field_error = InvalidOptionalFieldError(field, field_key)
            g.errors.append(invalid_field_error.create_error_payload())
            return self.null_imputations[field_key]

    def _enforce_numerical_validity(self, field: Union[int, float], field_key: str) -> Union[int, float, None]:
        exp_min = self.valid_numerical_fields[field_key]['min']
        exp_max = self.valid_numerical_fields[field_key]['max']
        if field is not None and field >= exp_min and field <= exp_max:
            return field
        elif field is None:
            return field
        else:
            invalid_field_error = OutOfRangeNumericalFieldError(
                field_key, field, exp_min, exp_max)
            g.errors.append(invalid_field_error.create_error_payload())
            return None

    def _map_string_field(self, return_field: str, current_value: str):
        """
        """
        if type(current_value) == str:
            mapped_field = self.string_field_map[return_field][current_value]
            return mapped_field
        return current_value

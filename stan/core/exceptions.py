"""
"""

from typing import Union, List

from .timezones import utcnow


class TriageRequestError(Exception):
    def __init__(self, message=None):
        self.message = message
        self.timestamp = utcnow()

    def create_error_payload(self):
        error_payload = {
            'error_type': str(self.__class__.__name__),
            'message': self.message,
            'timestamp': self.timestamp
        }
        return error_payload

class APIKeyError(TriageRequestError):
    def __init__(self, message):
        super().__init__(message=message)

class EmptyRequiredFieldError(TriageRequestError):
    def __init__(self, required_field: Union[str, List[str]], method: str):
        if isinstance(required_field, list):
            req_fields = ''
            for field in required_field:
                req_fields += f'{field}, '
            message=f'{req_fields}not in request. {req_fields}are required fields for a {method} request.'
        else:
            message=f'No {required_field} in request. {required_field} is a required fields for a {method} request.'
        super().__init__(message=message)

class InvalidRequestError(TriageRequestError):
    def __init__(self, message):
        super().__init__(message=message)

class InvalidRequiredFieldError(TriageRequestError):
    def __init__(self, required_field_value, required_field, endpoint):
        super().__init__(message=f"'{required_field_value}' is an invalid entry for {required_field}. {required_field} is a required field for the {endpoint} endpoint.")

class InvalidDateOfBirthError(TriageRequestError):
    def __init__(self, dob):
        super().__init__(message=f"'{dob}' is an invalid timestamp for DOB. Datetimes should be of the format '%Y-%m-%d %H:%M:%S.%f'.")

class InvalidOptionalFieldError(TriageRequestError):
    def __init__(self, optional_field_value, optional_field):
        super().__init__(
            message=f'{optional_field_value} is an invalid value for {optional_field}; {optional_field} is an optional field but predictions will be more accurate if it is used correctly.'
            )

class OutOfRangeNumericalFieldError(TriageRequestError):
    def __init__(self, field_key, field_value, expected_min, expected_max):
        super().__init__(
            message=f'{field_value} is outside of the valid range for {field_key}; a value between {expected_min} and {expected_max} is expected.'
            )

class UnknownEarlyWarningScoreTypeError(TriageRequestError):
    def __init__(self, age_in_months, presenting_complaint):
        super().__init__(message=f'Invalid input. Is {presenting_complaint} for a {age_in_months//12} y/o patient correct? Check your payload and/or contact the service admin')

class InvalidModelInputError(TriageRequestError):
    def __init__(self, X, mappings):

        def return_feature_input(feature, X, mappings):
            return f"{feature}: {feature, X[0, mappings['FEATURE_MAPPINGS'][feature]]}\n"

        printout = 'Invalid model input for below features: \n'
        printout = printout + return_feature_input('PresentingComplaint', X, mappings)
        printout = printout + return_feature_input('mean_triage_code', X, mappings)
        printout = printout + return_feature_input('PresentingComplaintGroup', X, mappings)
        printout = printout + return_feature_input('AgeInMonths', X, mappings)
        printout = printout + return_feature_input('Gender', X, mappings)
        printout = printout + return_feature_input('Airway', X, mappings)
        printout = printout + return_feature_input('Breathing', X, mappings)
        printout = printout + return_feature_input('NeuroAssessment', X, mappings)
        printout = printout + return_feature_input('CirculatorySkin', X, mappings)
        printout = printout + return_feature_input('MentalHealthConcerns', X, mappings)
        printout = printout + return_feature_input('DisabilityValue', X, mappings)
        printout = printout + return_feature_input('Immunocompromised', X, mappings)
        printout = printout + return_feature_input('hour_sin', X, mappings)
        printout = printout + return_feature_input('hour_cos', X, mappings)
        printout = printout + return_feature_input('PainScale', X, mappings)
        printout = printout + return_feature_input('VitalSignsPulse', X, mappings)
        printout = printout + return_feature_input('Sats', X, mappings)
        printout = printout + return_feature_input('RespiratoryRate', X, mappings)
        printout = printout + return_feature_input('BloodPressure_systolic', X, mappings)
        printout = printout + return_feature_input('BloodPressure_diastolic', X, mappings)
        printout = printout + return_feature_input('Temperature', X, mappings)
        printout = printout + return_feature_input('PainScale_was_measured', X, mappings)
        printout = printout + return_feature_input('Airway_was_measured', X, mappings)
        printout = printout + return_feature_input('Breathing_was_measured', X, mappings)
        printout = printout + return_feature_input('CirculatorySkin_was_measured', X, mappings)
        printout = printout + return_feature_input('DisabilityValue_was_measured', X, mappings)
        printout = printout + return_feature_input('NeuroAssessment_was_measured', X, mappings)
        printout = printout + return_feature_input('MentalHealthConcerns_was_measured', X, mappings)
        printout = printout + return_feature_input('Immunocompromised_was_measured', X, mappings)
        printout = printout + return_feature_input('VitalSignsPulse_was_measured', X, mappings)
        printout = printout + return_feature_input('RespiratoryRate_was_measured', X, mappings)
        printout = printout + return_feature_input('BloodPressure_was_measured', X, mappings)
        printout = printout + return_feature_input('Temperature_was_measured', X, mappings)
        printout = printout + return_feature_input('Sats_was_measured', X, mappings)

        print(printout)
        
        super().__init__(message='Invalid input. Check your payload and/or contact the service admin')

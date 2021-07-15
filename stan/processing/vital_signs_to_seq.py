from .base_triage_framework import BaseTriageFramework

class VitalSigns(BaseTriageFramework):

    def apply_triage_vital_signs(self):
        if self.age_in_months >= (12*self.adult_age):
            self._adult_vital_signs()
        else:
            self._paediatric_vital_signs()


    def _paediatric_vital_signs(self):
        if self.age_in_months <= 3:
            self._paediatric_vital_signs_0_3_months()
        elif (self.age_in_months >= 4) & (self.age_in_months <= 11):
            self._paediatric_vital_signs_4_11_months()
        elif (self.age_in_months >= 12) & (self.age_in_months < (5*12)):
            self._paediatric_vital_signs_1_4_years()
        elif (self.age_in_months >= (5*12)) & (self.age_in_months < (12*12)):
            self._paediatric_vital_signs_5_11_years()
        else :
            self._paediatric_vital_signs_12_adult_age()


    


"""
"""

from typing import Tuple

from ..core.triage_request import TriageRequest


class RedFlags():

    def __init__(self, adult_age=17):
        """
        """
        self.red_flags = {
            'sepsis': ['all_hospitals'],
            'chest_pain_2': ['all_hospitals', 'Nelson', 'Wairau', 'pytest'],
            'febrile_infant': ['all_hospitals'],
            'febrile_neutroenia': ['all_hospitals'],
            'mental_health_pathway': ['all_hospitals', 'Nelson', 'Wairau', 'pytest'],
            'neutropenic_pathway': ['all_hospitals', 'Nelson', 'Wairau', 'pytest'],
            'asthma_adult': ['all_hospitals', 'Nelson', 'Wairau', 'pytest'],
            'hip_fracture': ['all_hospitals', 'Nelson', 'Wairau', 'pytest'],
            'paediatric_oncology': ['all_hospitals', 'Nelson', 'Wairau', 'pytest']
            }
        self.adult_age = adult_age

    def assess_red_flags(self, triage_request: TriageRequest) -> Tuple[list, int]:
        """
        """
        warnings = []
        min_urgency = 5

        if self._apply_rule_for_hospital(triage_request.hospital, 'sepsis'):
            warnings, min_urgency = self._sepsis(triage_request, warnings, min_urgency)

        if self._apply_rule_for_hospital(triage_request.hospital, 'chest_pain_2'):
            warnings, min_urgency = self._chest_pain_2(triage_request, warnings, min_urgency)

        if self._apply_rule_for_hospital(triage_request.hospital, 'febrile_infant'):
            warnings, min_urgency = self._febrile_infant(triage_request, warnings, min_urgency)

        if self._apply_rule_for_hospital(triage_request.hospital, 'febrile_neutroenia'):
            warnings, min_urgency = self._febrile_neutroenia(triage_request, warnings, min_urgency)

        if self._apply_rule_for_hospital(triage_request.hospital, 'mental_health_pathway'):
            warnings, min_urgency = self._mental_health_pathway(triage_request, warnings, min_urgency)

        if self._apply_rule_for_hospital(triage_request.hospital, 'neutropenic_pathway'):
            warnings, min_urgency = self._neutropenic_pathway(triage_request, warnings, min_urgency)

        if self._apply_rule_for_hospital(triage_request.hospital, 'asthma_adult'):
            warnings, min_urgency = self._asthma_adult(triage_request, warnings, min_urgency)

        if self._apply_rule_for_hospital(triage_request.hospital, 'hip_fracture'):
            warnings, min_urgency = self._hip_fracture(triage_request, warnings, min_urgency)

        if self._apply_rule_for_hospital(triage_request.hospital, 'paediatric_oncology'):
            warnings, min_urgency = self._paediatric_oncology(triage_request, warnings, min_urgency)

        return warnings, min_urgency

    def _apply_rule_for_hospital(self, hospital: str, warning: str) -> bool:
        """
        """
        if [x for x in [hospital, 'all_hospitals'] if x in self.red_flags[warning]]:
            return True
        return False
        
    def _sepsis(self, triage_request, warnings, min_urgency) -> Tuple[list, int]:
        """
        """
        if triage_request.age_in_months >= (self.adult_age * 12):
            ## TODO need to come back and add some way to account for a source of
            # infection + how to add emphisas for there being a CPC that could
            # indicate sepsis eg fever symptoms, etc etc
            sepsis_indicators = []            

            if triage_request.temperature and (triage_request.temperature >= 38):
                sepsis_indicators.append('Fever; {}°C'.format(triage_request.temperature))
            if triage_request.temperature and (triage_request.temperature <= 36):
                sepsis_indicators.append('Fever; {}°C'.format(triage_request.temperature))
            if triage_request.vital_signs_pulse and (triage_request.vital_signs_pulse >= 100):
                sepsis_indicators.append('Tachycardia; pulse of {}'.format(triage_request.vital_signs_pulse))
            if triage_request.respiratory_rate and (triage_request.respiratory_rate > 20):
                sepsis_indicators.append('Tachypnoea; rr of {}'.format(triage_request.respiratory_rate))
            if triage_request.blood_pressure_systolic and (triage_request.blood_pressure_systolic < 90):
                sepsis_indicators.append('Hypotension; systolic bp {}'.format(triage_request.blood_pressure_systolic))
            if triage_request.immunocompromised:
                sepsis_indicators.append('Immunocompromised')
            if len(sepsis_indicators) > 0:
                if ((triage_request.presenting_complaint == 'Fever symptoms') | 
                    (triage_request.presenting_complaint == 'Altered mental state/confusion') | 
                    (triage_request.presenting_complaint == 'General weakness/fatigue/unwell') |
                    (triage_request.presenting_complaint == 'Shortness of breath') |
                    (triage_request.presenting_complaint == 'UTI symptoms')) :
                    """
                    Check for CPC here, if there are
                    """
                    sepsis_indicators.append(triage_request.presenting_complaint)

            if len(sepsis_indicators) > 1:
                sepsis_warning = '{} SEPSIS INDICATORS: '.format(len(sepsis_indicators))
                for indicator in sepsis_indicators:
                    sepsis_warning += indicator + '. '
                sepsis_warning += 'Are there other sepsis indicators or a source of infection?'
                
                warnings.append(sepsis_warning)
                min_urgency = min(min_urgency, 2)
        return warnings, min_urgency

    def _chest_pain_2(self, triage_request, warnings, min_urgency) -> Tuple[list, int]:
        """
        """
        if triage_request.presenting_complaint == 'Chest pain':
            min_urgency = min(min_urgency, 2)
            warnings.append('Consider chest pain pathway if non-cardiac cause of pain cannot be established')
        return warnings, min_urgency

    def _mental_health_pathway(self, triage_request, warnings, min_urgency) -> Tuple[list, int]:
        """
        """
        if (triage_request.presenting_complaint_group == 'MENTAL HEALTH') or \
            triage_request.presenting_complaint == 'Overdose of drug' or \
            triage_request.mental_health_concerns:
            warnings.append('Consider mental health pathway.')
        return warnings, min_urgency

    def _neutropenic_pathway(self, triage_request, warnings, min_urgency) -> Tuple[list, int]:
        """
        """
        #TODO check chemo type keywords
        if triage_request.immunocompromised:
            warnings.append('Consider neutropenic pathway.')
        return warnings, min_urgency

    def _asthma_adult(self, triage_request, warnings, min_urgency) -> Tuple[list, int]:
        """
        """
        #TODO add checks for asthma keywords
        if (self.adult_age <= (triage_request.age_in_months/12) <= 60) \
            and triage_request.presenting_complaint == 'Shortness of breath':
            warnings.append('Consider asthma adult pathway')
        return warnings, min_urgency

    def _hip_fracture(self, triage_request, warnings, min_urgency) -> Tuple[list, int]:
        """
        """
        #TODO add checks for hip/pelvis and injury/fracture keywords
        if triage_request.presenting_complaint == 'Injury of hip':
            warnings.append('Consider hip fracture pathway')
        return warnings, min_urgency

    def _paediatric_oncology(self, triage_request, warnings, min_urgency) -> Tuple[list, int]:
        """
        """
        #TODO add checks for chemo type keywords
        if (triage_request.age_in_months/12) < self.adult_age and \
            triage_request.immunocompromised == 1:
            warnings.append('Consider paediatric oncology pathway')
        return warnings, min_urgency

    def _febrile_infant(self, triage_request, warnings, min_urgency):
        return warnings, min_urgency

    def _febrile_neutroenia(self, triage_request, warnings, min_urgency):
        return warnings, min_urgency
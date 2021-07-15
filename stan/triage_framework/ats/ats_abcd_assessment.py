"""
"""

from typing import Tuple

from ...core.triage_request import TriageRequest
from ...core.triage_rules import get_triage_rules_template


def ats_abcd_assessment(
    triage_request: TriageRequest, 
    adult_age: int = 17
    ) -> Tuple[dict, int]:
    """
    Assesses a triage presentations airway, breathing circulation and disability 
    as per general rules in the Australiasian Triage Scale.

    Returns:
        - triage_rules: dictionary of triage rules for each triage code wrt to 
        ats vital sign guidelines
        - min_urgency: the minimal triage code the triage framework insists for 
        the given presentation wrt to ats vital sign guidelines
    """
    if adult_age <= (triage_request.age_in_months/12):
        abcd_rules, abcd_urgency = ats_abcd_adult(triage_request)
    else:
        abcd_rules, abcd_urgency = ats_abcd_paediatric(triage_request)
    return abcd_rules, abcd_urgency


def ats_abcd_adult(triage_request) -> Tuple[dict, int]:
    """
    """
    abcd_urgency = 5
    abcd_rules = get_triage_rules_template()
    if triage_request.airway_altered:
        if triage_request.airway_was_measured:
            abcd_urgency = min(abcd_urgency, 2)
        abcd_rules['Code1'] += ['Immediate risk to airway - impending arrest']
        abcd_rules['Code2'] += ['Airway risk-severe stridor or drooling with distress']
        abcd_rules['Code3'] += ['Patent airway']
        abcd_rules['Code4'] += ['Patent airway']
        abcd_rules['Code5'] += ['Patent airway']
    if triage_request.breathing_altered:
        if triage_request.breathing_was_measured:
            abcd_urgency = min(abcd_urgency, 3)
        abcd_rules['Code1'] += [
            'Severe respiratory distress',
            'Severe use of accessory muscles, unable to speak',
            'Central cyanosis; altered conscious state'
            ]
        abcd_rules['Code2'] += [
            'Moderate respiratory distress',
            'Moderate use of accessory muscles, speaking in words',
            'Skin pale; peripheral cyanosis'
            ]
        abcd_rules['Code3'] += [
            'Mild respiratory distress',
            'Minimal use of accessory muscles, speaking in short sentences',
            'Skin pink'
            ]
        abcd_rules['Code4'] += [
            'Nil respiratory distress',
            'Speaking full sentences',
            ]
        abcd_rules['Code5'] += [
            'Nil respiratory distress',
            'Speaking full sentences',
            ]
    if triage_request.circulation_altered:
        abcd_rules['Code1'] += [
            'Severe shock',
            'Absent peripheral pulses; skin pale moist, and cool',
            'Uncontrolled bleeding'
            ]
        abcd_rules['Code2'] += [
            'Moderate shock',
            'Abnormal peripheral pulses; skin pale, moist and cool',
            'Severe blood loss',
            'Clammy or mottled skin, poor perfusion',
            'Hypotension with haemodynamic effects'
            ]
        abcd_rules['Code3'] += [
            'Mild shock',
            'Palpable peripheral pulses; skin pale, cool and dry',
            'Moderate blood loss'
            ]
        abcd_rules['Code4'] += [
            'Nil signs of shock',
            'Palpable peripheral pulses',
            'Skin pink warm and dry'
            ]
        abcd_rules['Code5'] += [
            'Nil signs of shock',
            'Palpable peripheral pulses',
            'Skin pink warm and dry'
            ]
    if triage_request.disability_gcs <= 12:
        abcd_rules['Code1'] += [
            'Unresponsive or responds to pain only (GCS<9)',
            'Current seizure activity'
            ]
        abcd_rules['Code2'] += ['Drowsy, decreased responsiveness any cause (GCS<13)']
        if triage_request.disability_gcs <= 9 and triage_request.disability_gcs_was_measured:
            abcd_urgency = 1
        elif triage_request.disability_gcs <= 12 and triage_request.disability_gcs_was_measured:
            abcd_urgency = min(abcd_urgency, 2)
    return abcd_rules, abcd_urgency


def ats_abcd_paediatric(triage_request) -> Tuple[dict, int]:
    """
    """
    abcd_urgency = 5
    abcd_rules = get_triage_rules_template()
    if triage_request.airway_altered:
        if triage_request.airway_was_measured:
            abcd_urgency = min(abcd_urgency, 3)
        abcd_rules['Code1'] += [
            'Immediate risk to airway - impending arrest',
            'Obstructed or partially obstructed with severe respiratory distress'
            ]
        abcd_rules['Code2'] += [
            'Airway risk - biphasic stridor',
            'Moderate respiratory distress'
            ]
        abcd_rules['Code3'] += ['Stridor with mild respiratory distress']
        abcd_rules['Code4'] += ['Patent airway']
        abcd_rules['Code5'] += ['Patent airway']
    if triage_request.breathing_altered:
        if triage_request.breathing_was_measured:
            abcd_urgency = min(abcd_urgency, 3)
        abcd_urgency = min(abcd_urgency, 4)
        abcd_rules['Code1'] += [
            'Respiratory arrest; hypoventilation; extreme respiratory distress',
            'Extreme use of accessory muscles, extreme retractions',
            'Unable to speak; central cyanosis'
            ]
        abcd_rules['Code2'] += [
            'Respiration present; Abnormal Respiratory rate',
            'Severe respiratory distress',
            'Severe use of accessory muscles, severe retractions',
            'Speaking in single words; skin pale, peripheral cyanosis'
            ]
        abcd_rules['Code3'] += [
            'Respiration present; abnormal RR',
            'Moderate respiratory distress',
            'Moderate use of accessory muscles, moderate retractions',
            'Speaking in short sentences; skin pink'
            ]
        abcd_rules['Code4'] += [
            'Respiration present; Mild respiratory distress',
            'Mild use of accessory muscles, no retractions',
            'Speaking in full sentences'
            ]
        abcd_rules['Code5'] += [
            'Respiration present; Nil respiratory distress',
            'Nil use of accessory muscles, no retractions',
            'Speaking in full sentences'
            ]
    if triage_request.circulation_altered:
        abcd_rules['Code1'] += [
            'Cardiac arrest; significant bradycardia ie HR < 60 in an infant',
            'Severe haemodynamic compromise; tachycardia, absent peripheral pulses',
            'Skin pale, moist, cool, mottled; capillary refill > 4 seconds',
            'Uncontrolled bleeding'
            ]
        abcd_rules['Code2'] += [
            'Circulation present; moderate haemodynamic compromise',
            'Tachycardia, weak thready peripheral pulse',
            'Skin pale cool; signs of severe dehydration',
            'Capillary refill less than 2 seconds',
            'Clammy or mottled skin, poor perfusion',
            'Hypotension with haemodynamic effects'
            ]
        abcd_rules['Code3'] += [
            'Circulation present; mild haemodynamic compromise',
            'Tachycardia, palpable peripheral pulse',
            'Skin pale warm; signs of moderate dehydration',
            'Capillary refill less than 2 seconds'
            ]
        abcd_rules['Code4'] += [
            'Circulation present; no haemodynamic compromise',
            'No tachycardia, palpable peripheral pulses',
            'Skin pink warm and dry; signs of mild dehydration',
            'Normal capillary refill'
            ]
        abcd_rules['Code5'] += [
            'Circulation present; no haemodynamic compromise',
            'No tachycardia; skin pink warm and dry',
            'Clinically hydrated; normal capillary refill'
            ]
    if triage_request.disability_gcs <= 12:
        abcd_rules['Code1'] += [
            'Unresponsive or responds to pain only (GCS<9)',
            'Ongoing seizure activity'
            ]
        abcd_rules['Code2'] += [
            'Severe decrease in activity',
            'No eye contact; decreased muscle tone, lethargy'
            ]
        if triage_request.disability_gcs <= 8:
            abcd_urgency = 1
        elif triage_request.disability_gcs <= 10:
            abcd_urgency = min(abcd_urgency, 2)
        elif triage_request.disability_gcs <= 12:
            abcd_urgency = min(abcd_urgency, 3)
            
    return abcd_rules, abcd_urgency
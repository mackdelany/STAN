"""
"""

from typing import Tuple

from ...core.triage_request import TriageRequest
from ...core.triage_rules import combine_triage_rule_dicts, get_triage_rules_template


def ats_general_assessment(
    triage_request: TriageRequest,
    adult_age: int = 17,
    min_urgency: int = 5
) -> Tuple[dict, int]:
    """
    Assesses a triage presentations as per general rules in the Australiasian
    Triage Scale.

    Returns:
        - triage_rules: dictionary of triage rules for each triage code wrt to
        ats vital sign guidelines
        - min_urgency: the minimal triage code the triage framework insists for
        the given presentation wrt to ats vital sign guidelines
    """
    gen_rules, gen_urgency = ats_general(triage_request, adult_age)
    complaint_rules, complaint_urgency = ats_complaints(
        triage_request, adult_age)
    mental_health_rules, mental_health_urgency = ats_mental_health(
        triage_request)
    neuro_rules, neuro_urgency = ats_neuro(triage_request)
    eye_rules = ats_opthalmology(triage_request, adult_age)
    pain_rules = ats_pain(triage_request, adult_age)
    triage_rules = combine_triage_rule_dicts(
        gen_rules,
        complaint_rules,
        mental_health_rules,
        neuro_rules,
        eye_rules,
        pain_rules
    )
    min_urgency = min(
        gen_urgency,
        complaint_urgency,
        mental_health_urgency,
        neuro_urgency
    )
    return triage_rules, min_urgency


def ats_general(triage_request, adult_age):
    """
    """
    gen_urgency = 5
    gen_rules = get_triage_rules_template()

    if triage_request.age_in_months < 4:
        gen_urgency = min(gen_urgency, 3)
        gen_rules['Code3'] += ['Stable neonate']

    return gen_rules, gen_urgency


def ats_complaints(triage_request, adult_age):
    """
    """
    complaint_urgency = 5
    complaint_rules = get_triage_rules_template()

    # singles, can be if, elif, else
    if triage_request.presenting_complaint == 'Cardiac arrest':
        complaint_rules['Code1'] += ['Cardiac arrest']
        complaint_urgency = 1
    elif triage_request.presenting_complaint == 'Cardiac arrest due to trauma':
        complaint_rules['Code1'] += ['Cardiac arrest due to trauma']
        complaint_urgency = 1
    elif triage_request.presenting_complaint == 'Respiratory arrest':
        complaint_rules['Code1'] += ['Respiratory arrest']
        complaint_urgency = 1
    elif triage_request.presenting_complaint == 'Seizure':
        complaint_rules['Code1'] += ['Ongoing/prolonged seizure']
        complaint_rules['Code3'] += ['Seizure (now alert)']
    elif triage_request.presenting_complaint == 'Overdose of drug':
        complaint_rules['Code1'] += ['IV overdose and unresponsive or hypoventilation']
    elif triage_request.presenting_complaint == 'Multiple injuries - major':
        complaint_rules['Code2'] += [
            'Major multi trauma (requiring rapid organised team response )']
        complaint_urgency = min(complaint_urgency, 2)
    elif triage_request.presenting_complaint == 'Fever symptoms':
        complaint_rules['Code2'] += [
            'Fever with significant lethargy (any age)']
    elif triage_request.presenting_complaint == 'Shortness of breath':
        complaint_rules['Code3'] += ['Moderate shortness of breath']
    elif triage_request.presenting_complaint == 'Injury of head' \
            or 'concussion' in triage_request.presenting_complaint.lower() \
            or (triage_request.triage_assessment and (
                'head' in triage_request.triage_assessment.lower() and 'injury' in triage_request.triage_assessment.lower())
                )\
            or (triage_request.triage_assessment and 'concussion' in triage_request.triage_assessment.lower()):
        complaint_rules['Code3'] += ['Head injury with short LOC - now alert']
        complaint_rules['Code4'] += ['Minor head injury, no loss of consciousness']
        complaint_urgency = min(complaint_urgency, 4)
    elif triage_request.presenting_complaint == 'Injury of chest':
        complaint_rules['Code3'] += ['Chest injury without rib pain or respiratory distress']
        complaint_urgency = min(complaint_urgency, 4)
    elif triage_request.presenting_complaint == 'Abdominal pain':
        complaint_rules['Code3'] += ['Abdominal pain without high risk features - mod severity']
        complaint_rules['Code4'] += ['Non specific abdominal pain']
    elif triage_request.presenting_complaint == 'Altered sensation':
        complaint_rules['Code3'] += ['Limb-altered sensation, acutely absent pulse']
    elif triage_request.presenting_complaint == 'Swallowing problem':
        complaint_rules['Code4'] += ['Difficulty swallowing, no respiratory distress']
    elif triage_request.presenting_complaint == 'Male genital problem':
        complaint_rules['Code2'] += ['Testicular torsion']

    # multiples, should be if, if, if
    if triage_request.presenting_complaint in ['Chest pain', 'Palpitations', 'Shortness of breath']:
        complaint_rules['Code2'] += ['Chest pain of likely cardiac nature']
    if triage_request.presenting_complaint in ['Weakness of face muscles', 'Weakness of limb']:
        complaint_rules['Code2'] += ['Acute hemiparesis/dysphagia']
    if triage_request.presenting_complaint in [
        'Rash', 'Fever symptoms', 'Altered mental state/confusion'
    ]:
        complaint_rules['Code2'] += ['Suspected meningococcaemia']
    if triage_request.presenting_complaint in [
        'Nausea/vomiting/diarrhoea', 'Vomiting blood', 'General weakness/fatigue/unwell'
    ]:
        complaint_rules['Code3'] += ['Persistant vomiting']
        complaint_rules['Code4'] += ['Vomiting or diarrhoea without dehydration']
    if triage_request.presenting_complaint in ['Injury of lower limb', 'Injury of upper limb']:
        complaint_rules['Code3'] += [
            'Moderate limb injury - deformity, severe laceration, crush',
            'Limb-altered sensation, acutely absent pulse'
        ]
    if 'Foreign body' in triage_request.presenting_complaint:
        complaint_rules['Code4'] += ['Foreign body aspiration, no respiratory distress']
        complaint_urgency = min(complaint_urgency, 4)
    if triage_request.presenting_complaint in ['Change of dressing', 'Plaster cast problem']:
        complaint_rules['Code4'] += ['Tight cast, no neurovascular impairment']
    if triage_request.presenting_complaint in [
        'Swollen legs (both)', 'Swollen leg (single)', 'Swelling of joint (no recent injury)'
    ]:
        complaint_rules['Code4'] += ["Swollen 'hot' joint"]
    if triage_request.presenting_complaint in [
        'Weakness of face muscles', 'Weakness of limb', 'Altered mental state/confusion',
        'Visual disturbance', 'Speech problem'
    ]:
        complaint_rules['Code2'] += ['Acute stroke']

    # complaint groups
    if triage_request.presenting_complaint == 'TRAUMA/INJURY':
        complaint_rules['Code2'] += ['Severe localised trauma-major fracture, amputation']
        complaint_rules['Code3'] += [
            'Trauma - high risk history with no other high-risk features']
        complaint_rules['Code4'] += [
            'Minor limb trauma - sprained ankle, possible fracture, uncomplicated laceration',
            'Injury with normal vital signs, low/moderate pain'
        ]

    # multi conditionals
    if triage_request.presenting_complaint == 'Abdominal pain' and (triage_request.age_in_months/12) >= 65:
        complaint_urgency = min(complaint_urgency, 3)
        complaint_rules['Code3'] += ['Abdominal pain with patient over 65']
    if triage_request.presenting_complaint_group in ['TRAUMA/INJURY', 'SKIN'] and (triage_request.age_in_months/12) < adult_age:
        complaint_rules['Code3'] += ['Child at risk of abuse/suspected non accidental injury']
    if triage_request.presenting_complaint == 'Fever symptoms' and triage_request.immunocompromised:
        complaint_rules['Code2'] += ['Fever and immunocompromised']
        if triage_request.immunocompromised_was_measured:
            complaint_urgency = min(complaint_urgency, 2)
    if triage_request.presenting_complaint == 'Fever symptoms' and triage_request.age_in_months <= 12:
        complaint_rules['Code2'] += ['Fever in child less than 1 year old']

    return complaint_rules, complaint_urgency


def ats_mental_health(triage_request):
    """
    """
    mental_health_urgency = 5
    mental_health_rules = get_triage_rules_template()
    if triage_request.presenting_complaint in [
        'Aggressive behaviour',
        'Abnormal behaviour',
        'Altered mental state/confusion',
        'Aggressive behaviour',
        'Mental health problem',
        'Situational crisis',
        'Suicidal thoughts',
        'Anxiety',
        'Self harm',
        'Insomnia',
        'Overdose of drug'
    ] or triage_request.presenting_complaint_group == 'MENTAL HEALTH'\
            or triage_request.mental_health_concerns:
        mental_health_rules['Code1'] += [
            'Severe behavioral disorder with immediate threat of dangerous violence',
            'Self destruction in ED'
        ]
        mental_health_rules['Code2'] += [
            'Violent or aggresive behaviour',
            'Immediate threat to self or others',
            'Self-harm with suicidal intent',
            'Requires or has required restraint',
            'Severe agitation or aggression'
        ]
        mental_health_rules['Code3'] += [
            'Acutely psychotic or thought disordered',
            'Situational crises, risk of self harm',
            'Agitated/withdrawn/potentially aggressive',
            'Unable to wait safely'
        ]
        mental_health_rules['Code4'] += [
            'Semi-urgent mental health problem',
            'Under observation and/or no immediate risk to self or others',
            'Willing to wait'
        ]
        mental_health_rules['Code5'] += [
            'Known patient with chronic symptoms',
            'Social crisis, clinically well patient'
        ]
    return mental_health_rules, mental_health_urgency


def ats_neuro(triage_request):
    """
    """
    neuro_urgency = 5
    neuro_rules = get_triage_rules_template()
    if triage_request.neuro_altered:
        neuro_urgency = 4
        neuro_rules['Code2'] += [
            'Severe neurovascular compromise',
            'Pulseless, cold, altered sensation',
            'Delayed capillary refill'
        ]
        neuro_rules['Code3'] += [
            'Moderate neurovascular compromise',
            'Pulse present, cool, altered sensation',
            'Delayed capillary refill'
        ]
        neuro_rules['Code4'] += [
            'Mild neurovascular compromise',
            'Pulse present, warm, normal or altered sensation',
            'Normal capillary refill'
        ]
        neuro_rules['Code5'] += ['No neurovascular compromise']
    return neuro_rules, neuro_urgency


def ats_opthalmology(triage_request, adult_age):
    """
    """
    eye_rules = get_triage_rules_template()
    if any(x in triage_request.presenting_complaint for x in ['Eye', 'eye']):
        eye_rules['Code2'] += [
            'Chemical or penetrating eye injury',
            'Sudden loss of vision with or without injury',
            'Sudden severe eye pain',
            'Sudden onset pain, blurred vision and red eye',
            'Suspected endophthalmitis post eye procedure'
        ]
        eye_rules['Code3'] += [
            'Sudden abnormal vision with or without eye injury',
            'Moderate eye pain'
        ]
        eye_rules['Code4'] += [
            'Normal vision; mild eye pain',
            'Eye inflammation or foreign body - normal vision'
        ]
        eye_rules['Code5'] += [
            'Normal vision; no eye pain'
        ]
    if triage_request.presenting_complaint in ['Chemical exposure', 'Foreign body in eye']:
        eye_rules['Code2'] += ['Acid or alkali splash to eye-requiring irrigation']
    return eye_rules


def ats_pain(triage_request, adult_age):
    """
    """
    pain_rules = get_triage_rules_template()
    if triage_request.pain_was_measured:
        if adult_age <= (triage_request.age_in_months/12):     # adult
            pain_rules['Code2'] += ['Severe pain']
            pain_rules['Code3'] += ['Moderate pain']
            pain_rules['Code4'] += ['Mild pain']
            pain_rules['Code5'] += ['No pain']
        else:                                                   # paediatric
            pain_rules['Code2'] += ['Patient/parent report severe pain']
            pain_rules['Code3'] += ['Patient/parent report moderate pain']
            pain_rules['Code4'] += ['Patient/parent report mild pain']
            pain_rules['Code5'] += ['Patient/parent report no pain']
    return pain_rules

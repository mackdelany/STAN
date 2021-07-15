"""
"""

def get_triage_rules_template() -> dict:
    """
    Returns a blank triage rules template.

    #TODO should this be a class?
    """
    triage_rules = {
        'Code1' : [],
        'Code2' : [],
        'Code3' : [],
        'Code4' : [],
        'Code5' : []
        }
    return triage_rules

def combine_triage_rule_dicts(*args: dict):
    """
    Combines multiple triage rule dictionaries.
    """
    triage_rules = get_triage_rules_template()
    for dict_to_add in args:
        triage_rules['Code1'] += dict_to_add['Code1']
        triage_rules['Code2'] += dict_to_add['Code2']
        triage_rules['Code3'] += dict_to_add['Code3']
        triage_rules['Code4'] += dict_to_add['Code4']
        triage_rules['Code5'] += dict_to_add['Code5']
    return triage_rules
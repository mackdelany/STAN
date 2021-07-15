"""
TriageModel is STAN's assessment of a triage presentation, this will include AI assessments for:
- triage code
- sepsis risk

If not given in original request, then the following fields will also be assessed by AI:
- airway altered
- breathing altered
- circulation altered
- disability altered
- neuro altered
- immunocompromised
- mental health concerns


can this be done by TriageRequest ?
"""
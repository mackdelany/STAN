"""
"""

from collections import namedtuple

StanReponse = namedtuple(
    'StanResponse',
        [
        'triage_code',
        'prediction_distribution',
        'triage_rules',
        'ews_type',
        'ews_est',
        'ews_message',
        'warnings'
        ]
    )
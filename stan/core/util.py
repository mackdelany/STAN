"""
"""

import re

def remove_non_numbers(string):
    """Removes non numbers from a string.
    """
    numbers = re.sub('[^0-9]','', string)
    return numbers

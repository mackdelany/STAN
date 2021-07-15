"""
DEPRECATED
"""

import json
from functools import wraps
from flask import current_app, request

from ..core.exceptions import APIKeyError


def check_api_key(function):
    """
    """
    @wraps(function)
    def authenticated_function(*args, **kwargs):
        if current_app.config['ENV'] == 'production':
            if 'Key' in request.headers:
                if request.headers['Key'] in current_app.config['AUTH_KEYS'].values():
                    print('Request authenticated\n')
                    return function(*args, **kwargs)
                else:
                    print('Invalid API key\n')
                    error = APIKeyError('Invalid API key')
                    error_message = error.create_error_payload()
                    return error_message, 401 
            else :
                print('No API key in request\n')
                error = APIKeyError('No API key in request')
                error_message = error.create_error_payload()
                return error_message, 401
        else:
            print('Not production env. API not secured.\n')
            return function(*args, **kwargs)
    return authenticated_function
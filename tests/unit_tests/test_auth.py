
import json

from fixtures import app, integration_requests, prod_api_key, dev_client, prod_client_test


def test_auth(dev_client, prod_client_test, integration_requests, prod_api_key):
    test_request = integration_requests['request_3']

    authorized_prod = prod_client_test.post(
        '/predict-testing', json=test_request, headers={'Key': prod_api_key}
        )
    authorized_prod = json.loads(authorized_prod.data)

    authorized_dev = dev_client.post(
        '/predict-testing', json=test_request, headers={'Key': prod_api_key}
        )
    authorized_dev = json.loads(authorized_dev.data)

    no_key_prod = prod_client_test.post(
        '/predict-testing', json=test_request
        )
    no_key_prod = json.loads(no_key_prod.data)

    wrong_key_prod = prod_client_test.post(
        '/predict-testing', json=test_request, headers={'Key': 'this is the wrong key'}
        )
    wrong_key_prod = json.loads(wrong_key_prod.data)

    assert authorized_prod['triage_code'] == authorized_dev['triage_code'] 
    assert no_key_prod['error_type'] == 'APIKeyError'
    assert no_key_prod['message'] == 'No API key in request'
    assert wrong_key_prod['error_type'] == 'APIKeyError'
    assert wrong_key_prod['message'] == 'Invalid API key'
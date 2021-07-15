
import json

from fixtures import dev_client, warning_requests


def test_stan_warnings(dev_client, warning_requests):
    #TODO add checks for different hospitals....

    for presentation in warning_requests:
        payload = dev_client.post('/predict-testing', json=warning_requests[presentation]['Request'])
        response = json.loads(payload.data)
        string_to_check = warning_requests[presentation]['StringToCheck']
        assert any([string_to_check in warning for warning in response['warnings']])
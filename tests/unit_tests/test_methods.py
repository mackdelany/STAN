
from bs4 import BeautifulSoup
import json

from fixtures import dev_client, integration_requests


def test_response_types(dev_client, integration_requests):
    """
    """
    for presentation in integration_requests:
        predict_response = dev_client.post(
            '/predict-testing', json=integration_requests[presentation]
            )
        predict_data = json.loads(predict_response.data)
        assert isinstance(predict_data, dict)
        
        triage_response = dev_client.post(
            '/triage-testing', json=integration_requests[presentation]
            )
        assert bool(BeautifulSoup(triage_response.data, "html.parser").find())


def test_distributions(dev_client, integration_requests):
    for presentation in integration_requests:
        predict_response = dev_client.post(
            '/predict-testing', json=integration_requests[presentation]
            )
        predict_data = json.loads(predict_response.data)
        if predict_data['triage_code'] > 1:
            assert len(set(predict_data['prediction_distribution'])) > 10


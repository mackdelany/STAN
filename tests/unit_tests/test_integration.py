
import json
import sys
from builtins import all, any
from pathlib import Path

import pytest

sys.path.append(str(Path.cwd().parent))

from fixtures import app, integration_requests, prod_api_key, prod_client, prod_client_test

        
@pytest.fixture
def requests():
    """
    """
    with open("tests/integration_test_requests.json", "r") as read_file:
        return json.load(read_file)


def test_predict(prod_client_test, integration_requests, prod_api_key):
    """
    """
    response_1 = prod_client_test.post(
        '/predict-testing', 
        json=integration_requests['request_1'],
        headers={'Key': prod_api_key}
        )
    stan_prediction_1 = json.loads(response_1.data)

    response_2 = prod_client_test.post(
        '/predict-testing', 
        json=integration_requests['request_2'],
        headers={'Key': prod_api_key}
        )
    stan_prediction_2 = json.loads(response_2.data)

    if response_1.status_code != 200:
        print(stan_prediction_1['errors'])
    assert response_1.status_code == 200
    assert stan_prediction_1['triage_code'] >= 1
    assert stan_prediction_1['triage_code'] <= 5
    assert type(stan_prediction_1['prediction_distribution']) == list
    assert type(stan_prediction_1['triage_rules']) == dict
    assert any('mental health' in x for x in stan_prediction_1['triage_rules']['Code4'])

    if response_2.status_code != 200:
        print(stan_prediction_2['errors'])
    assert response_2.status_code == 200
    assert stan_prediction_2['triage_code'] <= 3
    assert type(stan_prediction_1['triage_rules']['Code1']) == list

    assert all(x <= 5  for x in stan_prediction_2['prediction_distribution'])
    assert all(x >= 1  for x in stan_prediction_2['prediction_distribution'])


def test_record(prod_client_test, integration_requests, prod_api_key):
    response = prod_client_test.post(
        '/record-testing', 
        json=integration_requests['request_3'],
        headers={'Key': prod_api_key}
        )
    assert response.status_code == 201
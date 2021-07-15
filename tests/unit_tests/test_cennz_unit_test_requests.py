"""
"""

import json
import os
from pathlib import Path
import sys

import pandas as pd
import pytest

from fixtures import app, cennz_requests, dev_client

## pretty print test results if needed
pd.options.display.width = 0
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def test_cennz_unit_test_requests(dev_client, cennz_requests, export_results=True):
    test_results = []
    for presentation in cennz_requests:
        payload = dev_client.post('/predict-testing', json=cennz_requests[presentation]['Request'])
        response = json.loads(payload.data)
        desired_code = cennz_requests[presentation]['Code']
        stan_code = response['triage_code']
        error = abs(desired_code - stan_code)
        test_results.append([
            presentation,
            cennz_requests[presentation]['Summary'],
            desired_code,
            round(stan_code, 2),
            round(error, 2)
            ])
    test_results = pd.DataFrame(
        test_results, 
        columns=['Presentation', 'Summary', 'Target', 'STAN', 'Error']
        )
    mae = round(test_results.Error.mean(), 2)
    accuracy = sum(test_results.Error < 0.5) / 20

    print(test_results)
    print('\nMAE: {}'.format(mae))
    print('\nClassification accuracy: {}'.format(accuracy))

    if export_results:
        test_results.to_csv('tests/cennz_unit_test_results.csv', index=False)

    assert (mae < 0.4)
    assert (accuracy >= 0.75)

    

import json
import datetime

from dateutil import parser as dateutil_parser
from dateutil.relativedelta import relativedelta

from fixtures import cennz_requests, dev_client
from stan.core.timezones import naive_dt_to_aware, utcnow


def test_early_warning_score(dev_client, cennz_requests):
    """
    """
    def adjust_dob(present_date_time, dob):
        """
        """
        present_date_time = dateutil_parser.parse(present_date_time)
        dob = dateutil_parser.parse(dob)
        present_date_time = naive_dt_to_aware(present_date_time, 'UTC')
        dob = naive_dt_to_aware(dob, 'UTC')

        new_dob = utcnow() - relativedelta(present_date_time, dob)
        new_dob_str = str(new_dob)
        return new_dob_str

    for presentation in cennz_requests.keys():
        cennz_requests[presentation]['Request']['DOB'] = adjust_dob(
            cennz_requests[presentation]['Request']['PresentDateTime'],
            cennz_requests[presentation]['Request']['DOB']
            )

        desired_ews_type = cennz_requests[presentation]['EWS']['Type']
        desired_ews_estimate = cennz_requests[presentation]['EWS']['Estimated']

        payload = dev_client.post('/predict-testing', json=cennz_requests[presentation]['Request'])
        response = json.loads(payload.data)
        ews_type = response['early_warning_score']['type']
        ews_estimate = response['early_warning_score']['estimated']

        assert desired_ews_type == ews_type
        assert desired_ews_estimate == ews_estimate
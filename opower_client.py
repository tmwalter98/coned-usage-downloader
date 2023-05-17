import httpx

from datetime import date, timedelta
import httpx
import dateutil.parser
from datetime import timedelta
import json


def datetime_parser(json_dict: dict) -> dict:
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = dateutil.parser.parse(value)
        except Exception:
            pass
    return json_dict


class OpowerClient(httpx.Client):
    def __init__(self, customer_uuid: str, bearer_token: str):
        super().__init__(
            base_url='https://cned.opower.com/ei/edge/apis',
            headers={
                'Authorization': f'Bearer {bearer_token}',
                'Host': 'cned.opower.com',
            })
        self.customer_uuid = customer_uuid

    def get_service_accounts(self, fuel_type: str = 'ELECTRICITY'):
        res = self.get(
            f'/DataBrowser-v1/cws/metadata',
            params={
                'preferredUtilityAccountIdType': 'UTILITY_ACCOUNT_ID_2',
                'includeCommercialAndIndustrial': 'true',
                'customerUuid': self.customer_uuid,
            }
        )
        res.raise_for_status()
        return json.loads(res.text, object_hook=datetime_parser)['fuelTypeServicePoint'][fuel_type]

    def get_readings(self, service_account_id: str, start_date: date, end_date: date):
        t0, t1 = start_date, start_date + timedelta(days=30)
        readings = []

        while t0 < end_date:
            res = self.get(
                f'/DataBrowser-v1/cws/utilities/cned/utilityAccounts/{service_account_id}/reads',
                params={
                    'startDate': t0.strftime("%Y-%m-%d"),
                    'endDate': t1.strftime("%Y-%m-%d"),
                    'aggregateType': 'quarter_hour',
                    'includeEnhancedBilling': 'false',
                    'includeMultiRegisterData': 'false',
                }
            )
            response_readings = res.json(
                object_hook=datetime_parser).get('reads')
            if len(response_readings) == 0:
                break
            else:
                readings.extend(response_readings)
            t0 = t0 + timedelta(days=30)
            t1 = t1 + timedelta(days=30)
        return readings

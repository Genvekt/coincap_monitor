import unittest
from unittest.mock import patch

import pytz
import etl
from config import APIConf
from datetime import datetime


class TestCoincapEtl(unittest.TestCase):

    def test_utc_to_local_tz(self):
        # UTC timestamp
        utc_time = datetime.utcnow()
        utc_aware_time = pytz.timezone("UTC").localize(utc_time)

        # Test UTC timezone (UTC+0)
        tz_time = etl.utc_to_local_tz(utc_time, "UTC")
        hour_diff = (utc_aware_time-tz_time).seconds
        self.assertEqual(hour_diff, 0)

        # Test Moscow timezone (UTC+3)
        tz_time = etl.utc_to_local_tz(utc_time, "Europe/Moscow")
        hour_diff = (utc_aware_time-tz_time).seconds
        self.assertEqual(hour_diff, 3*60*60)

        # Test Japan (UTC+9)
        tz_time = etl.utc_to_local_tz(utc_time, "Japan")
        hour_diff = (utc_aware_time-tz_time).seconds
        self.assertEqual(hour_diff, 9*60*60)

    def test_transform_coin_info(self):

        # Test - Nothing to change
        coin_info = {
            'id': 1234,
            'symbol': "X",
            'name': "excoin",
            'priceUsd': 780.03
        }

        trans_coin_info = etl.transform_coin_info(coin_info)
        self.assertDictEqual(coin_info, trans_coin_info)

        # Test - Emty input
        coin_info = {}

        trans_coin_info = etl.transform_coin_info(coin_info)
        self.assertDictEqual(coin_info, trans_coin_info)

        # Test - Delete unwanted keys
        coin_info = {
            'id': 1234,
            'symbol': "X",
            'name': "excoin",
            'priceUsd': 780.03,
            'some_key_1': "some_value",
            'some_key_2': 374637
        }

        clean_coin_info = {
            'id': 1234,
            'symbol': "X",
            'name': "excoin",
            'priceUsd': 780.03
        }

        trans_coin_info = etl.transform_coin_info(coin_info)
        self.assertDictEqual(clean_coin_info, trans_coin_info)

    def test_get_coin_current_info(self):
        def good_responce():
            return {
                'data': {
                    'id': '1234',
                    'symbol': "X",
                    'name': "excoin",
                    'priceUsd': 780.03
                }
            }

        with patch('etl.requests.get') as mocked_get:
            # ===============================================================
            # TEST - Good responce
            # Define the good responce from API
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.json = good_responce

            api_conf = APIConf(
                coin_id='1234',
                url='http://test.api',
                key='MY_SUPER_SECRET_KEY')
            # Call function that contains API call
            code, test_api_responce = etl.get_coin_current_info(api_conf)

            # Ensure api called with required parameters
            mocked_get.assert_called_with(
                url='http://test.api/assets/1234',
                headers={'Authorization': 'Bearer MY_SUPER_SECRET_KEY'}
            )

            # Check function behaviour
            self.assertEqual(code, 200)
            self.assertDictEqual(good_responce()['data'], test_api_responce)

            # ===============================================================
            # TEST - Bad responce
            # Define the bad responce from API
            mocked_get.return_value.status_code = 404

            api_conf = APIConf(
                coin_id='some_id',
                url='http://test.api',
                key='MY_SUPER_SECRET_KEY_2')

            # Call function that contains API call
            code, test_api_responce = etl.get_coin_current_info(api_conf)

            # Ensure api called with required parameters
            mocked_get.assert_called_with(
                url='http://test.api/assets/some_id',
                headers={'Authorization': 'Bearer MY_SUPER_SECRET_KEY_2'}
            )

            # Check function behaviour
            self.assertEqual(code, 404)
            self.assertDictEqual({}, test_api_responce)

            # ===============================================================
            # TEST - connection error
            # Define connection error situation
            mocked_get.side_effect = etl.requests.ConnectionError()

            api_conf = APIConf(
                coin_id='some_id_2',
                url='http://test_bad.api',
                key='MY_SUPER_SECRET_KEY_3')

            # Call function that contains API call
            code, test_api_responce = etl.get_coin_current_info(api_conf)

            # Ensure api called with required parameters
            mocked_get.assert_called_with(
                url='http://test_bad.api/assets/some_id_2',
                headers={'Authorization': 'Bearer MY_SUPER_SECRET_KEY_3'}
            )

            # Check function behaviour
            self.assertEqual(code, -1)
            self.assertDictEqual({}, test_api_responce)


if __name__ == "__main__":
    unittest.main()

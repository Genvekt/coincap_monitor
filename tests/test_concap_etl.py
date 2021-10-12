import unittest

import pytz
import coincap_monitor.coincap_etl as etl
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

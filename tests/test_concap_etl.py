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

    




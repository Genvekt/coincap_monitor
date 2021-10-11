from datetime import datetime
import os
import pytz
import logging
import requests
from typing import Optional

# Retrieve invironment variables

API_URL = 'http://api.coincap.io/v2'
API_KEY = os.environ.get('API_KEY')
LOCAL_TZ = os.environ.get('LOCAL_TZ')
COIN_ID = os.environ.get('COIN_ID')
LOG_FILE = os.environ.get('PIPELINE_LOG_FILE')

# Configure logger

logger = logging.getLogger(name=__name__)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


def get_utc_timestamp() -> datetime:
    """
    Get cuttent timestamp for UTC timezone

    Return: datetime object with current UTC time
    """
    return datetime.utcnow()


def utc_to_local_tz(utc_time: datetime, time_zone: str) -> datetime:
    """
    Convert UTC time to some time zone.

    Args:
        - utc_time: datetime object with UTC time
        - time_zone: time zone name

    Return: datetime object relative to time_zone
    """
    tz = pytz.timezone(time_zone)
    local_time = tz.localize(utc_time)
    return local_time


def get_coin_current_info(coin_id: str) -> Optional[dict]:
    """
    Retrieve the current information about coin from API

    Args:
        - coin_id (str): id of a coin withing API

    Returns: dict with all information if status_code
        of responce is 200, None otherwise
    """

    url = f"{API_URL}/assets/{coin_id}"
    payload = {}
    headers = {'Authorization': f'Bearer {API_KEY}'}

    responce = requests.request(
        method="GET", url=url,
        headers=headers, data=payload)

    if responce.status_code != 200:
        logger.warning(
            f"API returned status code {responce.status_code},\
            cannot retrieve answer.")
        return None

    return responce.json()['data']


def transform_coin_info(coin_info: dict) -> dict:
    """
    Clear API responce from unwanted information

    Args:
        - coin_info (dict): responce from API

    Return: clean dictionary withount unwanted keys
    """
    keys_of_interest = ('id', 'symbol', 'name', 'priceUsd')
    transformed_info = {
        key: value for key, value in coin_info.items()
        if key in keys_of_interest
    }
    return transformed_info


def run_etl_cycle():
    # ----------------
    # STEP 1: Extract
    # ----------------
    # Request information from API
    coin_info = get_coin_current_info(COIN_ID)
    # Get current Timestamp
    timestamp = get_utc_timestamp()
    timestamp = utc_to_local_tz(timestamp, LOCAL_TZ)

    # ------------------
    # STEP 2: Transform
    # ------------------
    # Clean the API responce
    trans_coin_info = transform_coin_info(coin_info)

    logger.debug(f"Cycle performed at {timestamp} -> {trans_coin_info} USD")
    print(f"Cycle performed at {timestamp} -> {trans_coin_info} USD")


if __name__ == "__main__":
    run_etl_cycle()

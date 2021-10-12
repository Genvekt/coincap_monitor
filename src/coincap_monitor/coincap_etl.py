from datetime import datetime
import pytz
import requests
from typing import Tuple


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


def get_coin_current_info(coin_id: str,
                          api_url: str,
                          api_key: str) -> Tuple[int, dict]:
    """
    Retrieve the current information about coin from API

    Args:
        - coin_id (str): id of a coin withing API

    Returns: dict with all information if status_code
        of responce is 200, None otherwise
    """

    url = f"{api_url}/assets/{coin_id}"
    payload = {}
    headers = {'Authorization': f'Bearer {api_key}'}

    try:
        responce = requests.get(
            url=url,
            headers=headers,
            data=payload)

    except requests.ConnectionError:
        return -1, {}

    if responce.status_code != 200:
        return responce.status_code, {}

    return responce.status_code, responce.json()['data']


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

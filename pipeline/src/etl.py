from datetime import datetime
import pytz
import requests
from typing import Tuple, Dict, Union
from src.config import APIConf


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


def get_coin_current_info(conf: APIConf) -> Tuple[int, Dict[str,str]]:
    """
    Retrieve the current information about coin from API

    Args:
        - conf (APIConf): api confiqurations

    Returns: dict with all information if status_code
        of responce is 200, None otherwise
    """

    url = f"{conf.url}/assets/{conf.coin_id}"
    headers = {'Authorization': f'Bearer {conf.key}'}

    try:
        responce = requests.get(
            url=url,
            headers=headers)

    except requests.ConnectionError:
        return -1, {}

    if responce.status_code != 200:
        return responce.status_code, {}

    return responce.status_code, responce.json()['data']


def transform_coin_info(coin_info: Dict[str,str]) -> Dict[str,Union[str, float]]:
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
    if 'priceUsd' in transformed_info:
        transformed_info['priceUsd'] = float(transformed_info['priceUsd'])
    return transformed_info


def prepare_for_insert(coin_info: dict, timestamp: datetime) -> \
        Tuple[str, str, str, float, datetime]:
    return (
        coin_info['id'],
        coin_info['symbol'],
        coin_info['name'],
        coin_info['priceUsd'],
        timestamp
    )


def get_coincap_insert_query() -> str:
    return '''
        INSERT INTO exchange (
            id,
            symbol,
            name,
            priceUsd,
            timestamp)
        VALUES
    '''


def get_coincap_create_query() -> str:
    return """
        CREATE TABLE IF NOT EXISTS exchange
        (
            id String,
            symbol String,
            name String,
            priceUsd Float32,
            timestamp DateTime('UTC')
        )
        ENGINE = MergeTree
        PARTITION BY toYYYYMMDD(timestamp)
        ORDER BY (timestamp)
    """

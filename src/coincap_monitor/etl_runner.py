import os
import logging
import coincap_monitor.coincap_etl as etl

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


def run_etl_cycle():
    # ----------------
    # STEP 1: Extract
    # ----------------
    # Request information from API
    status, coin_info = etl.get_coin_current_info(COIN_ID, API_URL, API_KEY)
    # Get current timestamp
    timestamp = etl.get_utc_timestamp()
    timestamp = etl.utc_to_local_tz(timestamp, LOCAL_TZ)

    if status != 200:
        logger.warning(
            f"API returned status code {status},\
            cannot retrieve answer.")

    # ------------------
    # STEP 2: Transform
    # ------------------
    # Clean the API responce
    trans_coin_info = etl.transform_coin_info(coin_info)

    logger.debug(f"Cycle performed at {timestamp} -> {trans_coin_info} USD")


if __name__ == "__main__":
    run_etl_cycle()

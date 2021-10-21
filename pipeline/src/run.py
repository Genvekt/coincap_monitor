import os
import logging
import clickhouse_driver

import src.etl as etl
from src.config import get_api_conf, get_warehouse_conf
from src.db import WarehouseConnection


# Retrieve invironment variables
LOG_FILE = os.getenv('PIPELINE_LOG_FILE', 'pipeline.log')

# Configure logger

logger = logging.getLogger(name=__name__)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


def run_etl_cycle() -> None:
    # ----------------
    # STEP 1: Extract
    # ----------------
    # Request information from API
    status, coin_info = etl.get_coin_current_info(get_api_conf())
    # Get current timestamp
    timestamp = etl.get_utc_timestamp()

    if status != 200:
        logger.warning(
            f"API returned status code {status},\
            cannot retrieve answer.")
        exit(0)

    with WarehouseConnection(get_warehouse_conf()).managed_client() as cli:
        # ------------------
        # STEP 2: Transform
        # ------------------
        # Clean the API responce
        trans_coin_info = etl.transform_coin_info(coin_info)
        # Make timezome aware timestamp
        timestamp = etl.utc_to_local_tz(timestamp, "UTC")

        # ------------------
        # STEP 3: Load
        # ------------------

        # Prepare data for unsertion
        insert_data = etl.prepare_for_insert(trans_coin_info, timestamp)
        # Get insert query
        insert_query = etl.get_coincap_insert_query()
        try:
            # Save data in the warehouse
            num_inserted = cli.execute(insert_query, [insert_data])

        # Handle database errors
        except clickhouse_driver.errors.ServerException as e:
            logger.warning(f"""
                    Warehouse server returned code {e.code}
                    with message '{e.message}' on query {insert_query}
                    with data {insert_data}""")
            if e.code == clickhouse_driver.errors.ErrorCodes.UNKNOWN_TABLE:
                # Solve 'table does to exists'
                logger.debug("Creating missing table...")
                create_query = etl.get_coincap_create_query()
                cli.execute(create_query)
                # Rerun the query
                num_inserted = cli.execute(insert_query, [insert_data])
            # Ignore other errors
            else:
                logger.debug("Unnown error, cannot fix.")
                num_inserted = 0

        logger.debug(f"Cycle performed at {timestamp} -> {insert_data}")
        logger.debug(f"Inserted {num_inserted} rows")


if __name__ == "__main__":
    run_etl_cycle()

import os
from dataclasses import dataclass


@dataclass
class WarehouseConfig:
    host: str
    port: int
    db: str
    user: str
    password: str
    local_tz: str


@dataclass
class APIConf:
    coin_id: str
    url: str
    key: str


def get_api_conf() -> APIConf:
    return APIConf(
        coin_id=os.getenv('COIN_ID', ''),
        url=os.getenv('API_URL', ''),
        key=os.getenv('API_KEY', '')
    )


def get_warehouse_conf() -> WarehouseConfig:
    return WarehouseConfig(
        host=os.getenv('CLICKHOUSE_HOST', ''),
        port=int(os.getenv('CLICKHOUSE_PORT', '9000')),
        db=os.getenv('CLICKHOUSE_DB', ''),
        user=os.getenv('CLICKHOUSE_USER', ''),
        password=os.getenv('CLICKHOUSE_PASSWORD', ''),
        local_tz=os.getenv('LOCAL_TZ', 'UTC'),
    )

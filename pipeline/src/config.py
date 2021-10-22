import os
from dataclasses import dataclass


@dataclass
class WarehouseConfig:
    host: str
    port: int
    db: str
    user: str
    password: str


@dataclass
class APIConf:
    coin_id: str
    url: str
    key: str


@dataclass
class StageDBConf:
    host: str
    port: int
    db: str
    user: str
    password: str


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
    )


def get_stagedb_conf() -> StageDBConf:
    return StageDBConf(
        host=os.getenv('STAGEDB_HOST', ''),
        port=int(os.getenv('STAGEDB_PORT', '27017')),
        db=os.getenv('STAGEDB_DB', ''),
        user=os.getenv('STAGEDB_USER', ''),
        password=os.getenv('STAGEDB_PASSWORD', ''),
    )

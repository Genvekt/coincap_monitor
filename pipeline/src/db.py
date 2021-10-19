from clickhouse_driver import Client
from contextlib import contextmanager
from config import WarehouseConfig


class WarehouseConnection:
    def __init__(self, conf: WarehouseConfig):
        self.client = Client(
            host=conf.host,
            port=conf.port,
            database=conf.db,
            user=conf.user,
            password=conf.password
        )

    @contextmanager
    def managed_client(self) -> Client:
        try:
            yield self.client
        finally:
            pass

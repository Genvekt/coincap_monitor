from pymongo.database import Database
from pymongo import MongoClient
from contextlib import contextmanager
from src.config import StageDBConf


class StageDBConnection:
    def __init__(self, conf: StageDBConf):
        client = MongoClient(
            f'mongodb://{conf.user}:{conf.password}@{conf.host}:{conf.port}/')
        self.db = client[conf.db]

    @contextmanager
    def managed_client(self) -> Database:
        try:
            yield self.db
        finally:
            self.db.client.close()

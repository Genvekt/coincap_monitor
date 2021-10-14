from clickhouse_driver import Client
import os
import time
import requests

CLICKHOUSE_PORT = os.environ.get('CLICKHOUSE_PORT')
CLICKHOUSE_DB = os.environ.get('CLICKHOUSE_DB')
CLICKHOUSE_USER = os.environ.get('CLICKHOUSE_USER')
CLICKHOUSE_PASSWORD = os.environ.get('CLICKHOUSE_PASSWORD')
LOCAL_TZ = os.environ.get('LOCAL_TZ')

print(CLICKHOUSE_PORT, CLICKHOUSE_DB, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD)

resp = requests.get("http://warehouse:8123")

print(resp.status_code)
print(resp.text)

client = Client(host='warehouse',
                port=9000,
                user=CLICKHOUSE_USER,
                password=CLICKHOUSE_PASSWORD,
                database=CLICKHOUSE_DB)

client.execute(f"CREATE TABLE IF NOT EXISTS coincap \
                (id String, \
                 symbol String,\
                 name String,\
                 priceUsd Float32, \
                 timestamp DateTime('{LOCAL_TZ}')) \
                ENGINE = MergeTree \
                PARTITION BY toYYYYMMDD(timestamp) \
                ORDER BY (timestamp)")


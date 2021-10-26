
# CoinCap monitor 


ETL pipeline for monitoring cripto curency price and build analytical dashboard based on collected data inside Data Warehouse.


[![example workflow](https://img.shields.io/github/workflow/status/Genvekt/coincap_monitor/flake8_and_mypy?label=code%20quality&logo=github&style=for-the-badge)](https://github.com/Genvekt/coincap_monitor/actions/workflows/flake8_and_mypy.yml)
[![example workflow](https://img.shields.io/github/workflow/status/Genvekt/coincap_monitor/Tests?label=tests&logo=github&style=for-the-badge)](https://github.com/Genvekt/coincap_monitor/actions/workflows/tests.yml)

## Built with
![](https://img.shields.io/github/pipenv/locked/python-version/Genvekt/coincap_monitor)
![](https://img.shields.io/badge/Docker-20.10.7-blue)
![](https://img.shields.io/badge/docker_compose-1.29.2-blue)


## System diagram
The following system diagram represents the project structure. From the picture, it may be seen that the system is composed from 4 docker containers with following purposes:
- **pipeline** performs complete ETL cycle (cron job)
- **warehause** contains main storage of cleaned data (Clickhouse)
- **stagedb** plays the role of a backup storage for raw data (MongoDB)
- **dashboard** generates and shows reports out of cleaned data (Metabase)

Additionally, dashboard uses PostgreSQL database container as its internal storage.

![system design](https://github.com/Genvekt/coincap_monitor/blob/main/assets/coincap_monitor.png)

## Project Structure

```
├── docs
│
├── pipeline
│   ├── cron              # Scheduler configs
│   ├── docker            # Environment configs
│   ├── logs              # Logs for pipeline service
│   │
│   ├── src               # ETL source code
│   │   ├── config.py     # Enviroment parsers
│   │   ├── db.py         # Warehouse management
│   │   ├── etl.py        # ETL functions
│   │   ├── run.py        # Pipeline script
│   │   └── stagedb.py    # StageDB management
│   │
│   └── tests             # Unittests for ETL source code
│
├── warehouse
│   ├── db                # Warehouse database files (Clickhouse)
│   └── logs              # Logs for warehouse service
│
├── stagedb
│   └── db                # StageDB database files (MongoDB)
│
└── dashboard
    ├── db                # Dashboard database files (PostgreSQL)
    ├── docker            # Environment configs
    └── logs              # Logs for dashboard service


```

## Installation

To run the project, perform the following steps:
1. Clone repo to your machine
```
git clone https://github.com/Genvekt/coincap_monitor.git
cd coincap_monitor
```
2. Create `.env` file with the following envairoment parameters:
- `API_KEY`: key that you must retrieve from [here](https://coincap.io/api-key)
- `API_URL`: url to the CoinCap API
- `STAGEDB_HOST`, `STAGEDB_DB`, `STAGEDB_USER`, `STAGEDB_PASSWORD`, `STAGEDB_PORT`: MongoDB access data
- `CLICKHOUSE_HOST`, `CLICKHOUSE_DB`, `CLICKHOUSE_USER`, `CLICKHOUSE_PASSWORD`, `CLICKHOUSE_PORT`: ClickHouse access data
- `POSTGRES_HOST`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_PORT`: PostgreSQL access data

    Example `.env` file:

    ```
    API_KEY={YOUR_API_KEY}
    API_URL=http://api.coincap.io/v2


    STAGEDB_HOST=stagedb
    STAGEDB_DB=stagedbdb
    STAGEDB_USER=stagedbuser
    STAGEDB_PASSWORD={YOUR_MONGODB_PASSWORD}
    STAGEDB_PORT=27017

    CLICKHOUSE_HOST=warehouse
    CLICKHOUSE_DB=clickhousedb
    CLICKHOUSE_USER=clickhouseuser
    CLICKHOUSE_PASSWORD={YOUR_CLICKHOUSE_PASSWORD}
    CLICKHOUSE_PORT=9000


    POSTGRES_HOST=dashboard_db
    POSTGRES_DB=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD={YOUR_POSTGRESQL_PASSWORD}
    POSTGRES_PORT=5432

    ```
3. Run application
```
docker network create CoinCapNet
docker-compose run --build -d
```
4. Stop application:
```
docker-compose down -v
```


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

![system design](https://github.com/Genvekt/coincap_monitor/blob/main/assets/coincap_monitor.png)

## Project Structure

```
├── assets
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
│   │   └── run.py        # Pipeline script
│   │
│   └── tests             # Unittests for ETL source code
│
├── warehouse
│   ├── db                # Warehouse database files (Clickhouse)
│   └── logs              # Logs for warehouse service
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
- `LOCAL_TZ`: Suitable timezone name from [this](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568) list
- `COIN_ID`: Id of a coin to monitor used by CoinCap API

    Example `.env` file:

    ```
    API_KEY='{YOUR_API_KEY}'
    LOCAL_TZ='Europe/Moscow'
    COIN_ID='bitcoin'
    ```
3. Run application
```
docker-compose run --build -d
```
4. Stop application:
```
docker-compose down -v
```

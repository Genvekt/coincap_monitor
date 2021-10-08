# Development process
This notes show my thoughts during development process

## Project Goal
In this project I aim to learn how to build Data Pipeline to collect and 
monitor information from third-side API. Moreover, I would like to deploy my 
application on AWS machine and make it publicly available.

## Requirements for the MVP
I see as an MVP the dashboard page hosted on AWS that shows how price of
the bitcoin changed during last 24 hour. Additionally, it must represent the
highest and lowest value recorded in this time period and during application
lifetime.

The purpose of monitoring is informational, therefore I will update dashbord
with 5 min interval. 

## System structure
System stracture will be as follows: 

- Python3 file as ETL sctipt
- Cron for sheduling the ETL script for every 5 min
- PostgreSQL as Data Warehouse
- Metabase for dashboarding
- Docker + Docker Compose for deploy
- AWS EC2 as publicly available host


## ETL
As a data source I decided to use [CoinCap API](https://docs.coincap.io/). It 
allows 200 requests/min, which is more than enough for this project.





# Development process
This notes show my thoughts during development process.
Development timeline goes with this notes - from top to bottom.

## Project Goal
In this project I aim to learn how to build Data Pipeline to collect and 
monitor information from third-side API. Moreover, I would like to deploy my 
application on AWS machine and make it publicly available.

I see my solution as OLAP system. It will not collect inforamtion in Real Time,
but will require quickly produce reports for users. 

## Requirements for the MVP
I see as an MVP the dashboard page hosted on AWS that shows how price of
the bitcoin changed during last 24 hour. Additionally, it must represent the
highest and lowest value recorded in this time period and during application
lifetime.

The purpose of monitoring is informational, therefore I will update dashbord
with 5 min interval. 

## Agile Work Breakdown
In this project I also practise the agile workflow. To do it, I define the tasks
with Theme - Epic - User Story - Task scheme.
For the MVP, next definition covers all aspects needed:

|Theme| Epic | User Stopy | Task |
|-----|------|------------|------|
|     |      |1. As a user I want to see bitcoin price in USD so that I can easily understand how much it is without googling.|  |
|     |      |2. As a user I want dashbord to update at least every 5 min so that I can know fresh state of bitcoin price. | |
|     |      |3. As a user I want to see the history of bitcoin price for last 24 hours so that I can understand the pattern of its price change. | |
|     |      |4. As a user I want to see the lowest/highest price for the last 24 hours so  that I can understand the current variance of price change.| |
|     |      |5. As a user I want to see historical data as scater plot so that I can easily see patterns in data.| |
|     |      |6. As a user I want historical data be present on revisit so that I can compare new data with old one.| |

## System structure
System stracture will be as follows: 

- Python3 file as ETL sctipt
- Cron for sheduling the ETL script for every 5 min
- MongoDB as Staging DB
- Clickhouse as Data Warehouse
- Metabase for dashboarding
- Docker + Docker Compose for deploy
- AWS EC2 as publicly available host


## ETL
As a data source I decided to use [CoinCap API](https://docs.coincap.io/). It 
allows 200 requests/min, which is more than enough for this project.

ETL python script will:
- **(Extract)** Request API for bitcoin price in USD.
- **(Staging)** Store responce unchanged with timestamp in MongoDB. 
    - **Why store?** To be able to rerun transformation scripts on already
    collected data. Usefull in situations when the requirements for 
    transformation change + backup. 
    - **Why MongoDB?** Although API responces have one structure, API may change.
    MongoDB allowes to store files as they are + practise with NoSQL DB.

- **(Transform)** Retrieve only price, timestamp, curency names and id 
from responce.

- **(Load)** Save data to the Clickhouse.
    - **Why Clickhouse?** Clickhouse is OLAP DW. I want my application to
    have quick reporting functionality, therefore it is better to take OLAP DW
    rather than OLTP, such as PostgreSQL. + Learn how to work with Clickhouse.


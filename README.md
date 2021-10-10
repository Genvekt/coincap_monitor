# 

![](https://img.shields.io/badge/Linter-flake8-blue)
![](https://img.shields.io/github/pipenv/locked/python-version/Genvekt/coincap_monitor)

## System diagram
The following system diagram represents the project structure. From the picture, it may be seen that the system is composed from 4 docker containers with following purposes:
- **pipeline** perform complete ETL cycle 
- **warehause** contains main storage of cleaned data
- **stagedb** plays role of backup storage for raw data
- **dashboard** generate and shows reports out of cleaned data

![system design](https://github.com/Genvekt/coincap_monitor/blob/main/assets/coincap_monitor.png)
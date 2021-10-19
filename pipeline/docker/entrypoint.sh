#!/bin/bash
printenv | grep -v "no_proxy" >> /etc/environment
touch  $CRON_LOG_FILE
cron && tail -f $CRON_LOG_FILE
#!/bin/bash
printenv | grep -v "no_proxy" >> /etc/environment
cron && tail -f /var/log/cron.log
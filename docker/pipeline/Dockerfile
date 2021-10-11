FROM python:3.8

# Set up 
WORKDIR /app
ENV PYTHONPATH=/app/src

# Install cron
RUN apt-get update && apt-get install cron -y

# Install all requirements
ADD ./docker/pipeline/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy all source code
COPY ./ /app/

# Copy cron config 
COPY ./cron/pipeline_scheduler /etc/cron.d/pipeline_scheduler
RUN chmod 644 /etc/cron.d/pipeline_scheduler
RUN crontab /etc/cron.d/pipeline_scheduler

# Create main log file
RUN touch /var/log/cron.log


# Pass environment variables to cron
# And run scheduler with log monitor
ENTRYPOINT /app/docker/pipeline/entrypoint.sh
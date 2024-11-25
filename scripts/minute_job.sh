#!/bin/bash
cd /app

echo "Starting minute data collection at $(date)" >> /var/log/cron.log 2>&1

echo "Running BTC minute data retrieval..." >> /var/log/cron.log 2>&1
python scripts/btc_minute_data.py >> /var/log/cron.log 2>&1

echo "Minute data collection completed at $(date)" >> /var/log/cron.log 2>&1

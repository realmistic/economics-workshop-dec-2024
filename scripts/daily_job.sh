#!/bin/bash
cd /app

echo "Starting daily data collection at $(date)" >> /var/log/cron.log 2>&1

echo "Running FRED data retrieval..." >> /var/log/cron.log 2>&1
python scripts/fred_data_retrieval.py >> /var/log/cron.log 2>&1

echo "Daily data collection completed at $(date)" >> /var/log/cron.log 2>&1

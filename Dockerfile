FROM python:3.9-slim

WORKDIR /app

# Install cron and other required system packages
RUN apt-get update && apt-get install -y cron curl sqlite3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files (excluding data directory)
COPY app.py .
COPY scripts/ scripts/

# Make shell scripts executable
RUN chmod +x scripts/minute_job.sh scripts/daily_job.sh

# Set up environment for cron
RUN echo "SHELL=/bin/bash\n\
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\n\
* * * * * cd /app && ./scripts/minute_job.sh >> /var/log/cron.log 2>&1\n\
0 0 * * * cd /app && ./scripts/daily_job.sh >> /var/log/cron.log 2>&1" | crontab -

# Create log file and set permissions
RUN touch /var/log/cron.log && \
    chmod 0666 /var/log/cron.log

# Create data directory
RUN mkdir -p /app/data

# Create startup script with data check
RUN echo '#!/bin/bash\n\
service cron start\n\
echo "$(date): Starting cron service..." >> /var/log/cron.log\n\
\n\
# Check if database exists and has data\n\
if [ ! -f /app/data/economics_data.db ] || [ ! -s /app/data/economics_data.db ]; then\n\
    echo "$(date): No existing data found. Running initial data collection..." >> /var/log/cron.log\n\
    ./scripts/daily_job.sh\n\
    ./scripts/minute_job.sh\n\
else\n\
    echo "$(date): Existing data found. Skipping initial collection." >> /var/log/cron.log\n\
fi\n\
\n\
echo "$(date): Starting Streamlit..." >> /var/log/cron.log\n\
exec streamlit run app.py --server.port=8501 --server.address=0.0.0.0\n\
' > /app/start.sh && \
    chmod +x /app/start.sh

# Expose Streamlit port
EXPOSE 8501

# Health check using curl
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health

# Run both cron and Streamlit
CMD ["/app/start.sh"]

# Economic Data Dashboard - Reproduction Guide

This document provides step-by-step instructions for reproducing this project using AI-assisted development.

## Introduction

Hi, I'm **Ivan Brigida**, an Analyst at Google with a background in **Economics** and **Data Analysis**. 
Before joining Google, I worked in the banking sector, and 3 years ago, I started investing in **U.S. markets** while living in **Ireland**. 
My work and investing experience focus on using **economic data** to understand the economy, 
make financial decisions, and develop market strategies.

Last year, I ran the **Stock Markets Analysis Zoomcamp**, 
which attracted **1,800+ registrations**. 
I’ll be running it again in **2025** to introduce participants to economic data with 
reduced technical complexity.

---

### My Skills and Motivation

I’m skilled in:
- Writing **SQL code** for analysis and workflows.
- Building **graphs** and conducting data-driven analysis.
- Creating **basic trading strategies**, though they can get complex.

However, I want to avoid the overhead of tasks like:
- Managing **data pipelines** and **databases**.
- Ensuring **data integrity**.
- Coding **dashboards**, debugging **JavaScript**, or dealing with **CSS styles**.
- Handling **containerization** and deployment.

AI tools have helped me bridge these gaps, saving time and energy (at <$30/month). 
I’m focusing on what I do best while letting technology handle the rest.

---

### The Grand Idea 💡

This repository is a step toward a **generic Data Science project template** with solid foundational layers:
1. **Data storage** and **automated updates** for reliable, scalable data handling.
2. **Dashboards** for visualization and monitoring.
3. **Containers** for streamlined deployment.

With these pieces in place, the real focus can shift to **predictions**, **machine learning**, 
and advanced strategy development—what really matters for understanding markets and making decisions.


## Steps to Reproduce via AI-Assisted Development

### 1. Initial Data Collection Setup
Start with the manual Jupyter notebook that reads data from Yahoo Finance and FRED
```
"I need to convert the manual_start.ipynb notebook into a Python script. The notebook contains code to fetch S&P 500 data from Yahoo Finance and economic data from FRED."
```

### 2. Create FRED Data Retrieval Script
Move to a dedicated Python script and expand the metrics:
```
"Create a script fred_data_retrieval.py that fetches the following metrics from FRED in this order: UNRATE, CPILFESL, CPIAUCSL, CP0000IEM086NEST, CP0000EZ19M086NEST, GDPC1, GDPPOT, FEDFUNDS, GFDEGDQ188S, DGS1, DGS5, DGS10, DTWEXBGS, DEXUSEU, VIXCLS. Include proper error handling and data transformations."
```

### 3. Create Data Visualization Module
Separate data loading from visualization:
```
"Create a data_visualization.py module that handles the visualization of our economic data. It should create interactive plots using Plotly for all our metrics, with proper styling and layout."
```

### 4. Develop Streamlit Application
Create the web application:
```
"Create a Streamlit app that displays our economic data visualizations. The app should:
1. Read data from SQLite database
2. Have multiple tabs for different data categories
3. Include interactive charts
4. Be styled professionally
5. Be containerization-ready"
```

### 5. Add Cryptocurrency Data Collection
Implement BTC-USD minute data collection:
```
"Create a script btc_minute_data.py that fetches BTC-USD minute data from Yahoo Finance. It should:
1. Support both one-time and continuous collection modes
2. Store data directly in SQLite database
3. Handle incremental updates
4. Include proper error handling and logging"
```

### 6. Setup Local Development Environment
Create local development scripts:
```
"Create shell scripts for running data collection jobs locally:
1. minute_job.sh for cryptocurrency minute data
2. daily_job.sh for economic indicators
Both should handle logging and error reporting."
```

### 7. Containerization
Package the application:
```
"Create a Dockerfile that:
1. Sets up Python environment
2. Installs all dependencies
3. Configures cron jobs for data collection
4. Runs the Streamlit app
5. Includes health checks
6. Handles logging"
```

### 8. Container Deployment and Testing
Build and run the container:
```
"Help me test the containerized application:
1. Build the container
2. Configure port mapping
3. Set up volume mounting
4. Verify data collection jobs
5. Test the web interface"
```

## Running the Application

### Local Development
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run data collection scripts:
```bash
./scripts/daily_job.sh  # Collect daily economic data
./scripts/minute_job.sh  # Start minute data collection
```

3. Launch Streamlit app:
```bash
streamlit run app.py
```

### Docker Deployment
1. Build the container:
```bash
docker build -t data_app .
```

2. Run the container:
```bash
docker run -d \
  --name finance_test \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  data_app
```

3. Monitor logs:
```bash
docker logs finance_test
```

4. Check data collection:
```bash
docker exec finance_test sqlite3 /app/data/economics_data.db \
  "SELECT COUNT(*) FROM btc_minute;"
```

## Project Structure
```
.
├── app.py                      # Streamlit application
├── data/                       # Data directory
│   └── economics_data.db       # SQLite database
├── Dockerfile                  # Container configuration
├── requirements.txt            # Python dependencies
├── scripts/
│   ├── btc_minute_data.py     # Cryptocurrency data collection
│   ├── daily_job.sh           # Daily collection script
│   ├── fred_data_retrieval.py # Economic data collection
│   └── minute_job.sh          # Minute collection script
└── README.md                  # Project documentation
```

## Key Features
- Real-time cryptocurrency data collection
- Daily economic indicators updates
- Interactive visualizations
- Professional dark theme UI
- Containerized deployment
- Automated data collection via cron jobs
- SQLite database for data storage
- Health monitoring and logging

## Notes
- The application uses SQLite for simplicity, but can be adapted for other databases
- Data collection jobs run on different schedules (minute vs. daily)
- The container includes health checks and proper logging
- Volume mounting ensures data persistence across container restarts

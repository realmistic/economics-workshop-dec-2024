# Economic Data Dashboard - Reproduction Guide

This document provides step-by-step instructions for reproducing this project using AI-assisted development. For project overview, features, and deployment instructions, see [README.md](README.md).

## Steps to Reproduce via AI-Assisted Development

### 1. Initial Data Collection Setup
Start with the manual Jupyter notebook that reads data from Yahoo Finance and FRED
```
"I need to convert the manual_start.ipynb notebook into a Python script. The notebook contains code to fetch S&P 500 data from Yahoo Finance and economic data from FRED."
```
Output:
```
notebooks/
└── manual_start.ipynb
```

### 2. Create FRED Data Retrieval Script
Move to a dedicated Python script and expand the metrics:
```
"Create a script fred_data_retrieval.py that fetches the following metrics from FRED in this order: UNRATE, CPILFESL, CPIAUCSL, CP0000IEM086NEST, CP0000EZ19M086NEST, GDPC1, GDPPOT, FEDFUNDS, GFDEGDQ188S, DGS1, DGS5, DGS10, DTWEXBGS, DEXUSEU, VIXCLS. Include proper error handling and data transformations."
```
Output:
```
scripts/
└── fred_data_retrieval.py
```

### 3. Create Data Visualization Module
Separate data loading from visualization:
```
"Create a data_visualization.py module that handles the visualization of our economic data. It should create interactive plots using Plotly for all our metrics, with proper styling and layout."
```
Output:
```
interactive_notebooks/
└── data_visualization.py
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
Output:
```
app.py
utils.py
data/
└── economics_data.db
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
Output:
```
scripts/
├── fred_data_retrieval.py
└── btc_minute_data.py
```

### 6. Setup Local Development Environment
Create local development scripts:
```
"Create shell scripts for running data collection jobs locally:
1. minute_job.sh for cryptocurrency minute data
2. daily_job.sh for economic indicators
Both should handle logging and error reporting."
```
Output:
```
scripts/
├── fred_data_retrieval.py
├── btc_minute_data.py
├── daily_job.sh
└── minute_job.sh
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
Output:
```
Dockerfile
requirements.txt
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
Output:
```
.gitignore
```

### 9. Application Structure and Styling Improvements
Organize the application structure and enhance styling:
```
"Let's improve the application organization and styling:
1. Create a 'pages' directory to separate different dashboard sections
2. Move CSS to a dedicated file in 'static/css/style.css'
3. Implement pagination for data tables
4. Create separate modules for economic indicators, stock market, interest rates, currency markets, and crypto markets"
```
Output:
```
pages/
├── __init__.py
├── economic_indicators.py
├── stock_market.py
├── interest_rates.py
├── currency_markets.py
└── crypto_markets.py
static/
└── css/
    └── style.css
```

## Final Project Structure
```
.
├── app.py                      # Streamlit application
├── utils.py                    # Shared utilities (DB, data loading, chart styling)
├── data/                       # Data directory
│   └── economics_data.db       # SQLite database
├── Dockerfile                  # Container configuration
├── requirements.txt            # Python dependencies
├── scripts/
│   ├── btc_minute_data.py     # Cryptocurrency data collection
│   ├── daily_job.sh           # Daily collection script
│   ├── fred_data_retrieval.py # Economic data collection
│   └── minute_job.sh          # Minute collection script
├── pages/                      # Dashboard pages
│   ├── economic_indicators.py  # Economic indicators page
│   ├── stock_market.py        # Stock market analysis
│   ├── interest_rates.py      # Interest rates page
│   ├── currency_markets.py    # Currency markets page
│   └── crypto_markets.py      # Cryptocurrency markets page
├── static/
│   └── css/
│       └── style.css          # Application styling
└── README.md                  # Project documentation

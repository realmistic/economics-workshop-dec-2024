# Economic Data Dashboard
**🚀 Try the live dashboard: [Economics Dashboard on Streamlit Cloud](https://economics-workshop-dec-2024.streamlit.app/)** - [Watch Workshop Recording](https://www.youtube.com/watch?v=MeDUe75WQaQ&list=PLSWnIAnueyu8KBcwhE48ASp20nZMg2qtt)

<p align="center">
  <img src="static/images/dashboard_preview.png" alt="Economic Data Dashboard Preview" width="900"/>
  <br>
  <em>Economic Indicators Dashboard showing unemployment rate trends and analysis</em>
</p>

A comprehensive economic data dashboard that combines data from multiple sources (Yahoo Finance, FRED) into a Streamlit application with automated data collection and visualization.

## Introduction

Hi, I'm **Ivan Brigida**, an Analyst at Google with a background in **Economics** and **Data Analysis**. Before joining Google, I worked in the banking sector, and 3 years ago, I started investing in **U.S. markets** while living in **Ireland**. My work and investing experience focus on using **economic data** to understand the economy, make financial decisions, and develop market strategies. You can read more about my approach in my [blog post about macro indicators affecting the stock market](https://pythoninvest.com/long-read/macro-indicators-affecting-stock-market).

Last year, I ran the **[Stock Markets Analysis Zoomcamp](https://pythoninvest.com/course)**, which attracted **1,800+ registrations**. I'll be running it again in **2025**, you can express your interest here:

<p align="center">
  <a href="https://pythoninvest.com/course"><img src="https://user-images.githubusercontent.com/875246/185755203-17945fd1-6b64-46f2-8377-1011dcb1a444.png" height="50" /></a>
</p>

## 🙌 Support PythonInvest

Help us grow and improve PythonInvest:  

1. **Engage**: 🌟 Star this repo, 👍 like the video, and 💬 comment on YouTube.  
2. **Contribute**: 🍴 Fork the repo, try it, tweak the indicators, and share feedback with a link.  
3. **Donate**: ☕ [Buy Me a Coffee](https://buymeacoffee.com/pythoninvest) or ❤️ [GitHub Sponsorship](https://github.com/sponsors/realmistic).  

---

### My Skills and Motivation

I'm skilled in:
- Writing **SQL code** for analysis and workflows.
- Building **graphs** and conducting data-driven analysis.
- Deliverying business insights.

However, I want to avoid the overhead of tasks like:
- Managing **data pipelines** and **databases**.
- Ensuring **data integrity**.
- Coding **dashboards**, debugging **JavaScript**, or dealing with **CSS styles**.
- Handling **containerization** and deployment.

AI tools have helped me bridge these gaps, saving time and energy (at <$30/month). I'm focusing on what I do best while letting technology handle the rest.

---

### The Grand Idea 💡

This repository is a step toward a **generic Data Science project template** with solid foundational layers:
1. **Data storage** and **automated updates** for reliable, scalable data handling.
2. **Dashboards** for visualization and monitoring.
3. **Containers** for streamlined deployment.

With these pieces in place, the real focus can shift to **predictions**, **machine learning**, and advanced strategy development—what really matters for understanding markets and making decisions.

## Features
- (Near) real-time cryptocurrency data collection
- Daily economic indicators updates
- Interactive visualizations
- Containerized deployment
- Automated data collection via cron jobs
- SQLite database for data storage
- Health monitoring and logging

## Project Structure
```
.
├── app.py                      # Streamlit application
├── utils.py                    # Shared utilities (DB, data loading, chart styling)
├── data/                       # Data directory
│   ├── economics_data.db       # SQLite database
│   ├── snp_500_minute_yfinance.parquet # S&P 500 minute data
│   └── test_db.db             # Test database
├── Dockerfile                  # Container configuration
├── requirements.txt            # Python dependencies
├── interactive_notebooks/      # Interactive Python notebooks
│   └── data_visualization.py   # Visualization utilities
├── notebooks/                  # Jupyter notebooks
│   └── manual_start.ipynb      # Manual startup notebook
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
│   ├── css/
│   │   └── style.css          # Application styling
│   └── images/                # Static images
│       ├── dashboard_preview.png # Dashboard preview
│       └── logo.png           # Application logo
└── README.md                  # Project documentation
```

## Project Reproduction
For detailed instructions on how to reproduce this project from scratch using AI-assisted development, see [REPRODUCTION.md](REPRODUCTION.md).

## Quick Start

### Local Development
Note: The scripts are designed to run within the Docker container. For local development:

1. Create and activate a virtual environment, install dependencies:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

2. (Optional) Run data collection scripts before starting the app:
```bash
# Collect BTC minute data
python scripts/btc_minute_data.py --mode once

# Collect FRED economic indicators
python scripts/fred_data_retrieval.py
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

### Docker Deployment (Local)

Use this option for local testing with persistent data:
```bash
# Run this before, if you want to rebuild the container that is currently running:
docker stop finance_test && docker rm finance_test

# Then run the container:
docker build -t data_app .
docker run -d --name finance_test -p 8501:8501 -v $(pwd)/data:/app/data data_app
```

Note: For local development, we use port 8501 (Streamlit's default port). For production deployment on Digital Ocean, we use port 80 (standard HTTP port).

### Verifying Data Collection
After running the container, you can verify data collection:

1. Check data collection logs:
```bash
docker exec finance_test tail -f /var/log/cron.log
```

2. Verify collected data:
```bash
# Check BTC minute data
docker exec finance_test sqlite3 /app/data/economics_data.db "SELECT datetime, close, volume FROM btc_minute ORDER BY datetime DESC LIMIT 5;"

# Check daily economic data (e.g., SP500)
docker exec finance_test sqlite3 /app/data/economics_data.db "SELECT date, sp500, sp500_returns_daily FROM sp500 ORDER BY date DESC LIMIT 5;"
```

### Managing Data Collection

1. To manually trigger data collection jobs:
```bash
# Run daily job
docker exec finance_test /app/scripts/daily_job.sh

# Run minute job
docker exec finance_test /app/scripts/minute_job.sh
```

2. Monitor logs:
```bash
# View cron job logs
docker exec finance_test tail -f /var/log/cron.log

# View container logs
docker logs finance_test

# Check data collection status
docker exec finance_test sqlite3 /app/data/economics_data.db "SELECT COUNT(*) FROM btc_minute;"
```

### Accessing the Dashboard
Access the dashboard at http://localhost:8501

## Cloud Deployment Options

### 1. Streamlit Community Cloud (Current Demo, easiest)
This option is perfect for demos and simple deployments. The data will be static but it's free and easy to set up.

> [!NOTE]
> The [live demo](https://economics-workshop-dec-2024.streamlit.app/) runs on Streamlit Community Cloud.


### Steps:
1. Fork this repository to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your forked repository
6. Set main branch and app path to `app.py`
7. Click "Deploy"

Your app will be available at `https://[your-app-name].streamlit.app`

Note: The Community Cloud version will have static data. For dynamic updates, consider:
- Setting up GitHub Actions for periodic data collection
- Using external databases instead of local SQLite
- Implementing API-based data fetching

### 2. Cloud Platform Deployment (Full Control)

### Digital Ocean (Recommended for Beginners)

Digital Ocean offers a good balance of simplicity and control.

1. Create account at [digitalocean.com](https://m.do.co/c/bb21d245e296). (This is a referral link by Ivan: you will have $200 in credit over 60 days)

2. Install Docker on your machine
> [!TIP]
> You can skip this step by creating a Droplet with Docker pre-installed using Digital Ocean's "Docker" image when creating your droplet. 
> This is the recommended approach as it saves time and ensures proper Docker setup.
> See [How to Use the Docker 1-Click Install on DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-use-the-docker-1-click-install-on-digitalocean) for detailed instructions.

3. Generate GitHub Personal Access Token (Required for repository access)
   - Go to https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Name: "digital-ocean-deployment"
   - Select scope: check "repo"
   - Click "Generate token"
   - COPY THE TOKEN IMMEDIATELY (you won't see it again)

4. Deploy the application:
```bash
# Clone repository using your token (replace YOUR_TOKEN)
git clone https://YOUR_TOKEN@github.com/realmistic/economics-workshop-dec-2024.git
cd economics-workshop-dec-2024

# Build and run locally on droplet
docker build -t data_app .
docker run -d --name finance_test -p 80:8501 -v $(pwd)/data:/app/data data_app
```

> [!NOTE]
> If you don't want to use your token directly in the git clone command, you can also:
> ```bash
> git config --global credential.helper store
> git clone https://github.com/realmistic/economics-workshop-dec-2024.git
> # When prompted for password, use your token
> ```

5. Get your droplet's IP address:
```bash
hostname -I | awk '{print $1}'
```

6. Access your dashboard by entering your droplet's IP address in a web browser:
   `http://YOUR_DROPLET_IP`

Note: The dashboard works without specifying a port because we mapped the container's port 8501 to the host's port 80 (standard HTTP port) in the docker run command (`-p 80:8501`).

Cost: Starting at ~$5/month

### 3. AWS/GCP/Azure (Enterprise)
For full control and scalability, use major cloud providers.

Example using AWS:
1. Create AWS account
2. Install AWS CLI
3. Push to ECR:
```bash
aws ecr get-login-password --region region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com
docker tag data_app aws_account_id.dkr.ecr.region.amazonaws.com/data_app
docker push aws_account_id.dkr.ecr.region.amazonaws.com/data_app
```
4. Deploy using ECS or EKS
5. Set up EFS for data persistence

Cost: Starting at ~$20/month

## Cloud Deployment Comparison

### Streamlit Community Cloud
✅ Free
✅ Easy setup
✅ Good for demos
❌ Static data only
❌ Limited control

### Digital Ocean
✅ Simple pricing
✅ Good documentation
✅ Moderate control
✅ Data persistence
❌ Basic monitoring

### AWS/GCP/Azure
✅ Full control
✅ Enterprise features
✅ Advanced monitoring
✅ Auto-scaling
❌ Complex setup
❌ Higher cost

Choose based on your needs:
- Demo/Portfolio: Use Streamlit Cloud
- Small Project: Use Digital Ocean
- Enterprise/Production: Use AWS/GCP/Azure

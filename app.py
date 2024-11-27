import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sqlite3
from datetime import datetime, timedelta
import plotly.express as px
from pathlib import Path
import os

# Set page config
st.set_page_config(
    page_title="Economic Data Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for navigation if it doesn't exist
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'Market Overview'

# Database connection function
def get_database_connection():
    db_path = 'data/economics_data.db'
    if not os.path.exists(db_path):
        st.error(f"Database file not found at {db_path}")
        raise FileNotFoundError(f"Database file not found at {db_path}")
    return sqlite3.connect(db_path)

@st.cache_data(ttl=24*3600)  # Cache for 24 hours
def load_data(query):
    try:
        conn = get_database_connection()
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if 'date' not in df.columns:
            st.error(f"date column not found in query result. Available columns: {df.columns.tolist()}")
            raise KeyError("date column not found in query result")
            
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        raise e

def load_btc_data():
    try:
        conn = get_database_connection()
        query = """
        SELECT Datetime, Open, High, Low, Close, Volume
        FROM btc_minute
        ORDER BY Datetime DESC
        LIMIT 300
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        return df
    except Exception as e:
        st.error(f"Error loading BTC data: {str(e)}")
        raise e

def get_file_update_time(filepath):
    try:
        timestamp = os.path.getmtime(filepath)
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return "File not found"

def get_recent_logs():
    try:
        with open('/var/log/cron.log', 'r') as f:
            logs = f.readlines()
            return logs[-10:] if logs else ["No logs available"]
    except:
        return ["Log file not accessible"]

# Custom CSS for modern dark theme
st.markdown("""
    <style>
    /* Main page background */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1a1c24;
    }
    
    /* Sidebar title */
    .sidebar-title {
        color: #00FFF0;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 2rem;
    }
    
    /* Navigation buttons */
    section[data-testid="stSidebar"] div.stButton > button {
        background-color: #00FFF0 !important;
        color: #0e1117 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        padding: 4px 12px !important;
        border-radius: 20px !important;
        border: none !important;
        margin: 4px 0 !important;
        height: 32px !important;
        width: 100% !important;
        display: block !important;
        text-align: center !important;
    }
    
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #00FFF0 !important;
        color: #0e1117 !important;
        border: none !important;
    }

    section[data-testid="stSidebar"] div.stButton > button:active {
        background-color: #00FFF0 !important;
        color: #0e1117 !important;
        border: none !important;
    }

    section[data-testid="stSidebar"] div.stButton > button:focus {
        background-color: #00FFF0 !important;
        color: #0e1117 !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00FFF0 !important;
    }
    
    /* Text elements */
    .stText {
        color: #c6cad2 !important;
    }

    /* Plotly hover style override */
    .js-plotly-plot .plotly .modebar {
        background: rgba(26,28,36,0.8) !important;
    }
    
    .js-plotly-plot .plotly .modebar-btn path {
        fill: #00FFF0 !important;
    }

    .js-plotly-plot .plotly .modebar-btn:hover path {
        fill: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# Function to create consistent chart layout
def get_chart_layout(title):
    return dict(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=dict(
            text=title,
            font=dict(color='#00FFF0', size=20)
        ),
        showlegend=True,
        legend=dict(
            font=dict(color='#ffffff'),
            bgcolor='rgba(26,28,36,0.8)'
        ),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#1a1c24',
            font_size=14,
            font_family="monospace"
        ),
        xaxis=dict(
            gridcolor='#2d3139',
            showgrid=True,
            gridwidth=1
        ),
        yaxis=dict(
            gridcolor='#2d3139',
            showgrid=True,
            gridwidth=1
        )
    )

# Sidebar navigation
with st.sidebar:
    st.markdown('<p class="sidebar-title">Navigation</p>', unsafe_allow_html=True)
    for view in ['Market Overview', 'Economic Indicators', 'Interest Rates', 
                'Currency Markets', 'Crypto Markets', 'Data Status']:
        if st.button(view, key=view, help=f"View {view}", use_container_width=True):
            st.session_state.current_view = view

# Main content
st.title('Economic Data Dashboard')

# Display content based on selected view
if st.session_state.current_view == 'Data Status':
    st.header('Data Update Status')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Last Update Times')
        st.text(f"S&P 500 Minute Data: {get_file_update_time('data/sp500_minute.parquet')}")
        st.text(f"BTC Minute Data: {get_file_update_time('data/btc_minute.db')}")
        st.text(f"Economic Data: {get_file_update_time('data/economics_data.db')}")
    
    with col2:
        st.subheader('Recent Data Collection Logs')
        logs = get_recent_logs()
        for log in logs:
            st.text(log.strip())

elif st.session_state.current_view == 'Market Overview':
    st.header('S&P 500 Overview')
    
    try:
        # Load S&P 500 data
        sp500_query = """
        SELECT *
        FROM sp500
        ORDER BY date
        """
        sp500 = load_data(sp500_query)
        
        fig_sp500 = go.Figure()
        fig_sp500.add_trace(go.Scatter(x=sp500.index, y=sp500['SP500'], 
                                     name='S&P 500', 
                                     line=dict(color='#FFBA08', width=2)))
        fig_sp500.add_trace(go.Scatter(x=sp500.index, y=sp500['sp500_ma20'], 
                                     name='20-day MA',
                                     line=dict(color='#00FFF0', width=1, dash='dash')))
        fig_sp500.add_trace(go.Scatter(x=sp500.index, y=sp500['sp500_ma50'], 
                                     name='50-day MA',
                                     line=dict(color='#FF00FF', width=1, dash='dash')))
        fig_sp500.add_trace(go.Scatter(x=sp500.index, y=sp500['sp500_ma200'], 
                                     name='200-day MA',
                                     line=dict(color='#00FF00', width=1, dash='dash')))
        fig_sp500.update_layout(get_chart_layout('S&P 500 Index with Moving Averages'))
        st.plotly_chart(fig_sp500, use_container_width=True)

        # VIX
        vix_query = """
        SELECT *
        FROM vixcls
        ORDER BY date
        """
        vix = load_data(vix_query)
        
        fig_vix = go.Figure()
        fig_vix.add_trace(go.Scatter(x=vix.index, y=vix['VIXCLS'], 
                                   name='VIX',
                                   line=dict(color='#FFBA08', width=2)))
        vix['vix_ma20'] = vix['VIXCLS'].rolling(window=20).mean()
        vix['vix_ma50'] = vix['VIXCLS'].rolling(window=50).mean()
        fig_vix.add_trace(go.Scatter(x=vix.index, y=vix['vix_ma20'], 
                                   name='20-day MA',
                                   line=dict(color='#00FFF0', width=1, dash='dash')))
        fig_vix.add_trace(go.Scatter(x=vix.index, y=vix['vix_ma50'], 
                                   name='50-day MA',
                                   line=dict(color='#FF00FF', width=1, dash='dash')))
        fig_vix.update_layout(get_chart_layout('VIX Volatility Index'))
        st.plotly_chart(fig_vix, use_container_width=True)
    except Exception as e:
        st.error(f"Error in Market Overview: {str(e)}")

elif st.session_state.current_view == 'Economic Indicators':
    st.header('Economic Indicators')
    
    try:
        # Unemployment Rate
        unemployment_query = """
        SELECT *
        FROM unrate
        ORDER BY date
        """
        unemployment = load_data(unemployment_query)
        
        fig_unemployment = go.Figure()
        fig_unemployment.add_trace(go.Scatter(x=unemployment.index, y=unemployment['UNRATE'], 
                                           name='Unemployment Rate',
                                           line=dict(color='#FFBA08', width=2)))
        fig_unemployment.update_layout(get_chart_layout('U.S. Unemployment Rate'))
        st.plotly_chart(fig_unemployment, use_container_width=True)
        
        # Add unemployment rate bullet points
        st.markdown("""
        * **Importance**: The U.S. unemployment rate is a vital economic indicator, reflecting labor market health and overall economic performance. It helps shape policies for sustainable growth.
        * **Recent Trend**: Following a sharp spike around 2020 (due to the COVID-19 pandemic), unemployment has declined significantly, stabilizing near historical lows, showcasing labor market resilience.
        * **Role of the Central Bank**: The Federal Reserve aims to maintain maximum employment as part of its dual mandate. By adjusting interest rates and using monetary policy tools, it strives to balance low unemployment with price stability, ensuring sustainable economic growth.
        """)
        
        # US CPI Data
        cpi_core_query = """
        SELECT *
        FROM cpilfesl
        ORDER BY date
        """
        cpi_all_query = """
        SELECT *
        FROM cpiaucsl
        ORDER BY date
        """
        cpi_core = load_data(cpi_core_query)
        cpi_all = load_data(cpi_all_query)
        
        fig_cpi = go.Figure()
        fig_cpi.add_trace(go.Scatter(x=cpi_core.index, y=cpi_core['cpi_core_yoy'], 
                                   name='Core CPI',
                                   line=dict(color='#FFBA08', width=2)))
        fig_cpi.add_trace(go.Scatter(x=cpi_all.index, y=cpi_all['cpi_all_yoy'], 
                                   name='All Items CPI',
                                   line=dict(color='#00FFF0', width=2)))
        fig_cpi.update_layout(get_chart_layout('US Inflation/Consumer Price Index (Year-over-Year Change)'))
        st.plotly_chart(fig_cpi, use_container_width=True)

        # Add US CPI commentary
        st.markdown("""
        * **Rising Costs of Living**: High inflation, especially post-2020, reduces household purchasing power, prompting families to reallocate budgets toward essentials like food, energy, and housing.
        * **Planning Ahead for Potential Rate Hikes**: Persistent inflation increases the likelihood of future Federal Reserve rate hikes, which could raise borrowing costs for mortgages, credit cards, and loans, influencing current savings and spending decisions.
        * **Delayed Major Purchases**: Households may postpone big-ticket purchases (like homes or cars) in anticipation of potential increases in financing costs or tighter credit availability.
        """)

        # Ireland and Euro Area CPI Data
        ireland_cpi_query = """
        SELECT *
        FROM ireland_cpi
        ORDER BY date
        """
        euro_cpi_query = """
        SELECT *
        FROM euro_cpi
        ORDER BY date
        """
        ireland_cpi = load_data(ireland_cpi_query)
        euro_cpi = load_data(euro_cpi_query)
        
        fig_euro_cpi = go.Figure()
        fig_euro_cpi.add_trace(go.Scatter(x=ireland_cpi.index, y=ireland_cpi['cpi_ireland_yoy'], 
                                       name='Ireland CPI',
                                       line=dict(color='#00FF00', width=2)))
        fig_euro_cpi.add_trace(go.Scatter(x=euro_cpi.index, y=euro_cpi['cpi_euro_yoy'], 
                                       name='Euro Area CPI',
                                       line=dict(color='#003399', width=2)))
        fig_euro_cpi.add_trace(go.Scatter(x=cpi_all.index, y=cpi_all['cpi_all_yoy'], 
                                       name='US CPI (All Items)',
                                       line=dict(color='#00FFF0', width=2)))
        fig_euro_cpi.update_layout(get_chart_layout('Ireland vs Euro Area vs. US CPI (Year-over-Year Change)'))
        st.plotly_chart(fig_euro_cpi, use_container_width=True)

        # Add Euro CPI commentary
        st.markdown("""
        * **Household Responses to Inflation Pressure**: High inflation since 2020 has led citizens to prioritize essential spending while delaying or reducing discretionary expenses, such as travel or luxury goods.
        * **Potential Impact of ECB Policy Shifts**: Elevated inflation in the Euro Area raises concerns about future European Central Bank rate hikes, which would increase mortgage and credit costs for households, encouraging higher savings today.
        * **Cross-Regional Impact**: Irish households, being more exposed to energy and housing price volatility, may face unique challenges compared to more stable Euro Area averages, making financial planning more uncertain.
        """)

    except Exception as e:
        st.error(f"Error in Economic Indicators: {str(e)}")

elif st.session_state.current_view == 'Interest Rates':
    st.header('Interest Rates')
    
    try:
        # Treasury Yields
        yields_1y_query = """
        SELECT *
        FROM dgs1
        ORDER BY date
        """
        yields_5y_query = """
        SELECT *
        FROM dgs5
        ORDER BY date
        """
        yields_10y_query = """
        SELECT *
        FROM dgs10
        ORDER BY date
        """
        yields_1y = load_data(yields_1y_query)
        yields_5y = load_data(yields_5y_query)
        yields_10y = load_data(yields_10y_query)
        
        fig_treasury = go.Figure()
        fig_treasury.add_trace(go.Scatter(x=yields_1y.index, y=yields_1y['DGS1'], 
                                       name='1-Year',
                                       line=dict(color='#FFBA08', width=2)))
        fig_treasury.add_trace(go.Scatter(x=yields_5y.index, y=yields_5y['DGS5'], 
                                       name='5-Year',
                                       line=dict(color='#00FFF0', width=2)))
        fig_treasury.add_trace(go.Scatter(x=yields_10y.index, y=yields_10y['DGS10'], 
                                       name='10-Year',
                                       line=dict(color='#FF00FF', width=2)))
        fig_treasury.update_layout(get_chart_layout('Treasury Yields'))
        st.plotly_chart(fig_treasury, use_container_width=True)
        
        # Fed Funds Rate
        fedfunds_query = """
        SELECT *
        FROM fedfunds
        ORDER BY date
        """
        fedfunds = load_data(fedfunds_query)
        
        fig_fedfunds = go.Figure()
        fig_fedfunds.add_trace(go.Scatter(x=fedfunds.index, y=fedfunds['FEDFUNDS'], 
                                       name='Federal Funds Rate',
                                       line=dict(color='#FFBA08', width=2)))
        fig_fedfunds.update_layout(get_chart_layout('Federal Funds Rate'))
        st.plotly_chart(fig_fedfunds, use_container_width=True)
    except Exception as e:
        st.error(f"Error in Interest Rates: {str(e)}")

elif st.session_state.current_view == 'Currency Markets':
    st.header('Currency Markets')
    
    try:
        # Dollar Index
        dollar_query = """
        SELECT *
        FROM dtwexbgs
        ORDER BY date
        """
        dollar_index = load_data(dollar_query)
        
        fig_dollar = go.Figure()
        fig_dollar.add_trace(go.Scatter(x=dollar_index.index, y=dollar_index['DTWEXBGS'], 
                                     name='Dollar Index',
                                     line=dict(color='#FFBA08', width=2)))
        fig_dollar.update_layout(get_chart_layout('Trade Weighted U.S. Dollar Index'))
        st.plotly_chart(fig_dollar, use_container_width=True)
        
        # EUR/USD
        eurusd_query = """
        SELECT *
        FROM dexuseu
        ORDER BY date
        """
        eurusd = load_data(eurusd_query)
        
        fig_eurusd = go.Figure()
        fig_eurusd.add_trace(go.Scatter(x=eurusd.index, y=eurusd['DEXUSEU'], 
                                     name='EUR/USD',
                                     line=dict(color='#FFBA08', width=2)))
        fig_eurusd.update_layout(get_chart_layout('EUR/USD Exchange Rate'))
        st.plotly_chart(fig_eurusd, use_container_width=True)
    except Exception as e:
        st.error(f"Error in Currency Markets: {str(e)}")

elif st.session_state.current_view == 'Crypto Markets':
    st.header('Cryptocurrency Markets')
    
    try:
        # Load BTC data
        btc_data = load_btc_data()
        
        # Price chart
        fig_btc = go.Figure()
        fig_btc.add_trace(go.Scatter(x=btc_data['Datetime'], y=btc_data['Close'], 
                                  name='BTC/USD',
                                  line=dict(color='#FFBA08', width=2)))
        fig_btc.update_layout(get_chart_layout('BTC/USD Price'))
        st.plotly_chart(fig_btc, use_container_width=True)
        
        # Volume chart
        fig_volume = go.Figure()
        fig_volume.add_trace(go.Bar(x=btc_data['Datetime'], y=btc_data['Volume'], 
                                 name='Volume',
                                 marker_color='#FFBA08'))
        fig_volume.update_layout(get_chart_layout('BTC/USD Trading Volume'))
        st.plotly_chart(fig_volume, use_container_width=True)
        
        # Last 5 values table
        st.subheader('Latest BTC/USD Data')
        last_5_data = btc_data.head(5)[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']]
        last_5_data = last_5_data.round(2)
        st.dataframe(last_5_data)
        
    except Exception as e:
        st.error(f"Error in Crypto Markets: {str(e)}")

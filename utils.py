import sqlite3
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

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
    """
    Load BTC/USD minute data for the past 7 days (maximum available from yfinance).
    Data is sampled to reduce points for better visualization while maintaining
    price movement patterns.
    """
    try:
        conn = get_database_connection()
        # Get data from the last 7 days
        seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
        query = f"""
        SELECT Datetime, Open, High, Low, Close, Volume
        FROM btc_minute
        WHERE Datetime >= '{seven_days_ago}'
        ORDER BY Datetime DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            st.error("No BTC data available")
            raise ValueError("No BTC data available")
            
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        
        # If we have more than 1000 points, sample the data to reduce points
        # while maintaining the overall price movement pattern
        if len(df) > 1000:
            # Keep every Nth row to reduce to ~1000 points
            n = len(df) // 1000
            df = df.iloc[::n].copy()
        
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

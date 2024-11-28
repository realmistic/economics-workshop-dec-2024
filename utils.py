import sqlite3
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
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

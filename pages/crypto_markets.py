import streamlit as st
import plotly.graph_objects as go
from utils import load_btc_data, get_chart_layout

def show():
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

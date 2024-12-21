import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils import load_btc_data, get_chart_layout

def show():
    st.header('Cryptocurrency Markets')
        
    try:
        # Load BTC data
        btc_data = load_btc_data()
        
        if not btc_data.empty and btc_data['Close'].notna().any():
            # Price chart
            st.subheader('BTC/USD Price')
            latest_price = btc_data['Close'].iloc[0]  # First row is most recent in minute data
            latest_date = btc_data['Datetime'].iloc[0]
            
            caption = f'<span style="background-color: #31333F; padding: 2px 6px; border-radius: 3px;"><b>Latest data: {latest_date.strftime("%B %d, %Y %H:%M")}</b></span>'
            if pd.notna(latest_price):
                caption += f' | Price: ${latest_price:,.2f}'
            st.caption(caption, unsafe_allow_html=True)
            
            fig_btc = go.Figure()
            fig_btc.add_trace(go.Scatter(
                x=btc_data['Datetime'], 
                y=btc_data['Close'],
                name='BTC/USD',
                line=dict(color='#FFBA08', width=2),
                hovertemplate='Date: %{x}<br>Price: $%{y:,.2f}<extra></extra>'
            ))
            fig_btc.update_layout(get_chart_layout(''))
            st.plotly_chart(fig_btc, use_container_width=True)
            
            # Add explanatory text
            st.markdown("""
            * **Alternative Asset Class**: Cryptocurrencies represent a distinct asset class that historically has shown lower correlation with traditional investments like stocks and bonds, potentially offering portfolio diversification benefits.
            * **Real-Time Data Pipeline**: This dashboard displays minute-level BTC/USD data that updates with a 2-3 minute lag, demonstrating an automated data pipeline for near real-time market monitoring.
            """)

            # Volume chart
            st.subheader('BTC/USD Trading Volume')
            latest_volume = btc_data['Volume'].iloc[0]
            
            caption = f'<span style="background-color: #31333F; padding: 2px 6px; border-radius: 3px;"><b>Latest data: {latest_date.strftime("%B %d, %Y %H:%M")}</b></span>'
            if pd.notna(latest_volume):
                caption += f' | Volume: {latest_volume:,.0f}'
            st.caption(caption, unsafe_allow_html=True)
            
            fig_volume = go.Figure()
            fig_volume.add_trace(go.Bar(
                x=btc_data['Datetime'], 
                y=btc_data['Volume'],
                name='Volume',
                marker_color='#FFBA08',
                hovertemplate='Date: %{x}<br>Volume: %{y:,.0f}<extra></extra>'
            ))
            fig_volume.update_layout(get_chart_layout(''))
            st.plotly_chart(fig_volume, use_container_width=True)
            
            # Last 5 values table
            st.subheader('Latest BTC/USD Data')
            last_5_data = btc_data.head(5)[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']]
            # Format the columns
            last_5_data = pd.DataFrame({
                'Time': last_5_data['Datetime'].dt.strftime('%Y-%m-%d %H:%M'),
                'Open': last_5_data['Open'].map('${:,.2f}'.format),
                'High': last_5_data['High'].map('${:,.2f}'.format),
                'Low': last_5_data['Low'].map('${:,.2f}'.format),
                'Close': last_5_data['Close'].map('${:,.2f}'.format),
                'Volume': last_5_data['Volume'].map('{:,.0f}'.format)
            })
            st.dataframe(last_5_data, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error in Crypto Markets: {str(e)}")

import streamlit as st
import plotly.graph_objects as go
from utils import load_data, get_chart_layout

def show():
    st.header('Stock Market Overview')
    
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
        
        # Add S&P 500 commentary
        st.markdown("""
        **What Does This Show?**: The S&P 500 chart tracks the performance of 500 large U.S. companies. The moving averages (20-day, 50-day, and 200-day) smooth out short-term price fluctuations, showing long-term trends.

        **Impact on Everyday Investors**: The steady growth of the S&P 500 over the years indicates strong long-term returns for passive investors. However, short-term dips (like those seen in 2020 during the pandemic) are reminders that markets can be volatile.

        **Why It Matters**: For long-term investors, the upward trend encourages staying invested through market ups and downs. The moving averages can also signal potential changes in momentum—for example, when the index falls below a moving average, it may indicate a short-term slowdown.
        """)

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

        # Add VIX commentary
        st.markdown("""
        **What is the VIX?**: Often called the "fear gauge," the VIX measures expected market volatility. Higher values suggest that investors anticipate large price swings (uncertainty), while lower values mean the market is stable.

        **Impact on Investors**: Spikes in the VIX (e.g., during 2008, 2020) often coincide with major market downturns or crises. For passive investors, high VIX levels might feel unsettling, but historically, markets recover over time.

        **Why It Matters**: A lower VIX generally signals confidence in the market, making it a more favorable environment for investing. However, investors should be cautious when the VIX rises sharply, as it often signals turbulence in the stock market.

        **Key Takeaways for the Average Citizen**:
        * **For Long-Term Investors**: The steady upward trend in the S&P 500 highlights the importance of patience and not reacting to short-term market volatility.
        * **For Understanding Volatility**: The VIX is a helpful indicator to monitor market uncertainty, but remember that spikes in volatility are often short-lived and do not derail long-term growth.
        """)

    except Exception as e:
        st.error(f"Error in Stock Market Overview: {str(e)}")

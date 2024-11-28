import streamlit as st
import plotly.graph_objects as go
from utils import load_data, get_chart_layout

def show():
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
        
        # Add Commentary for Trade Weighted U.S. Dollar Index
        st.markdown("""
        **What is the Dollar Index?**: The Trade Weighted Dollar Index measures the U.S. dollar's strength against a basket of major world currencies. A rising index means the dollar is getting stronger compared to other currencies, while a falling index indicates it's getting weaker.

        **Impact on Global Trade**: When the dollar strengthens (index rises), U.S. exports become more expensive for other countries, potentially reducing international sales. However, imports become cheaper for U.S. consumers and businesses. The opposite occurs when the dollar weakens.

        **Why It Matters**: A stronger dollar can help control inflation by making imports cheaper, but it can hurt U.S. companies that sell products internationally. For travelers, a stronger dollar means more purchasing power when visiting other countries.
        """)
        
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

        # Add Commentary for EUR/USD Exchange Rate
        st.markdown("""
        **What is EUR/USD?**: This shows how many U.S. dollars one euro can buy. For example, if EUR/USD is 1.08, it means 1 euro can buy 1.08 U.S. dollars. This is one of the world's most traded currency pairs.

        **Current Trend**: The euro has been weakening against the dollar, as shown by the declining EUR/USD rate. This trend reflects stronger U.S. economic performance and differences in monetary policy between the Federal Reserve and European Central Bank.

        **Impact on Trade and Travel**: With the euro weakening against the dollar:
        - European goods are becoming cheaper for American buyers
        - U.S. products are becoming more expensive in Europe
        - Travel to Europe is becoming more affordable for Americans
        - European companies earning dollars (through exports) benefit when converting back to euros
        
        **Key Takeaways for the Average Citizen:**

        - For U.S. Travelers: Now might be a good time to plan European trips as your dollars will buy more euros
        - For U.S. Consumers: European imports (like wines, cars, or luxury goods) may become more affordable
        - For Investors: Consider how currency weakness might boost European export-oriented companies, while potentially creating headwinds for U.S. companies with large European operations
        """)
    except Exception as e:
        st.error(f"Error in Currency Markets: {str(e)}")

import streamlit as st
import plotly.graph_objects as go
from utils import load_data, get_chart_layout

def show():
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

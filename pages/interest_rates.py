import streamlit as st
import plotly.graph_objects as go
from utils import load_data, get_chart_layout

def show():
    st.header('Interest Rates')
    
    try:
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

        # Add Fed Funds Rate commentary
        st.markdown("""
        **What is the Federal Funds Rate?**: This is the interest rate that banks charge each other for short-term loans. The Federal Reserve (the U.S. central bank) sets this rate to help control inflation and keep the economy stable. When the Fed raises the rate, borrowing becomes more expensive.

        **Impact on Mortgages and Loans**: When the Fed raises rates, mortgage rates and loan interest rates typically go up. This means your monthly mortgage payments could increase if you're taking out a new loan or refinancing your mortgage. It also affects credit card rates and car loans, so borrowing can become more costly.

        **What Does This Mean for You?**: If you're thinking about buying a home or taking out a loan, you may want to consider doing so sooner rather than later, before rates rise further. On the other hand, if you have savings or a fixed-rate investment, you might not feel much impact from these changes.
        """)

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

        # Add Treasury Yields commentary
        st.markdown("""
        **What Are Treasury Yields?**: Treasury yields are the returns (or interest rates) that the U.S. government pays to borrow money for different periods (like 1 year, 5 years, or 10 years). The higher the yield, the more the government has to pay in interest to borrow money.

        **Impact on Savings and Mortgages**: When Treasury yields go up, interest rates on savings accounts, mortgages, and other loans often rise too. This means that if you have a mortgage or are planning to borrow money, your payments could go up. On the flip side, if you're saving money, you may get a better return on savings accounts or CDs.

        **Bond Yields vs. Stocks**: When yields (or interest rates) rise, bonds become more attractive because they pay higher interest. As a result, stock prices might fall a bit, as people may prefer safer investments like bonds over riskier ones like stocks. So, if you have some money in the stock market, rising yields could impact your investment returns.

        **Key Takeaways for Everyday Decisions**:
        * For Savings: If interest rates rise (both in Treasury yields and the Federal Funds Rate), you could earn more on your savings accounts, CDs, or bonds.
        * For Mortgages: Higher interest rates from the Fed or rising Treasury yields could lead to higher monthly mortgage payments or loan costs. If you're planning to buy a house or refinance, it may be better to do so sooner, before rates go up more.
        * For Investing in Stocks: Rising interest rates can make bonds more attractive, which could lead to lower stock prices in the short term. However, if you're a passive investor in stocks, it's important to stay focused on the long-term growth potential of your investments.
        """)

    except Exception as e:
        st.error(f"Error in Interest Rates: {str(e)}")

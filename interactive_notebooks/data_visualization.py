# Economic Data Visualization
# This script visualizes various economic indicators using Plotly.

#%%
# Import required libraries
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pathlib import Path
from sqlalchemy import create_engine
import os

#%%
# Setup database connection : 
# [Comment] Ivan: YOU CAN RUN IT INTERACTIVE FROM THIS WINDOW, or by calling "python interactive_notebooks/data_visualization.py" from the top project folder 
def get_db_path():
    """Get the database path whether running as script or interactively"""
    current_file = Path(__file__).resolve() if '__file__' in globals() else Path.cwd()
    if current_file.is_file():
        # Running as script
        return current_file.parent.parent / 'data' / 'economics_data.db'
    else:
        # Running interactively
        return current_file.parent / 'data' / 'economics_data.db'

db_path = get_db_path()
if not db_path.exists():
    print("Error: Database file not found!")
    print(f"Expected location: {db_path}")
else:
    # Create database connection
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Load all economic data from database
    print("Loading data from database...")
    unemployment = pd.read_sql('SELECT * FROM unrate', engine, parse_dates=['date']).set_index('date')
    cpi_core = pd.read_sql('SELECT * FROM cpilfesl', engine, parse_dates=['date']).set_index('date')
    cpi_all = pd.read_sql('SELECT * FROM cpiaucsl', engine, parse_dates=['date']).set_index('date')
    ireland_cpi = pd.read_sql('SELECT * FROM ireland_cpi', engine, parse_dates=['date']).set_index('date')
    euro_cpi = pd.read_sql('SELECT * FROM euro_cpi', engine, parse_dates=['date']).set_index('date')
    gdpc1 = pd.read_sql('SELECT * FROM gdpc1', engine, parse_dates=['date']).set_index('date')
    gdppot = pd.read_sql('SELECT * FROM gdppot', engine, parse_dates=['date']).set_index('date')
    fedfunds = pd.read_sql('SELECT * FROM fedfunds', engine, parse_dates=['date']).set_index('date')
    debt_to_gdp = pd.read_sql('SELECT * FROM gfdegdq188s', engine, parse_dates=['date']).set_index('date')
    dgs1 = pd.read_sql('SELECT * FROM dgs1', engine, parse_dates=['date']).set_index('date')
    dgs5 = pd.read_sql('SELECT * FROM dgs5', engine, parse_dates=['date']).set_index('date')
    dgs10 = pd.read_sql('SELECT * FROM dgs10', engine, parse_dates=['date']).set_index('date')
    dollar_index = pd.read_sql('SELECT * FROM dtwexbgs', engine, parse_dates=['date']).set_index('date')
    eurusd = pd.read_sql('SELECT * FROM dexuseu', engine, parse_dates=['date']).set_index('date')
    vix = pd.read_sql('SELECT * FROM vixcls', engine, parse_dates=['date']).set_index('date')
    sp500 = pd.read_sql('SELECT * FROM sp500', engine, parse_dates=['date']).set_index('date')
    print("Data loading completed!")

    #%% [markdown]
    # ## S&P 500 Price and Moving Averages

    #%%
    # Create S&P 500 price plot with moving averages
    fig_sp500 = go.Figure()
    fig_sp500.add_trace(go.Scatter(
        x=sp500.index,
        y=sp500['SP500'],
        name='S&P 500',
        line=dict(color='blue')
    ))
    fig_sp500.add_trace(go.Scatter(
        x=sp500.index,
        y=sp500['sp500_ma20'],
        name='20-day MA',
        line=dict(color='red', dash='dash')
    ))
    fig_sp500.add_trace(go.Scatter(
        x=sp500.index,
        y=sp500['sp500_ma50'],
        name='50-day MA',
        line=dict(color='green', dash='dash')
    ))
    fig_sp500.add_trace(go.Scatter(
        x=sp500.index,
        y=sp500['sp500_ma200'],
        name='200-day MA',
        line=dict(color='purple', dash='dash')
    ))
    fig_sp500.update_layout(
        title='S&P 500 Index with Moving Averages',
        yaxis_title='Index Value',
        template='plotly_white',
        hovermode='x unified'
    )
    fig_sp500.show()

    #%% [markdown]
    # ## S&P 500 Yearly Returns

    #%%
    # Create S&P 500 yearly returns plot
    fig_sp500_returns = go.Figure()
    fig_sp500_returns.add_trace(
        go.Scatter(x=sp500.index, y=sp500['sp500_returns_yearly'],
                  name='Yearly Returns', line=dict(color='blue'))
    )

    fig_sp500_returns.update_layout(
        title='S&P 500 Yearly Returns',
        yaxis_title='Yearly Returns',
        template='plotly_white',
        hovermode='x unified'
    )
    fig_sp500_returns.update_yaxes(tickformat='.2%')
    fig_sp500_returns.show()

    #%% [markdown]
    # ## Unemployment Rate Visualization

    #%%
    # Create Unemployment Rate plot
    fig_unemployment = go.Figure()
    fig_unemployment.add_trace(go.Scatter(
        x=unemployment.index,
        y=unemployment['UNRATE'],
        name='Unemployment Rate',
        line=dict(color='blue')
    ))
    fig_unemployment.add_trace(go.Scatter(
        x=unemployment.index,
        y=unemployment['unrate_ma3'],
        name='3-month MA',
        line=dict(color='red', dash='dash')
    ))
    fig_unemployment.add_trace(go.Scatter(
        x=unemployment.index,
        y=unemployment['unrate_ma12'],
        name='12-month MA',
        line=dict(color='green', dash='dash')
    ))
    fig_unemployment.update_layout(
        title='U.S. Unemployment Rate with Moving Averages',
        yaxis_title='Rate (%)',
        template='plotly_white',
        hovermode='x unified'
    )
    fig_unemployment.show()

    #%% [markdown]
    # ## CPI Comparison Visualization

    #%%
    # Create CPI Comparison plot
    fig_cpi = go.Figure()
    fig_cpi.add_trace(go.Scatter(
        x=cpi_core.index,
        y=cpi_core['cpi_core_yoy'],
        name='Core CPI (Less Food & Energy)',
        line=dict(color='blue')
    ))
    fig_cpi.add_trace(go.Scatter(
        x=cpi_all.index,
        y=cpi_all['cpi_all_yoy'],
        name='All Items CPI',
        line=dict(color='red')
    ))
    fig_cpi.update_layout(
        title='Core CPI vs All Items CPI (Year-over-Year Change)',
        yaxis_title='Change Rate',
        template='plotly_white',
        hovermode='x unified'
    )
    fig_cpi.update_yaxes(tickformat='.2%')
    fig_cpi.show()

    #%% [markdown]
    # ## Ireland and Euro Area CPI Comparison

    #%%
    # Create Ireland and Euro Area CPI Comparison plot
    fig_euro_cpi = go.Figure()
    fig_euro_cpi.add_trace(go.Scatter(
        x=ireland_cpi.index,
        y=ireland_cpi['cpi_ireland_yoy'],
        name='Ireland CPI',
        line=dict(color='green')
    ))
    fig_euro_cpi.add_trace(go.Scatter(
        x=euro_cpi.index,
        y=euro_cpi['cpi_euro_yoy'],
        name='Euro Area CPI',
        line=dict(color='blue')
    ))
    fig_euro_cpi.add_trace(go.Scatter(
        x=euro_cpi.index,
        y=cpi_all['cpi_all_yoy'],
        name='US CPI',
        line=dict(color='red')
    ))
    fig_euro_cpi.update_layout(
        title='Ireland vs Euro Area vs. US CPI (Year-over-Year Change)',
        yaxis_title='Change Rate',
        template='plotly_white',
        hovermode='x unified'
    )
    fig_euro_cpi.update_yaxes(tickformat='.2%')
    fig_euro_cpi.show()

    #%% [markdown]
    # ## GDP Growth Comparison

    #%%
    # Create GDP Growth Comparison plot
    fig_gdp_comparison = go.Figure()
    fig_gdp_comparison.add_trace(go.Scatter(
        x=gdppot.index,
        y=gdppot['gdppot_us_yoy'],
        name='Potential GDP Growth',
        line=dict(color='blue')
    ))
    fig_gdp_comparison.add_trace(go.Scatter(
        x=gdpc1.index,
        y=gdpc1['gdpc1_us_yoy'],
        name='Real GDP Growth',
        line=dict(color='red')
    ))
    fig_gdp_comparison.update_layout(
        title='US GDP Growth Comparison (YoY)',
        yaxis_title='Growth Rate (%)',
        yaxis_tickformat='.1%',
        hovermode='x unified',
        template='plotly_white'
    )
    fig_gdp_comparison.show()

    #%% [markdown]
    # ## Fed Funds Rate Visualization

    #%%
    # Create Fed Funds Rate plot
    fig_fedfunds = px.line(fedfunds, x=fedfunds.index, y='FEDFUNDS',
                           title='Federal Funds Rate')
    fig_fedfunds.update_layout(
        showlegend=False,
        yaxis_title='Rate (%)',
        template='plotly_white'
    )
    fig_fedfunds.show()

    #%% [markdown]
    # ## Federal Debt to GDP Visualization

    #%%
    # Create Federal Debt to GDP plot
    fig_debt_gdp = px.line(debt_to_gdp, x=debt_to_gdp.index, y='GFDEGDQ188S',
                           title='Federal Debt to GDP Ratio')
    fig_debt_gdp.update_layout(
        showlegend=False,
        yaxis_title='Ratio (%)',
        template='plotly_white'
    )
    fig_debt_gdp.show()

    #%% [markdown]
    # ## Treasury Yields Visualization

    #%%
    # Create Treasury Yields plot
    fig_treasury = go.Figure()
    fig_treasury.add_trace(go.Scatter(x=dgs1.index, y=dgs1['DGS1'], name='1-Year'))
    fig_treasury.add_trace(go.Scatter(x=dgs5.index, y=dgs5['DGS5'], name='5-Year'))
    fig_treasury.add_trace(go.Scatter(x=dgs10.index, y=dgs10['DGS10'], name='10-Year'))
    fig_treasury.update_layout(
        title='Treasury Yields',
        yaxis_title='Yield (%)',
        template='plotly_white',
        hovermode='x unified'
    )
    fig_treasury.show()

    #%% [markdown]
    # ## Trade Weighted U.S. Dollar Index Visualization

    #%%
    # Create Trade Weighted Dollar Index plot
    fig_dollar = go.Figure()
    fig_dollar.add_trace(go.Scatter(
        x=dollar_index.index,
        y=dollar_index['DTWEXBGS'],
        name='Dollar Index',
        line=dict(color='blue')
    ))
    fig_dollar.add_trace(go.Scatter(
        x=dollar_index.index,
        y=dollar_index['dollar_index_ma20'],
        name='20-day MA',
        line=dict(color='red', dash='dash')
    ))
    fig_dollar.add_trace(go.Scatter(
        x=dollar_index.index,
        y=dollar_index['dollar_index_ma50'],
        name='50-day MA',
        line=dict(color='green', dash='dash')
    ))
    fig_dollar.update_layout(
        title='Trade Weighted U.S. Dollar Index: Broad, Goods',
        yaxis_title='Index Value',
        template='plotly_white',
        hovermode='x unified'
    )
    fig_dollar.show()

    #%% [markdown]
    # ## EUR/USD Exchange Rate Visualization

    #%%
    # Create EUR/USD Exchange Rate plot
    fig_eurusd = go.Figure()
    fig_eurusd.add_trace(go.Scatter(
        x=eurusd.index,
        y=eurusd['DEXUSEU'],
        name='EUR/USD',
        line=dict(color='blue')
    ))
    fig_eurusd.add_trace(go.Scatter(
        x=eurusd.index,
        y=eurusd['eurusd_ma20'],
        name='20-day MA',
        line=dict(color='red', dash='dash')
    ))
    fig_eurusd.add_trace(go.Scatter(
        x=eurusd.index,
        y=eurusd['eurusd_ma50'],
        name='50-day MA',
        line=dict(color='green', dash='dash')
    ))
    fig_eurusd.update_layout(
        title='U.S. / Euro Foreign Exchange Rate',
        yaxis_title='Exchange Rate (USD per EUR)',
        template='plotly_white',
        hovermode='x unified'
    )
    fig_eurusd.show()

    #%% [markdown]
    # ## VIX Volatility Index Visualization

    #%%
    # Create VIX plot
    fig_vix = go.Figure()
    fig_vix.add_trace(go.Scatter(
        x=vix.index,
        y=vix['VIXCLS'],
        name='VIX',
        line=dict(color='red')
    ))
    fig_vix.add_trace(go.Scatter(
        x=vix.index,
        y=vix['vix_ma20'],
        name='20-day MA',
        line=dict(color='blue', dash='dash')
    ))
    fig_vix.add_trace(go.Scatter(
        x=vix.index,
        y=vix['vix_ma50'],
        name='50-day MA',
        line=dict(color='green', dash='dash')
    ))
    fig_vix.update_layout(
        title='VIX Volatility Index with Moving Averages',
        yaxis_title='VIX Value',
        template='plotly_white',
        hovermode='x unified'
    )
    fig_vix.show()

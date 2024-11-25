# # Economic Data Visualization
# This script visualizes various economic indicators using Plotly.
# 
# **Important**: Before running this script, make sure to run `data_retrieval.py` first to generate the required data files.

#%%
# Import required libraries
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pathlib import Path

#%%
# Check if data files exist
data_dir = Path('../data')  # Changed from '../data' to 'data'
required_files = [
    'unrate.parquet',
    'cpilfesl.parquet',
    'cpiaucsl.parquet',
    'ireland_cpi.parquet',
    'euro_cpi.parquet',
    'gdpc1.parquet',
    'gdppot.parquet',
    'fedfunds.parquet',
    'gfdegdq188s.parquet',
    'dgs1.parquet',
    'dgs5.parquet',
    'dgs10.parquet',
    'dtwexbgs.parquet',
    'dexuseu.parquet',
    'vixcls.parquet',
    'sp500.parquet'
]

missing_files = [f for f in required_files if not (data_dir / f).exists()]

if missing_files:
    print("Error: Missing required data files!")
    print("Please run data_retrieval.py first to generate the following files:")
    for file in missing_files:
        print(f"- {file}")
    print("\nRun this command in the terminal:")
    print("python scripts/data_retrieval.py")
else:
    # Load all economic data from parquet files
    print("Loading data files...")
    unemployment = pd.read_parquet(data_dir / 'unrate.parquet')
    cpi_core = pd.read_parquet(data_dir / 'cpilfesl.parquet')
    cpi_all = pd.read_parquet(data_dir / 'cpiaucsl.parquet')
    ireland_cpi = pd.read_parquet(data_dir / 'ireland_cpi.parquet')
    euro_cpi = pd.read_parquet(data_dir / 'euro_cpi.parquet')
    gdpc1 = pd.read_parquet(data_dir / 'gdpc1.parquet')
    gdppot = pd.read_parquet(data_dir / 'gdppot.parquet')
    fedfunds = pd.read_parquet(data_dir / 'fedfunds.parquet')
    debt_to_gdp = pd.read_parquet(data_dir / 'gfdegdq188s.parquet')
    dgs1 = pd.read_parquet(data_dir / 'dgs1.parquet')
    dgs5 = pd.read_parquet(data_dir / 'dgs5.parquet')
    dgs10 = pd.read_parquet(data_dir / 'dgs10.parquet')
    dollar_index = pd.read_parquet(data_dir / 'dtwexbgs.parquet')
    eurusd = pd.read_parquet(data_dir / 'dexuseu.parquet')
    vix = pd.read_parquet(data_dir / 'vixcls.parquet')
    sp500 = pd.read_parquet(data_dir / 'sp500.parquet')
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

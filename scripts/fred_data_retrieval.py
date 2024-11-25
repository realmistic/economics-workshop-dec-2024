import os
import time
import pandas as pd
from pandas_datareader import data as pdr
from sqlalchemy import create_engine
from tqdm import tqdm

# Directory to save data
DATA_DIR = 'data'

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# SQLite database path
DB_PATH = os.path.join(DATA_DIR, 'economics_data.db')

# Create SQLAlchemy engine
engine = create_engine(f'sqlite:///{DB_PATH}')

def fetch_macro(min_date=None):
    '''Fetch Macro data from FRED (using Pandas datareader)'''
    
    if min_date is None:
        min_date = "1970-01-01"
    else:
        min_date = pd.to_datetime(min_date)
    
    # List of metrics to fetch
    metrics = [
        ("UNRATE", "Unemployment Rate"),
        ("CPILFESL", "Core CPI"),
        ("CPIAUCSL", "All Items CPI"),
        ("CP0000IEM086NEST", "Ireland CPI"),
        ("CP0000EZ19M086NEST", "Euro Area CPI"),
        ("GDPC1", "Real Gross Domestic Product"),
        ("GDPPOT", "Real Potential GDP"),
        ("FEDFUNDS", "Fed Funds Rate"),
        ("GFDEGDQ188S", "Federal Debt to GDP"),
        ("DGS1", "1-Year Treasury"),
        ("DGS5", "5-Year Treasury"),
        ("DGS10", "10-Year Treasury"),
        ("DTWEXBGS", "Trade Weighted U.S. Dollar Index: Broad, Goods"),
        ("DEXUSEU", "U.S. / Euro Foreign Exchange Rate"),
        ("VIXCLS", "VIX Volatility Index"),
        ("SP500", "S&P 500")
    ]
    
    data = {}
    for metric_code, metric_name in tqdm(metrics, desc="Fetching economic data"):
        # Real Gross Domestic Product (GDPC1), Billions of Chained 2012 Dollars, QUARTERLY
        if metric_code == "GDPC1":
            gdpc1 = pdr.DataReader(metric_code, "fred", start=min_date)
            gdpc1['gdpc1_us_yoy'] = gdpc1.GDPC1 / gdpc1.GDPC1.shift(4) - 1
            gdpc1['gdpc1_us_qoq'] = gdpc1.GDPC1 / gdpc1.GDPC1.shift(1) - 1
            data['gdpc1'] = gdpc1[['gdpc1_us_yoy','gdpc1_us_qoq']]

        # Real Potential Gross Domestic Product (GDPPOT), Billions of Chained 2012 Dollars, QUARTERLY
        elif metric_code == "GDPPOT":
            gdppot = pdr.DataReader(metric_code, "fred", start=min_date)
            gdppot['gdppot_us_yoy'] = gdppot.GDPPOT / gdppot.GDPPOT.shift(4) - 1
            gdppot['gdppot_us_qoq'] = gdppot.GDPPOT / gdppot.GDPPOT.shift(1) - 1
            data['gdppot'] = gdppot[['gdppot_us_yoy','gdppot_us_qoq']]
        
        # Core CPI index
        elif metric_code == "CPILFESL":
            cpilfesl = pdr.DataReader(metric_code, "fred", start=min_date)
            cpilfesl['cpi_core_yoy'] = cpilfesl.CPILFESL / cpilfesl.CPILFESL.shift(12) - 1
            cpilfesl['cpi_core_mom'] = cpilfesl.CPILFESL / cpilfesl.CPILFESL.shift(1) - 1
            data['cpilfesl'] = cpilfesl[['cpi_core_yoy','cpi_core_mom']]
            
        # All Items CPI index
        elif metric_code == "CPIAUCSL":
            cpiaucsl = pdr.DataReader(metric_code, "fred", start=min_date)
            cpiaucsl['cpi_all_yoy'] = cpiaucsl.CPIAUCSL / cpiaucsl.CPIAUCSL.shift(12) - 1
            cpiaucsl['cpi_all_mom'] = cpiaucsl.CPIAUCSL / cpiaucsl.CPIAUCSL.shift(1) - 1
            data['cpiaucsl'] = cpiaucsl[['cpi_all_yoy','cpi_all_mom']]

        # Ireland CPI
        elif metric_code == "CP0000IEM086NEST":
            ireland_cpi = pdr.DataReader(metric_code, "fred", start=min_date)
            ireland_cpi['cpi_ireland_yoy'] = ireland_cpi.CP0000IEM086NEST / ireland_cpi.CP0000IEM086NEST.shift(12) - 1
            ireland_cpi['cpi_ireland_mom'] = ireland_cpi.CP0000IEM086NEST / ireland_cpi.CP0000IEM086NEST.shift(1) - 1
            data['ireland_cpi'] = ireland_cpi[['cpi_ireland_yoy','cpi_ireland_mom']]

        # Euro Area CPI
        elif metric_code == "CP0000EZ19M086NEST":
            euro_cpi = pdr.DataReader(metric_code, "fred", start=min_date)
            euro_cpi['cpi_euro_yoy'] = euro_cpi.CP0000EZ19M086NEST / euro_cpi.CP0000EZ19M086NEST.shift(12) - 1
            euro_cpi['cpi_euro_mom'] = euro_cpi.CP0000EZ19M086NEST / euro_cpi.CP0000EZ19M086NEST.shift(1) - 1
            data['euro_cpi'] = euro_cpi[['cpi_euro_yoy','cpi_euro_mom']]
        
        # VIX Volatility Index
        elif metric_code == "VIXCLS":
            vix = pdr.DataReader(metric_code, "fred", start=min_date)
            # Calculate rolling metrics for VIX
            vix['vix_ma20'] = vix.VIXCLS.rolling(window=20).mean()
            vix['vix_ma50'] = vix.VIXCLS.rolling(window=50).mean()
            data['vixcls'] = vix
            
        # Trade Weighted U.S. Dollar Index
        elif metric_code == "DTWEXBGS":
            dtwexbgs = pdr.DataReader(metric_code, "fred", start=min_date)
            # Calculate rolling averages for the dollar index
            dtwexbgs['dollar_index_ma20'] = dtwexbgs.DTWEXBGS.rolling(window=20).mean()
            dtwexbgs['dollar_index_ma50'] = dtwexbgs.DTWEXBGS.rolling(window=50).mean()
            data['dtwexbgs'] = dtwexbgs
            
        # U.S. / Euro Exchange Rate
        elif metric_code == "DEXUSEU":
            dexuseu = pdr.DataReader(metric_code, "fred", start=min_date)
            # Calculate rolling averages for EUR/USD
            dexuseu['eurusd_ma20'] = dexuseu.DEXUSEU.rolling(window=20).mean()
            dexuseu['eurusd_ma50'] = dexuseu.DEXUSEU.rolling(window=50).mean()
            data['dexuseu'] = dexuseu
            
        # Unemployment Rate
        elif metric_code == "UNRATE":
            unrate = pdr.DataReader(metric_code, "fred", start=min_date)
            # Calculate rolling averages for unemployment
            unrate['unrate_ma3'] = unrate.UNRATE.rolling(window=3).mean()
            unrate['unrate_ma12'] = unrate.UNRATE.rolling(window=12).mean()
            data['unrate'] = unrate

        # S&P 500
        elif metric_code == "SP500":
            sp500 = pdr.DataReader(metric_code, "fred", start=min_date)
            # Calculate rolling averages and returns for S&P 500
            sp500['sp500_ma20'] = sp500.SP500.rolling(window=20).mean()
            sp500['sp500_ma50'] = sp500.SP500.rolling(window=50).mean()
            sp500['sp500_ma200'] = sp500.SP500.rolling(window=200).mean()
            sp500['sp500_returns_daily'] = sp500.SP500.pct_change()
            sp500['sp500_returns_monthly'] = sp500.SP500 / sp500.SP500.shift(20) - 1
            sp500['sp500_returns_yearly'] = sp500.SP500 / sp500.SP500.shift(252) - 1
            data['sp500'] = sp500
        
        # Other metrics
        else:
            data[metric_code.lower()] = pdr.DataReader(metric_code, "fred", start=min_date)
        
        # Sleep to avoid overloading the API
        time.sleep(1)
    
    # Save to parquet and SQLite
    print("\nSaving data to files...")
    for name, df in tqdm(data.items(), desc="Saving data"):
        
        # Skip saving to parquet
        # df.to_parquet(os.path.join(DATA_DIR, f'{name}.parquet'))
        
        # Save to SQLite
        df.to_sql(name, engine, if_exists='replace')

def main():
    fetch_macro()

if __name__ == '__main__':
    main()

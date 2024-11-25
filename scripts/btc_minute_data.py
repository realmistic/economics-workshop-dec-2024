import os
import yfinance as yf
import pandas as pd
import time
import argparse
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

# Directory to save data
DATA_DIR = 'data'

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# SQLite database path
DB_PATH = os.path.join(DATA_DIR, 'economics_data.db')

# Create SQLAlchemy engine
engine = create_engine(f'sqlite:///{DB_PATH}')

def get_latest_timestamp():
    """Get the latest timestamp from the database"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT MAX(Datetime) FROM btc_minute"))
            latest = result.scalar()
            if latest:
                # Convert to UTC timezone-aware timestamp
                return pd.to_datetime(latest).tz_localize('UTC')
            return None
    except Exception as e:
        print(f"Error getting latest timestamp: {e}")
        return None

def get_btc_minute_data():
    """
    Fetch minute-level data for BTC-USD and save it to SQLite database.
    """
    try:
        print(f"\n{datetime.now()} - Fetching data...")
        
        # Get the latest timestamp from the database
        latest_ts = get_latest_timestamp()
        if latest_ts:
            print(f"Latest timestamp in database: {latest_ts}")
        
        # Download data using yf.download with 1d period and 1m interval
        df = yf.download(
            tickers="BTC-USD",
            interval="1m",
            period="1d"  # Changed from 60m to 1d
        )
        
        if df.empty:
            print("No data received")
            return None
        
        print(f"\nReceived data shape: {df.shape}")
        
        # Filter for only new data if we have existing data
        if latest_ts:
            # Make sure both timestamps are UTC aware for comparison
            df = df[df.index.tz_localize(None).tz_localize('UTC') > latest_ts]
            if df.empty:
                print("No new data to add")
                return None
            print(f"New data shape after filtering: {df.shape}")
        
        print("\nFirst few rows:")
        print(df.head())
        
        # Create a new DataFrame while preserving the index
        new_df = df.copy()
        new_df.columns = ['Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume']
        new_df['fetch_timestamp'] = datetime.now()
        
        # Convert index to timezone-naive for SQLite storage
        new_df.index = new_df.index.tz_localize(None)
        
        # Print column names for debugging
        print("\nDataFrame columns before saving:")
        print(new_df.columns.tolist())
        
        # Append to SQLite with unique index to avoid duplicates
        try:
            new_df.to_sql('btc_minute', engine, if_exists='append', index=True, index_label='Datetime')
            print(f"\nAdded {len(new_df)} new records to database")
            print("\nLatest data point:")
            print(new_df.tail(1)[['Open', 'High', 'Low', 'Close', 'Volume', 'Adj_Close']])
            
            # Print total records in database
            with engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM btc_minute"))
                total_records = result.scalar()
                print(f"\nTotal records in database: {total_records}")
                
        except Exception as e:
            if 'UNIQUE constraint failed' in str(e):
                print("Duplicate data point - skipping")
            else:
                print(f"Error saving to database: {e}")
                # Print the actual SQL for debugging
                print("\nDataFrame dtypes:")
                print(new_df.dtypes)
        
        return df
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return None

def continuous_fetch(interval_seconds=60):
    """
    Continuously fetch BTC minute data at specified intervals.
    
    Args:
        interval_seconds (int): Seconds to wait between fetches
    """
    print(f"Starting continuous BTC-USD data collection (interval: {interval_seconds} seconds)")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            get_btc_minute_data()
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\nStopping data collection")

def setup_database():
    """Create the database table if it doesn't exist"""
    create_table_sql = text("""
    CREATE TABLE IF NOT EXISTS btc_minute (
        Datetime TIMESTAMP PRIMARY KEY,
        Open REAL,
        High REAL,
        Low REAL,
        Close REAL,
        Volume REAL,
        Adj_Close REAL,
        fetch_timestamp TIMESTAMP
    )
    """)
    
    with engine.connect() as conn:
        conn.execute(create_table_sql)
        conn.commit()

def main():
    parser = argparse.ArgumentParser(
        description='BTC Minute Data Collector',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    mode_choices = ['continuous', 'once']
    parser.add_argument(
        '--mode',
        type=str,
        choices=mode_choices,
        default='once',
        metavar='MODE',
        help='Execution mode:\n'
             '  continuous - Keep running and fetch data at regular intervals\n'
             '  once      - Single fetch and exit (default)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=60,
        metavar='SECONDS',
        help='Interval in seconds between fetches in continuous mode (default: 60)'
    )
    
    args = parser.parse_args()
    
    # Setup database
    setup_database()
    
    # Execute based on mode
    if args.mode == 'continuous':
        continuous_fetch(args.interval)
    else:
        get_btc_minute_data()

if __name__ == "__main__":
    main()

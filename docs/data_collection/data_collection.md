# Data Collection Module

The data collection module is responsible for fetching XRP-related data from various APIs and storing it in the database. It consists of three main components:

## CoinGecko Client (coingecko_client.py)

This client interacts with the CoinGecko API to fetch XRP market data.

### Key Features:
- Fetches current XRP market data
- Retrieves historical XRP market data

### Main Methods:
- `get_xrp_data()`: Fetches current XRP market data
- `get_xrp_historical_data(days, interval)`: Retrieves historical XRP market data

## CoinAPI Client (coinapi_client.py)

This client interacts with the CoinAPI to fetch OHLCV (Open, High, Low, Close, Volume) data for XRP.

### Key Features:
- Fetches latest OHLCV data
- Retrieves historical OHLCV data
- Respects API daily limit

### Main Methods:
- `get_ohlcv_data()`: Fetches the latest OHLCV data
- `get_historical_ohlcv_data(start_time, end_time, limit)`: Retrieves historical OHLCV data

## Data Collector (collector.py)

This script orchestrates the data collection process, using both the CoinGecko and CoinAPI clients to fetch and store data.

### Key Features:
- Collects and stores market data
- Collects and stores OHLCV data
- Handles historical data collection

### Main Functions:
- `collect_and_store_market_data(db)`: Collects and stores current market data
- `collect_and_store_ohlcv_data(db)`: Collects and stores current OHLCV data
- `collect_historical_data(db, start_date, end_date)`: Collects and stores historical OHLCV data
- `run_data_collection(db)`: Runs the main data collection process

## Usage

The data collection process can be initiated by running the collector.py script directly. It will use the configured database session to store the collected data.

```python
from src.models.base import SessionLocal

db = SessionLocal()
try:
    run_data_collection(db)
finally:
    db.close()
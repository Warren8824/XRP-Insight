# collector.py

This file contains functions for collecting and storing XRP market and OHLCV data from CoinGecko and CoinAPI, respectively. It also includes a function for collecting historical data.

## Functions

### collect_and_store_market_data(db: Session)
Collects the latest XRP market data from CoinGecko and stores it in the database.

- Uses `CoinGeckoClient` to fetch data
- Stores data in the `MarketData15Min` table

### collect_and_store_ohlcv_data(db: Session)
Collects the latest XRP OHLCV data from CoinAPI and stores it in the database.

- Uses `CoinAPIClient` to fetch data
- Stores data in the `OHLCVData15Min` table

### collect_historical_data(db: Session, start_date: datetime, end_date: datetime)
Collects historical OHLCV data for a specified date range and stores it in the database.

- Uses `CoinAPIClient` to fetch historical data
- Processes data in daily chunks
- Stores data in the `OHLCVData15Min` table

### run_data_collection(db: Session)
Runs the data collection process for both market and OHLCV data.

## Usage

The script can be run as a standalone module:

```python
if __name__ == "__main__":
    from src.models.base import SessionLocal

    db = SessionLocal()
    try:
        run_data_collection(db)
    finally:
        db.close()
        logger.info("Database connection closed.")
```

## Error Handling
All functions include try-except blocks to catch and log any exceptions that occur during the data collection process. In case of an error, the database transaction is rolled back.

## Notes

- Ensure that the necessary database models (MarketData15Min and OHLCVData15Min) are properly defined.
- The script uses UTC timestamps for all data.
- Historical data collection is done in daily chunks to manage API rate limits.
- All operations are logged using the data_collection_logger.

## Potential Improvements

- Implement retrying mechanism for failed API calls.
- Add more granular error handling for different types of exceptions.
- Implement a mechanism to avoid duplicate data entries.
- Add data validation before storing in the database.
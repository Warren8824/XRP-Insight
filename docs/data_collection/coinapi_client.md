# coinapi_client.py

This file contains the `CoinAPIClient` class, which is responsible for interacting with the CoinAPI service to retrieve OHLCV (Open, High, Low, Close, Volume) data for XRP.

## Class: CoinAPIClient

### Initialization
The class is initialized with configuration values from the project's config file, including:
- Base URL for the API
- API key
- Daily API call limit
- Logger instance

### Methods

#### get_ohlcv_data()
Retrieves the latest OHLCV data for XRP/USD from Bitstamp.

- Endpoint: `{base_url}/ohlcv/BITSTAMP_SPOT_XRP_USD/latest`
- Parameters:
  - `period_id`: "15MIN" (15-minute intervals)
  - `limit`: 1 (retrieves only the latest data point)

Returns: JSON response from the API

#### get_historical_ohlcv_data(start_time, end_time=None, limit=daily_limit)
Retrieves historical OHLCV data for XRP/USD from Bitstamp.

- Endpoint: `{base_url}/ohlcv/BITSTAMP_SPOT_XRP_USD/history`
- Parameters:
  - `period_id`: "15MIN" (15-minute intervals)
  - `time_start`: Start time for the data retrieval (ISO format)
  - `time_end`: End time for the data retrieval (ISO format, optional)
  - `limit`: Number of data points to retrieve (default is the daily limit)

Returns: JSON response from the API

### Error Handling
Both methods use try-except blocks to catch and log any `RequestException` that may occur during the API calls.

## Usage Example

```python
from src.data_collection.coinapi_client import CoinAPIClient
from datetime import datetime, timedelta

client = CoinAPIClient()

# Get latest OHLCV data
latest_data = client.get_ohlcv_data()

# Get historical OHLCV data
start_time = datetime.now() - timedelta(days=7)
historical_data = client.get_historical_ohlcv_data(start_time)
```

## Notes

- Ensure that the config file contains the necessary API endpoints, keys, and limits.
- The client respects the daily API call limit specified in the config.
- All API calls are logged using the data_collection_logger.


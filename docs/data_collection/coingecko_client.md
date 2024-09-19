# coingecko_client.py

This file contains the `CoinGeckoClient` class, which is responsible for interacting with the CoinGecko API service to retrieve data for XRP.

## Class: CoinGeckoClient

### Initialization
The class is initialized with configuration values from the project's config file, including:
- Base URL for the API
- API key
- Logger instance

### Methods

#### get_xrp_data()
Retrieves the latest data for XRP from CoinGecko.

- Endpoint: `{base_url}/coins/ripple`
- Parameters:
  - `localization`: false
  - `tickers`: false
  - `market_data`: true
  - `community_data`: false
  - `developer_data`: false
  - `sparkline`: false

Returns: JSON response from the API containing current XRP data

#### get_xrp_historical_data(days=1, interval="15m")
Retrieves historical market chart data for XRP from CoinGecko.

- Endpoint: `{base_url}/coins/ripple/market_chart`
- Parameters:
  - `vs_currency`: "usd"
  - `days`: Number of days of data to retrieve (default is 1)
  - `interval`: Data interval (default is "15m" for 15 minutes)

Returns: JSON response from the API containing historical XRP data

### Error Handling
Both methods use try-except blocks to catch and log any `RequestException` that may occur during the API calls.

## Usage Example

```python
from src.data_collection.coingecko_client import CoinGeckoClient

client = CoinGeckoClient()

# Get latest XRP data
latest_data = client.get_xrp_data()

# Get historical XRP data for the last 7 days with 15-minute intervals
historical_data = client.get_xrp_historical_data(days=7, interval="15m")
```

## Notes

- Ensure that the config file contains the necessary API endpoint and key for CoinGecko.
- All API calls are logged using the data_collection_logger.
- The CoinGecko API has rate limits. Make sure to respect these limits in your application logic.
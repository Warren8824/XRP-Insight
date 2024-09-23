import requests
from ..utils.config import config
from ..utils.logger import data_collection_logger


class CoinAPIClient:
    """
    A client for interacting with the CoinAPI service.

    This class provides methods to fetch OHLCV (Open, High, Low, Close, Volume) data
    for XRP/USD from the Bitstamp exchange via CoinAPI.

    Attributes:
        base_url (str): The base URL for the CoinAPI service.
        api_key (str): The API key for authenticating with CoinAPI.
        daily_limit (int): The daily limit for API calls.
        logger (Logger): Logger for recording operations and errors.
    """

    def __init__(self):
        """
        Initialize the CoinAPIClient with configuration settings.
        """
        self.base_url = config["api_endpoints"]["coinapi"]
        self.api_key = config["api_keys"]["coinapi"]
        self.daily_limit = config["api_limits"]["coinapi_daily"]
        self.logger = data_collection_logger

    def get_ohlcv_data(self):
        """
        Fetch the latest OHLCV data for XRP/USD.

        This method retrieves the most recent 15-minute OHLCV data point
        for the XRP/USD pair from the Bitstamp exchange.

        Returns:
            list: A list containing a single dictionary with the latest OHLCV data.

        Raises:
            requests.exceptions.RequestException: If there's an error in the API request.
        """
        endpoint = f"{self.base_url}/ohlcv/BITSTAMP_SPOT_XRP_USD/latest"
        params = {"period_id": "15MIN", "limit": 1}
        headers = {"X-CoinAPI-Key": self.api_key}

        self.logger.info(f"Requesting OHLCV data from endpoint: {endpoint}")

        try:
            response = requests.get(endpoint, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error retrieving OHLCV data: {str(e)}")
            raise

    def get_historical_ohlcv_data(
        self, start_time, end_time=None, limit=config["api_limits"]["coinapi_daily"]
    ):
        """
        Fetch historical OHLCV data for XRP/USD within a specified time range.

        This method retrieves 15-minute interval OHLCV data for the XRP/USD pair
        from the Bitstamp exchange, starting from the specified start time up to
        either the specified end time or the API call limit.

        Args:
            start_time (datetime): The start time for the historical data.
            end_time (datetime, optional): The end time for the historical data.
            If not provided, data up to the latest available point will be fetched.
            limit (int, optional): The maximum number of data points to retrieve.
            Defaults to the daily API call limit.

        Returns:
            list: A list of dictionaries, each containing OHLCV data for a 15-minute interval.

        Raises:
            requests.exceptions.RequestException: If there's an error in the API request.
        """
        endpoint = f"{self.base_url}/ohlcv/BITSTAMP_SPOT_XRP_USD/history"
        params = {
            "period_id": "15MIN",
            "time_start": start_time.isoformat()
        }
        if end_time:
            params["time_end"] = end_time.isoformat()
            params["limit"] = min(limit, self.daily_limit)  # Ensure we don't exceed daily limit(100 candles equals one api call credit)

        headers = {"X-CoinAPI-Key": self.api_key, "Accept": "application/json"}

        self.logger.info(f"Requesting historical OHLCV data from endpoint: {endpoint}")
        self.logger.info(f"Parameters: {params}")
        self.logger.info(f"Headers: {headers}")
        try:
            response = requests.get(endpoint, params=params, headers=headers)
            response.raise_for_status()
            self.logger.info("Successfully retrieved historical OHLCV data")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error retrieving historical OHLCV data: {str(e)}")
            if hasattr(e.response, 'text'):
                self.logger.error(f"Response content: {e.response.text}")
            raise

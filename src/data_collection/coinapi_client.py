import requests
from ..utils.config import config
from ..utils.logger import data_collection_logger


class CoinAPIClient:
    def __init__(self):
        self.base_url = config["api_endpoints"]["coinapi"]
        self.api_key = config["api_keys"]["coinapi"]
        self.daily_limit = config["api_limits"]["coinapi_daily"]
        self.logger = data_collection_logger

    def get_ohlcv_data(self):
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
        endpoint = f"{self.base_url}/ohlcv/BITSTAMP_SPOT_XRP_USD/history"
        params = {
            "period_id": "15MIN",
            "time_start": start_time.isoformat(),
            "limit": min(limit, self.daily_limit),  # Ensure we don't exceed daily limit
        }
        if end_time:
            params["time_end"] = end_time.isoformat()

        headers = {"X-CoinAPI-Key": self.api_key}

        self.logger.info(f"Requesting historical OHLCV data from endpoint: {endpoint}")
        self.logger.info(f"Parameters: {params}")
        try:
            response = requests.get(endpoint, params=params, headers=headers)
            response.raise_for_status()
            self.logger.info("Successfully retrieved historical OHLCV data")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error retrieving historical OHLCV data: {str(e)}")
            raise

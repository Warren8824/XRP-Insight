import requests
from src.utils.config import config


class CoinAPIClient:
    def __init__(self):
        self.base_url = config['api_endpoints']['coinapi']
        self.api_key = config['api_keys']['coinapi']
        self.daily_limit = config['api_limits']['coinapi_daily']

    def get_ohlcv_data(self):
        endpoint = f"{self.base_url}/ohlcv/BITSTAMP_SPOT_XRP_USD/latest"
        params = {
            "period_id": "15MIN",
            "limit": 1
        }
        headers = {"X-CoinAPI-Key": self.api_key}

        response = requests.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_historical_ohlcv_data(self, start_time, end_time=None, limit=config['api_limits']['coinapi_daily']):
        endpoint = f"{self.base_url}/ohlcv/BITSTAMP_SPOT_XRP_USD/history"
        params = {
            "period_id": "15MIN",
            "time_start": start_time.isoformat(),
            "limit": min(limit, self.daily_limit)  # Ensure we don't exceed daily limit
        }
        if end_time:
            params["time_end"] = end_time.isoformat()

        headers = {"X-CoinAPI-Key": self.api_key}

        response = requests.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

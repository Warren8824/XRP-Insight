import requests
from ..utils.config import config
from ..utils.logger import data_collection_logger


class CoinGeckoClient:
    def __init__(self):
        self.base_url = config["api_endpoints"]["coingecko"]
        self.api_key = config["api_keys"]["coingecko"]
        self.logger = data_collection_logger

    def get_market_data(self):
        endpoint = f"{self.base_url}/coins/ripple"
        params = {
            "localization": "false",
            "tickers": "false",
            "market_data": "true",
            "community_data": "false",
            "developer_data": "false",
            "sparkline": "false",
        }
        headers = {"X-Cg-Pro-Api-Key": self.api_key}

        # Log the request
        self.logger.info(f"Requesting XRP data from CoinGecko endpoint: {endpoint}")

        try:
            response = requests.get(endpoint, params=params, headers=headers)
            response.raise_for_status()
            self.logger.info("Successfully retrieved XRP data from CoinGecko")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error retrieving XRP data from CoinGecko: {str(e)}")
            raise

    def get_historical_market_data(self, days=1, interval="15m"):
        endpoint = f"{self.base_url}/coins/ripple/market_chart"
        params = {"vs_currency": "usd", "days": days, "interval": interval}
        headers = {"X-Cg-Pro-Api-Key": self.api_key}

        # Log the request
        self.logger.info(
            f"Requesting XRP historical data from CoinGecko endpoint: {endpoint}"
        )
        self.logger.info(f"Parameters: {params}")

        try:
            response = requests.get(endpoint, params=params, headers=headers)
            response.raise_for_status()
            self.logger.info(
                "Successfully retrieved XRP historical data from CoinGecko"
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(
                f"Error retrieving XRP historical data from CoinGecko: {str(e)}"
            )
            raise

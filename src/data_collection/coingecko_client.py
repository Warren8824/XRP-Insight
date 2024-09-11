import requests
from src.utils.config import config


class CoinGeckoClient:
    def __init__(self):
        self.base_url = config['api_endpoints']['coingecko']
        self.api_key = config['api_keys']['coingecko']

    def get_xrp_data(self):
        endpoint = f"{self.base_url}/coins/ripple"
        params = {
            "localization": "false",
            "tickers": "false",
            "market_data": "true",
            "community_data": "false",
            "developer_data": "false",
            "sparkline": "false"
        }
        headers = {"X-Cg-Pro-Api-Key": self.api_key}

        response = requests.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_xrp_historical_data(self, days=1, interval="15m"):
        endpoint = f"{self.base_url}/coins/ripple/market_chart"
        params = {
            "vs_currency": "usd",
            "days": days,
            "interval": interval
        }
        headers = {"X-Cg-Pro-Api-Key": self.api_key}

        response = requests.get(endpoint, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

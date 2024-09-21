import unittest
from unittest.mock import patch, MagicMock
from src.data_collection.coingecko_client import CoinGeckoClient
from src.utils.config import config


class TestCoinGeckoClient(unittest.TestCase):
    def setUp(self):
        self.client = CoinGeckoClient()

    @patch("src.data_collection.coingecko_client.requests.get")
    def test_get_xrp_data(self, mock_get):
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": "xrp_data"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call the method
        result = self.client.get_xrp_data()

        # Assert the result
        self.assertEqual(result, {"test": "xrp_data"})

        # Assert the correct URL and parameters were used
        expected_url = f"{config['api_endpoints']['coingecko']}/coins/ripple"
        expected_params = {
            "localization": "false",
            "tickers": "false",
            "market_data": "true",
            "community_data": "false",
            "developer_data": "false",
            "sparkline": "false",
        }
        expected_headers = {"X-Cg-Pro-Api-Key": config["api_keys"]["coingecko"]}
        mock_get.assert_called_once_with(
            expected_url, params=expected_params, headers=expected_headers
        )

    @patch("src.data_collection.coingecko_client.requests.get")
    def test_get_xrp_historical_data(self, mock_get):
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {"test": "historical_data"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call the method
        result = self.client.get_xrp_historical_data(days=2, interval="30m")

        # Assert the result
        self.assertEqual(result, {"test": "historical_data"})

        # Assert the correct URL and parameters were used
        expected_url = (
            f"{config['api_endpoints']['coingecko']}/coins/ripple/market_chart"
        )
        expected_params = {"vs_currency": "usd", "days": 2, "interval": "30m"}
        expected_headers = {"X-Cg-Pro-Api-Key": config["api_keys"]["coingecko"]}
        mock_get.assert_called_once_with(
            expected_url, params=expected_params, headers=expected_headers
        )

    @patch("src.data_collection.coingecko_client.requests.get")
    def test_get_xrp_data_error(self, mock_get):
        # Mock the response to raise an exception
        mock_get.side_effect = Exception("API Error")

        # Assert that the method raises an exception
        with self.assertRaises(Exception):
            self.client.get_xrp_data()


if __name__ == "__main__":
    unittest.main()

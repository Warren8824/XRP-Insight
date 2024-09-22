import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from src.data_collection.coinapi_client import CoinAPIClient
from src.utils.config import config


class TestCoinAPIClient(unittest.TestCase):
    def setUp(self):
        """
           Set up a CoinAPIClient instance for use in all test methods.
           This method is run before each test.
        """
        self.client = CoinAPIClient()

    @patch("src.data_collection.coinapi_client.requests.get")
    def test_get_ohlcv_data(self, mock_get):
        """
            Test the get_ohlcv_data method of CoinAPIClient.

            This test mocks the requests.get function to return a predefined OHLCV data response.
            It then calls the get_ohlcv_data method and verifies that:
            1. The returned data has the expected structure and values.
            2. The API was called with the correct URL, parameters, and headers.

            Args:
                mock_get: A mocked requests.get function.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "time_period_start": "2023-01-01T00:00:00.0000000Z",
                "time_period_end": "2023-01-01T00:15:00.0000000Z",
                "time_open": "2023-01-01T00:00:00.0000000Z",
                "time_close": "2023-01-01T00:14:59.9999999Z",
                "price_open": 0.3384,
                "price_high": 0.3387,
                "price_low": 0.3384,
                "price_close": 0.3385,
                "volume_traded": 28615.34,
                "trades_count": 42,
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call the method
        result = self.client.get_ohlcv_data()

        # Assert the result
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["price_open"], 0.3384)
        self.assertEqual(result[0]["price_close"], 0.3385)

        # Assert the correct URL and parameters were used
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        self.assertIn("/ohlcv/BITSTAMP_SPOT_XRP_USD/latest", call_args[0][0])
        self.assertEqual(call_args[1]["params"]["period_id"], "15MIN")
        self.assertEqual(call_args[1]["params"]["limit"], 1)

    @patch("src.data_collection.coinapi_client.requests.get")
    def test_get_historical_ohlcv_data(self, mock_get):
        """
            Test the get_historical_ohlcv_data method of CoinAPIClient.

            This test mocks the requests.get function to return a predefined historical OHLCV data response.
            It then calls the get_historical_ohlcv_data method with specific start and end times, and verifies that:
            1. The returned data matches the mocked response.
            2. The API was called with the correct URL, parameters (including time range), and headers.

            Args:
                mock_get: A mocked requests.get function.
        """
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = [{"test": "historical_data"}]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call the method
        start_time = datetime(2023, 1, 1, tzinfo=timezone.utc)
        end_time = datetime(2023, 1, 2, tzinfo=timezone.utc)
        result = self.client.get_historical_ohlcv_data(start_time, end_time)

        # Assert the result
        self.assertEqual(result, [{"test": "historical_data"}])

        # Assert the correct URL and parameters were used
        expected_url = (
            f"{config['api_endpoints']['coinapi']}/ohlcv/BITSTAMP_SPOT_XRP_USD/history"
        )
        expected_params = {
            "period_id": "15MIN",
            "time_start": start_time.isoformat(),
            "time_end": end_time.isoformat(),
            "limit": min(
                config["api_limits"]["coinapi_daily"],
                config["api_limits"]["coinapi_daily"],
            ),
        }
        expected_headers = {"X-CoinAPI-Key": config["api_keys"]["coinapi"]}
        mock_get.assert_called_once_with(
            expected_url, params=expected_params, headers=expected_headers
        )

    @patch("src.data_collection.coinapi_client.requests.get")
    def test_get_ohlcv_data_error(self, mock_get):
        """
            Test the error handling of the get_ohlcv_data method.

            This test mocks the requests.get function to raise an exception.
            It then calls the get_ohlcv_data method and verifies that:
            1. The method raises an exception when the API call fails.

            Args:
                mock_get: A mocked requests.get function set to raise an exception.
        """
        # Mock the response to raise an exception
        mock_get.side_effect = Exception("API Error")

        # Assert that the method raises an exception
        with self.assertRaises(Exception):
            self.client.get_ohlcv_data()


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from src.data_collection.coinapi_client import CoinAPIClient
from src.utils.config import config

class TestCoinAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = CoinAPIClient()

    @patch('src.data_collection.coinapi_client.requests.get')
    def test_get_ohlcv_data(self, mock_get):
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = [{"test": "data"}]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call the method
        result = self.client.get_ohlcv_data()

        # Assert the result
        self.assertEqual(result, [{"test": "data"}])

        # Assert the correct URL and parameters were used
        expected_url = f"{config['api_endpoints']['coinapi']}/ohlcv/BITSTAMP_SPOT_XRP_USD/latest"
        expected_params = {"period_id": "15MIN", "limit": 1}
        expected_headers = {"X-CoinAPI-Key": config['api_keys']['coinapi']}
        mock_get.assert_called_once_with(expected_url, params=expected_params, headers=expected_headers)

    @patch('src.data_collection.coinapi_client.requests.get')
    def test_get_historical_ohlcv_data(self, mock_get):
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
        expected_url = f"{config['api_endpoints']['coinapi']}/ohlcv/BITSTAMP_SPOT_XRP_USD/history"
        expected_params = {
            "period_id": "15MIN",
            "time_start": start_time.isoformat(),
            "time_end": end_time.isoformat(),
            "limit": min(config['api_limits']['coinapi_daily'], config['api_limits']['coinapi_daily'])
        }
        expected_headers = {"X-CoinAPI-Key": config['api_keys']['coinapi']}
        mock_get.assert_called_once_with(expected_url, params=expected_params, headers=expected_headers)

    @patch('src.data_collection.coinapi_client.requests.get')
    def test_get_ohlcv_data_error(self, mock_get):
        # Mock the response to raise an exception
        mock_get.side_effect = Exception("API Error")

        # Assert that the method raises an exception
        with self.assertRaises(Exception):
            self.client.get_ohlcv_data()


if __name__ == '__main__':
    unittest.main()

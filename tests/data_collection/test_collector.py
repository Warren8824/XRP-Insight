import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from src.data_collection.collector import (
    collect_and_store_market_data,
    collect_and_store_ohlcv_data,
    collect_historical_data,
    run_data_collection,
)


class TestCollector(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()

    @patch("src.data_collection.collector.CoinGeckoClient")
    def test_collect_and_store_market_data(self, mock_coingecko):
        # Mock the CoinGeckoClient
        mock_coingecko_instance = mock_coingecko.return_value
        mock_coingecko_instance.get_xrp_data.return_value = {
            "last_updated": "2023-07-01T12:00:00Z",
            "market_data": {
                "current_price": {"usd": 1.0},
                "market_cap": {"usd": 1000000},
                "total_volume": {"usd": 500000},
                "circulating_supply": 50000,
                "total_supply": 100000,
                "max_supply": 100000000,
            },
        }

        # Call the function
        collect_and_store_market_data(self.mock_db)

        # Assert that the database session methods were called
        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()

    @patch("src.data_collection.collector.CoinAPIClient")
    def test_collect_and_store_ohlcv_data(self, mock_coinapi):
        # Mock the CoinAPIClient
        mock_coinapi_instance = mock_coinapi.return_value
        mock_coinapi_instance.get_ohlcv_data.return_value = [
            {
                "time_period_start": "2023-01-01T00:00:00Z",
                "price_open": 1.0,
                "price_high": 1.1,
                "price_low": 0.9,
                "price_close": 1.05,
                "volume_traded": 1000000,
            }
        ]

        # Call the function
        collect_and_store_ohlcv_data(self.mock_db)

        # Assert that the database session methods were called
        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()

    @patch("src.data_collection.collector.CoinAPIClient")
    def test_collect_historical_data(self, mock_coinapi):
        # Mock the CoinAPIClient
        mock_coinapi_instance = mock_coinapi.return_value
        mock_data = [
            {
                "time_period_start": f"2023-01-01T{hour:02d}:{minute:02d}:00Z",
                "price_open": 1.0,
                "price_high": 1.1,
                "price_low": 0.9,
                "price_close": 1.05,
                "volume_traded": 1000000,
            }
            for hour in range(24)
            for minute in range(0, 60, 15)
        ]
        mock_coinapi_instance.get_historical_ohlcv_data.return_value = mock_data[
            :95
        ]  # Return only 95 data points

        # Call the function
        start_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        end_date = datetime(2023, 1, 2, tzinfo=timezone.utc)
        collect_historical_data(self.mock_db, start_date, end_date)

        # Assert that the database session methods were called
        self.assertEqual(self.mock_db.add.call_count, 95)  # Expect 95 calls
        self.mock_db.commit.assert_called_once()

    @patch("src.data_collection.collector.collect_and_store_market_data")
    @patch("src.data_collection.collector.collect_and_store_ohlcv_data")
    def test_run_data_collection(self, mock_collect_ohlcv, mock_collect_market):
        # Call the function
        run_data_collection(self.mock_db)

        # Assert that both collection functions were called
        mock_collect_market.assert_called_once_with(self.mock_db)
        mock_collect_ohlcv.assert_called_once_with(self.mock_db)


if __name__ == "__main__":
    unittest.main()

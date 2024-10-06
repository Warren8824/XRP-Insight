import unittest
from unittest.mock import patch, mock_open
import os
from src.utils.config import load_config


class TestConfig(unittest.TestCase):
    """
    A test suite for the config module.

    This class contains unit tests for the configuration loading function
    in the config module, testing various scenarios including successful
    loading, file not found, and invalid YAML.
    """

    @patch(
        "src.utils.config.open",
        new_callable=mock_open,
        read_data=(
            "data_collection:\n"
            "  interval_minutes: 30\n"
            "api_limits:\n"
            "  coinapi_daily: 100\n"
        ),
    )
    @patch.dict(
        os.environ,
        {
            "COINGECKO_API_KEY": "fake_coingecko_key",
            "COINAPI_API_KEY": "fake_coinapi_key",
            "TWITTER_CONSUMER_KEY": "fake_twitter_consumer_key",
            "TWITTER_CONSUMER_SECRET": "fake_twitter_consumer_secret",
            "TWITTER_ACCESS_TOKEN": "fake_twitter_access_token",
            "TWITTER_ACCESS_TOKEN_SECRET": "fake_twitter_access_token_secret",
            "OPENAI_API_KEY": "fake_openai_key",
            "DATABASE_URL": "postgresql://user:pass@localhost:5432/testdb",
        },
    )
    def test_load_config(self, mock_file):
        """
        Test the load_config function with valid input.

        This test verifies that:
        1. The YAML configuration is correctly loaded.
        2. Environment variables are properly merged into the configuration.
        3. API keys are correctly set from environment variables.
        4. The database URL is correctly parsed and added to the configuration.
        5. Derived values (like interval_seconds) are correctly calculated.

        Args:
            mock_file (MagicMock): Mock for the open function to simulate reading a config file.
        """
        config = load_config()

        # Test YAML loading
        self.assertEqual(config["data_collection"]["interval_minutes"], 30)
        self.assertEqual(config["data_collection"]["interval_seconds"], 1800)

        # Test coinapi_daily limit loading
        self.assertEqual(config["api_limits"]["coinapi_daily"], 100)

        # Test API key loading
        self.assertEqual(config["api_keys"]["coingecko"], "fake_coingecko_key")
        self.assertEqual(config["api_keys"]["coinapi"], "fake_coinapi_key")
        self.assertEqual(
            config["api_keys"]["twitter"]["consumer_key"], "fake_twitter_consumer_key"
        )
        self.assertEqual(
            config["api_keys"]["twitter"]["consumer_secret"],
            "fake_twitter_consumer_secret",
        )
        self.assertEqual(
            config["api_keys"]["twitter"]["access_token"], "fake_twitter_access_token"
        )
        self.assertEqual(
            config["api_keys"]["twitter"]["access_token_secret"],
            "fake_twitter_access_token_secret",
        )
        self.assertEqual(config["api_keys"]["openai"], "fake_openai_key")

        # Test database URL parsing
        self.assertEqual(
            config["database"]["url"], "postgresql://user:pass@localhost:5432/testdb"
        )
        self.assertEqual(config["database"]["host"], "localhost")
        self.assertEqual(config["database"]["port"], 5432)
        self.assertEqual(config["database"]["user"], "user")
        self.assertEqual(config["database"]["password"], "pass")
        self.assertEqual(config["database"]["dbname"], "testdb")

    @patch("src.utils.config.open", side_effect=FileNotFoundError)
    def test_load_config_file_not_found(self, mock_file):
        """
        Test the load_config function when the config file is not found.

        This test verifies that:
        1. When the configuration file is not found, an empty dictionary is returned.
        2. The function handles the FileNotFoundError gracefully.

        Args:
            mock_file (MagicMock): Mock for the open function to simulate a missing config file.
        """
        config = load_config()
        self.assertEqual(config, {})

    @patch(
        "src.utils.config.open",
        new_callable=mock_open,
        read_data="invalid: yaml: content:",
    )
    def test_load_config_invalid_yaml(self, mock_file):
        """
        Test the load_config function with invalid YAML content.

        This test verifies that:
        1. When the YAML content is invalid, an empty dictionary is returned.
        2. The function handles the YAMLError gracefully.

        Args:
            mock_file (MagicMock): Mock for the open function to simulate a file with invalid YAML content.
        """
        config = load_config()
        self.assertEqual(config, {})


if __name__ == "__main__":
    unittest.main()

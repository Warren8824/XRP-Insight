import unittest
import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from sqlalchemy import inspect
from src.models.base import engine
from src.utils.config import config

class TestSetup(unittest.TestCase):
    def test_database(self):
        inspector = inspect(engine)
        self.assertIn('market_data', inspector.get_table_names(), "market_data table does not exist in the database")

    def test_config(self):
        self.assertIn('database', config, "Database configuration is missing")
        self.assertIn('name', config['database'], "Database name is missing from configuration")
        self.assertIn('path', config['database'], "Database path is missing from configuration")
        self.assertIn('data_collection', config, "Data collection configuration is missing")
        self.assertIn('interval_minutes', config['data_collection'], "Data collection interval is missing from configuration")
        self.assertIn('api_endpoints', config, "API endpoints configuration is missing")
        self.assertIn('coingecko', config['api_endpoints'], "CoinGecko API endpoint is missing from configuration")

    def test_api_keys(self):
        self.assertIn('api_keys', config, "API keys configuration is missing")
        for key in ['coingecko', 'twitter', 'openai']:
            self.assertIn(key, config['api_keys'], f"{key.capitalize()} API key is missing from configuration")

    def test_print_config(self):
        print("\nConfiguration variables:")
        print(f"Database Name: {config['database']['name']}")
        print(f"Database Path: {config['database']['path']}")
        print(f"Data Collection Interval: {config['data_collection']['interval_minutes']} minutes")
        print(f"CoinGecko API Endpoint: {config['api_endpoints']['coingecko']}")

        for key, value in config['api_keys'].items():
            if isinstance(value, dict):
                print(f"\n{key.capitalize()} API Keys:")
                for subkey, subvalue in value.items():
                    print(f"  {subkey}: {'*' * 16 + subvalue[-4:] if subvalue else 'Not set'}")
            else:
                print(f"\n{key.capitalize()} API Key: {'*' * 16 + value[-4:] if value else 'Not set'}")

        #self.assertTrue(True)  # This ensures the test always passes after printing


if __name__ == '__main__':
    unittest.main()
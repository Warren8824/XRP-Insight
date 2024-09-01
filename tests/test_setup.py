import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from sqlalchemy import inspect
from src.models.base import engine
from src.utils.config import config
from src.models.market_data import MarketData


def test_database():
    inspector = inspect(engine)

    # Check if the market_data table exists
    if 'market_data' in inspector.get_table_names():
        print("✅ market_data table exists in the database.")
    else:
        print("❌ market_data table does not exist in the database.")


def print_config():
    print("\nConfiguration variables:")
    print(f"Database Name: {config['database']['name']}")
    print(f"Database Path: {config['database']['path']}")
    print(f"Data Collection Interval: {config['data_collection']['interval_minutes']} minutes")
    print(f"CoinGecko API Endpoint: {config['api_endpoints']['coingecko']}")
    print(f"XRPL API Endpoint: {config['api_endpoints']['xrpl']}")

    # Print API keys (partially masked for security)
    for key, value in config['api_keys'].items():
        if isinstance(value, dict):
            print(f"\n{key.capitalize()} API Keys:")
            for subkey, subvalue in value.items():
                print(f"  {subkey}: {'*' * 16 + subvalue[-4:] if subvalue else 'Not set'}")
        else:
            print(f"\n{key.capitalize()} API Key: {'*' * 16 + value[-4:] if value else 'Not set'}")


def main():
    print("Testing database and configuration setup...\n")

    # Test database
    try:
        test_database()
    except Exception as e:
        print(f"❌ Error connecting to the database: {e}")

    # Print configuration
    try:
        print_config()
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")


if __name__ == "__main__":
    main()
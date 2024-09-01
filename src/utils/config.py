import os
import yaml
from dotenv import load_dotenv
from src.constants import DEFAULT_DATABASE_NAME

load_dotenv()  # Load environment variables from .env file


def load_config():
    with open("config/configuration.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    # Merge with defaults and environment variables.
    config['api_keys'] = {
        'coingecko': os.getenv('COINGECKO_API_KEY'),
        'twitter': {
            'consumer_key': os.getenv('TWITTER_CONSUMER_KEY'),
            'consumer_secret': os.getenv('TWITTER_CONSUMER_SECRET'),
            'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
            'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
        },
        'openai': os.getenv('OPENAI_API_KEY'),
    }
    # Use defaults if not specified in configuration.yaml
    config['data_collection']['interval_seconds'] = config['data_collection'].get('interval_minutes', 15) * 60
    config['database']['name'] = config['database'].get('name', DEFAULT_DATABASE_NAME)

    return config


config = load_config()

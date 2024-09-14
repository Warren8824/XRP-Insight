import yaml
from dotenv import load_dotenv

import os

load_dotenv()  # Load environment variables from .env file


def load_config():
    config = {}
    try:
        # Load YAML configuration
        with open("config/config.yaml", "r") as config_file:
            config = yaml.safe_load(config_file)
        utils_logger.info("Loaded configuration from YAML file.")

        # Merge with environment variables
        config['api_keys'] = {
            'coingecko': os.getenv('COINGECKO_API_KEY'),
            'coinapi': os.getenv('COINAPI_API_KEY'),
            'twitter': {
                'consumer_key': os.getenv('TWITTER_CONSUMER_KEY'),
                'consumer_secret': os.getenv('TWITTER_CONSUMER_SECRET'),
                'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
                'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
            },
            'openai': os.getenv('OPENAI_API_KEY'),
        }
        utils_logger.info("Merged API keys with environment variables.")

        # Update configuration with environment variables
        config['data_collection']['interval_seconds'] = config['data_collection'].get('interval_minutes', 15) * 60
        config['database']['url'] = os.getenv('DATABASE_URL')  # Postgres credentials

        # Log the final configuration if necessary (be careful with sensitive data)
        utils_logger.debug(f"Final configuration: {config}")

    except FileNotFoundError as e:
        utils_logger.error(f"Configuration file not found: {e}")
    except yaml.YAMLError as e:
        utils_logger.error(f"Error loading YAML configuration: {e}")
    except Exception as e:
        utils_logger.error(f"Unexpected error while loading configuration: {e}")

    return config


config = load_config()

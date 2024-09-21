import yaml
from dotenv import load_dotenv
import os
from urllib.parse import urlparse
from src.utils.logger import utils_logger

load_dotenv()  # Load environment variables from .env file


def load_config():
    config = {}
    try:
        # Load YAML configuration
        with open("config/config.yml", "r") as config_file:
            config = yaml.safe_load(config_file)
        utils_logger.info("Loaded configuration from YAML file.")

        # Merge with environment variables
        config["api_keys"] = {
            "coingecko": os.getenv("COINGECKO_API_KEY"),
            "coinapi": os.getenv("COINAPI_API_KEY"),
            "twitter": {
                "consumer_key": os.getenv("TWITTER_CONSUMER_KEY"),
                "consumer_secret": os.getenv("TWITTER_CONSUMER_SECRET"),
                "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
                "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
            },
            "openai": os.getenv("OPENAI_API_KEY"),
        }
        utils_logger.info("Merged API keys with environment variables.")

        # Update configuration with environment variables
        config["data_collection"]["interval_seconds"] = (
            config["data_collection"].get("interval_minutes", 15) * 60
        )

        # Parse DATABASE_URL
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            parsed_url = urlparse(db_url)
            config["database"] = {
                "url": db_url,
                "host": parsed_url.hostname,
                "port": parsed_url.port,
                "user": parsed_url.username,
                "password": parsed_url.password,
                "dbname": parsed_url.path[1:],  # Remove leading '/'
            }
        else:
            utils_logger.error("DATABASE_URL not found in environment variables.")

        # Log the final configuration if necessary (be careful with sensitive data)
        # utils_logger.debug(f"Final configuration: {config}")

    except FileNotFoundError as e:
        utils_logger.error(f"Configuration file not found: {e}")
    except yaml.YAMLError as e:
        utils_logger.error(f"Error loading YAML configuration: {e}")
    except Exception as e:
        utils_logger.error(f"Unexpected error while loading configuration: {e}")

    return config


config = load_config()

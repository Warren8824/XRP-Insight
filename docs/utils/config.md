# Configuration System Documentation

## Overview

This document outlines the configuration system implemented in the XRP Market Bot project. The configuration system combines settings from a YAML file and environment variables to provide a flexible and secure way to manage application settings.

## Components

1. **YAML Configuration File**: `config/config.yaml`
2. **Environment Variables**: Stored in `.env` file
3. **Python Configuration Module**: `config.py`

## Configuration File (config.yaml)

The `config/config.yaml` file contains the following sections:

```yaml
database:
    name: xrp_market_bot.db
    path: database/

data_collection:
    interval_minutes: 15

twitter_bot:
    post_interval_hours: 1
    max_tweets_per_days: 24

logging:
    level: INFO
    file: logs/xrp_market_bot.log

api_endpoints:
    coingecko: https://api.coingecko.com/api/v3
    xrpl: wss://xrplcluster.com
```

## Environment Variables (.env)

The following environment variables should be set in the `.env` file:

```
COINGECKO_API_KEY=your_coingecko_api_key
TWITTER_CONSUMER_KEY=your_twitter_consumer_key
TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
OPENAI_API_KEY=your_openai_api_key
APP_ENV=development
```

Note: Replace `your_*_key` and `your_*_secret` with actual API keys and secrets. Never commit the `.env` file to version control.

## Configuration Loading Process

The `load_config()` function in `config.py` performs the following steps:

1. Loads environment variables from the `.env` file
2. Reads the `config/config.yaml` file
3. Merges the YAML configuration with environment variables
4. Applies default values for certain settings

## Usage

To use the configuration in your code:

```python
from utils.config import config

database_name = config['database']['name']
coingecko_api_endpoint = config['api_endpoints']['coingecko']
```

## Configuration Structure

The loaded configuration has the following structure:

```python
config = {
    'api_keys': {
        'coingecko': '...',
        'twitter': {
            'consumer_key': '...',
            'consumer_secret': '...',
            'access_token': '...',
            'access_token_secret': '...',
        },
        'openai': '...',
    },
    'data_collection': {
        'interval_minutes': 15,
        'interval_seconds': 900,
    },
    'database': {
        'name': 'xrp_market_bot.db',
        'path': 'database/',
    },
    'twitter_bot': {
        'post_interval_hours': 1,
        'max_tweets_per_days': 24,
    },
    'logging': {
        'level': 'INFO',
        'file': 'logs/xrp_market_bot.log',
    },
    'api_endpoints': {
        'coingecko': 'https://api.coingecko.com/api/v3',
        'xrpl': 'wss://xrplcluster.com',
    },
}
```

## Best Practices

1. Always use the `config` object imported from `utils.config` to access configuration values in your code.
2. Keep sensitive information (like API keys) in the `.env` file and never commit it to version control.
3. Use the `config.yaml` file for configuration values that may change between environments but are not sensitive.
4. When adding new configuration options, update both the `config.yaml` file and the `load_config()` function in `config.py`.
5. Use the `APP_ENV` environment variable to set the current environment (development, staging, or production).

## Customization

To modify the configuration system:

1. Add new sections to the `config.yaml` file as needed.
2. Update the `load_config()` function in `config.py` to handle new configuration options or environment variables.
3. If adding new default values, consider adding them to `src/constants.py` and referencing them in `config.py`.

---

For any questions or issues regarding the configuration system, please contact the project maintainer.
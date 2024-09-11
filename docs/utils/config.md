# Configuration Utility

The configuration utility manages the application's configuration, combining settings from a YAML file and environment variables.

## Key Features

- Loads configuration from a YAML file (`config/config.yml`)
- Incorporates sensitive information from environment variables
- Provides a centralized configuration object

## Usage

To use the configuration in your code:

```python
from src.utils.config import config

database_url = config['database']['url']
coinapi_key = config['api_keys']['coinapi']
```

Configuration Structure
The configuration object includes:

*API keys for various services (CoinGecko, CoinAPI, Twitter, OpenAI)
*Database connection URL
*Data collection interval
*Other application-specific settings

Environment Variables
The following environment variables are used:

*COINGECKO_API_KEY
*COINAPI_API_KEY
*TWITTER_CONSUMER_KEY
*TWITTER_CONSUMER_SECRET
*TWITTER_ACCESS_TOKEN
*TWITTER_ACCESS_TOKEN_SECRET
*OPENAI_API_KEY
*DATABASE_URL
*APP_ENV

Ensure these are set in your `.env` file or in your environment.
Customization
To add new configuration options, modify the `load_config` function in `src/utils/config.py` and update the `config/config.yml` file as needed.
# config.py

This file is responsible for loading and managing the configuration settings for the XRP Insight project.

## Functions

### load_config()

This function loads the configuration from a YAML file and environment variables.

#### Process:
1. Loads the YAML configuration from `config/config.yml`.
2. Merges API keys from environment variables.
3. Calculates the data collection interval in seconds.
4. Parses the DATABASE_URL environment variable.

#### Returns:
A dictionary containing the full configuration.

## Key Components

- Uses `yaml` for parsing the YAML configuration file.
- Uses `dotenv` to load environment variables from a `.env` file.
- Parses the `DATABASE_URL` to extract database connection details.
- Logs configuration loading process and any errors.

## Configuration Structure

The final configuration dictionary includes:
- API keys for various services (CoinGecko, CoinAPI, Twitter, OpenAI)
- Database connection details
- Data collection settings

## Usage

```python
from src.utils.config import config

# Access configuration values
coingecko_api_key = config['api_keys']['coingecko']
db_host = config['database']['host']
```

## Notes

- Ensure that the config/config.yml file exists and is properly formatted.
- Set up a .env file with necessary environment variables (API keys, DATABASE_URL, etc.).
- Be cautious about logging sensitive information (API keys, database credentials).
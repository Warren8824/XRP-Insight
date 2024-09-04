# XRP Market Bot

XRP Market Bot is a Python-based project that collects, analyzes, and reports on XRP market data. It uses various APIs to gather information, stores it in a SQLite database, and provides insights through data analysis and a Twitter bot.

## Project Structure

```
xrp_market_bot/
├── .github/
│   └── workflows/
│       └── ci.yaml
├── config/
│   └── config.yaml
├── database/
│   └──  xrp_market_bot.db
├── docs/
│   └── ai_analysis
│   └── analysis
│   └── api
│   └── data_collection
│   └── models
│   └── tweet_generation
│   └── utils
        └── config.md
│       └── logger.md
├── logs/
├── scripts/
│   └── init_db.py
├── src/
│   ├── analysis/
│   │   └── __init__.py
│   ├── data_collection/
│   │   └── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── market_data.py
│   ├── tweet_generation/
│   │   └── __init__.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logger.py
│   ├── app.py
│   └── constants.py
├── tests/
│   ├── analysis/
│   │   └── __init__.py
│   ├── data_collection/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   ├── tweet_generation/
│   │   └── __init__.py
│   ├── utils/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── __main__.py
│   └── test_setup.py
├── .env
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/Warren8824/xrp_market_bot.git
   cd xrp_market_bot
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your API keys:
   ```
   COINGECKO_API_KEY=your_coingecko_api_key
   TWITTER_CONSUMER_KEY=your_twitter_consumer_key
   TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret
   TWITTER_ACCESS_TOKEN=your_twitter_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
   OPENAI_API_KEY=your_openai_api_key
   
   APP_ENV=development # Set this to development/staging/production.
   ```

5. Update the `config/config.yaml` file with your desired configuration:
   ```yaml
   database:
     name: xrp_market_bot.db
     path: database/
   
   data_collection:
     interval_minutes: 15
   
   twitter_bot:
     post_interval_hours: 1
     max_tweets_per_day: 24
   
   logging:
     level: INFO
     file: logs/xrp_market_bot.log
   
   api_endpoints:
     coingecko: https://api.coingecko.com/api/v3
     xrpl: wss://xrplcluster.com
   ```

6. Initialize the database:
   ```
   python scripts/init_db.py
   ```

## Running Tests

To run the tests, use the following command from the project root directory:

```
python -m tests
```

This will discover and run all tests in the `tests` directory and its subdirectories.

## Configuration

This project uses a flexible configuration system that combines settings from a YAML file (`config/config.yaml`) and environment variables (`.env`). The configuration system provides:

- Centralized management of application settings
- Environment-specific configurations
- Secure handling of API keys and sensitive information

Key components:
- `config/config.yaml`: Contains general settings for database, data collection, Twitter bot, logging, and API endpoints.
- `.env`: Stores sensitive information like API keys and environment setting.
- `utils/config.py`: Loads and merges configuration from both sources.

To use the configuration in your code:

```python
from utils.config import config

database_name = config['database']['name']
coingecko_api_endpoint = config['api_endpoints']['coingecko']
```

For detailed information about the configuration system, including setup instructions and best practices, please refer to the [configuration documentation](docs/utils/config.md).

## Constants

The project uses a set of predefined constants to maintain consistency across different modules. These constants include:

- Internal constants: Such as the Coingecko ID for XRP, maximum tweet length, and maximum tokens for AI responses.
- Default values: Like the default database name, which can be overridden in the configuration file.

To use these constants in your code:

```python
from src.constants import XRP_ID, MAX_TWEET_LENGTH

# Example usage
def fetch_xrp_data():
    return coingecko_api.get_coin_data(XRP_ID)
```

For a complete list of constants and their usage, please refer to the [constants documentation](docs/constants.md).

## Continuous Integration

This project uses GitHub Actions for continuous integration. The workflow is defined in `.github/workflows/ci.yaml`. It automatically runs tests and checks code quality on every push and pull request.

## Usage

(Note: Add usage instructions here once the main application features are implemented)

## Logging

This project uses a comprehensive logging system that provides environment-specific logging configurations and separate loggers for each module. For detailed information about the logging system, including usage instructions and best practices, please refer to the [logger documentation](docs/utils/logger.md).

Key features of the logging system:
- Environment-specific configurations (development, staging, production)
- Separate loggers for each module
- Rotating file handlers to manage log file sizes
- Console output with environment-specific log levels

To use a logger in your code:

```python
from utils.logger import data_collection_logger

data_collection_logger.info("Starting data collection process")
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Warren Bebbington - [@your_twitter](https://twitter.com/your_twitter) - warrenbebbington88@gmail.com

Project Link: [https://github.com/Warren8824/xrp_market_bot](https://github.com/Warren8824/xrp_market_bot)
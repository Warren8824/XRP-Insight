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
├── docs/
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

## Continuous Integration

This project uses GitHub Actions for continuous integration. The workflow is defined in `.github/workflows/ci.yaml`. It automatically runs tests and checks code quality on every push and pull request.

## Usage

(Note: Add usage instructions here once the main application features are implemented)

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
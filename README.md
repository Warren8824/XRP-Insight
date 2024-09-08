# XRP Insight

XRP Insight is an advanced real-time analysis and AI-driven content generation system for the XRP cryptocurrency market. It collects data from various APIs, processes and analyzes this data using TimescaleDB, and generates insightful content using AI. This project aims to provide cryptocurrency enthusiasts, traders, and researchers with valuable, data-driven insights about XRP.

## Project Structure

xrp_insight/
├── .github/
│   └── workflows/
│       └── ci.yaml
├── config/
│   └── config.yaml
├── docs/
│   ├── whitepaper.md
│   ├── appendix_a_technical_specifications.md
│   ├── appendix_b_database_schema.md
│   ├── appendix_c_api_integration.md
│   └── yellow_paper.md
├── logs/
├── scripts/
│   ├── init_db.py
│   └── data_backfill.py
├── src/
│   ├── data_collection/
│   │   ├── init.py
│   │   ├── coingecko_client.py
│   │   ├── coinapi_client.py
│   │   └── collector.py
│   ├── data_processing/
│   │   ├── init.py
│   │   ├── cleaning.py
│   │   └── aggregation.py
│   ├── analysis/
│   │   ├── init.py
│   │   ├── indicators.py
│   │   └── trends.py
│   ├── models/
│   │   ├── init.py
│   │   ├── base.py
│   │   ├── market_data.py
│   │   ├── ohlcv_data.py
│   │   └── technical_indicators.py
│   ├── ai_integration/
│   │   ├── init.py
│   │   └── gpt_client.py
│   ├── content_generation/
│   │   ├── init.py
│   │   ├── templates.py
│   │   └── generator.py
│   ├── utils/
│   │   ├── init.py
│   │   ├── config.py
│   │   └── logger.py
│   ├── app.py
│   └── constants.py
├── tests/
│   ├── data_collection/
│   │   └── test_collectors.py
│   ├── data_processing/
│   │   ├── test_cleaning.py
│   │   └── test_aggregation.py
│   ├── analysis/
│   │   └── test_indicators.py
│   ├── models/
│   │   └── test_models.py
│   ├── ai_integration/
│   │   └── test_gpt_client.py
│   ├── content_generation/
│   │   └── test_generator.py
│   ├── utils/
│   │   ├── test_config.py
│   │   └── test_logger.py
│   ├── init.py
│   └── conftest.py
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
└── requirements.txt

## Setup

1. Clone the repository: git clone https://github.com/Warren8824/xrp_insight.git
cd xrp_insight

2. Create a virtual environment and activate it: python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

3. Install the required packages: pip install -r requirements.txt

4. Set up TimescaleDB:
- Install TimescaleDB on your system or use the provided Docker configuration.
- Create a database for the project.

5. Create a `.env` file in the project root and add your API keys and database connection string: COINGECKO_API_KEY=your_coingecko_api_key
COINAPI_API_KEY=your_coinapi_api_key
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://username:password@localhost:5432/xrp_insight
APP_ENV=development # Set this to development/staging/production

6. Update the `config/config.yaml` file with your desired configuration:
```yaml
database:
  url: ${DATABASE_URL}

data_collection:
  interval_minutes: 15

content_generation:
  interval_hours: 4
  max_posts_per_day: 6

logging:
  level: INFO
  file: logs/xrp_insight.log

api_endpoints:
  coingecko: https://api.coingecko.com/api/v3
  coinapi: https://rest.coinapi.io/v1
```

7. Initialize the database: python scripts/init_db.py

8. (Optional) Run the data backfill script to populate historical data: python scripts/data_backfill.py

## Running the Application

To start the XRP Insight application:
Copypython src/app.py

## Running Tests

To run the tests, use the following command from the project root directory:
Copypython -m pytest

This will discover and run all tests in the tests directory and its subdirectories.

## Configuration


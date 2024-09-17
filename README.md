# XRP Insight

XRP Insight is an advanced real-time analysis and AI-driven content generation system for the XRP cryptocurrency market. It collects data from various APIs, processes and analyzes this data using TimescaleDB, and generates insightful content using AI. This project aims to provide cryptocurrency enthusiasts, traders, and researchers with valuable, data-driven insights about XRP.

## Project Structure
```
xrp_insight/
├── .github/
│   └── workflows/
│       └── ci.yaml
├── config/
│   └── config.yaml
├── docs/
│   ├── __init__.py
│   ├── data_collection/
│   │   └── __init__.py
│   ├── data_processing/
│   │   └── __init__.py
│   ├── analysis/
│   │   └── __init__.py
│   ├── ai_integration/
│   │   └── __init__.py
│   ├── content_generation/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   ├── utils/
│   │   └── __init__.py
│   ├── api/
│   │   └── __init__.py
│   └── scheduler/
│       └── __init__.py
├── logs/
├── scripts/
│   ├── init_db.py
│   └── backfill_historical_data.py
├── src/
│   ├── __init__.py
│   ├── data_collection/
│   │   ├── __init__.py
│   │   ├── coingecko_client.py
│   │   ├── coinapi_client.py
│   │   └── collector.py
│   ├── data_processing/
│   │   ├── __init__.py
│   │   └── indicators.py
│   ├── analysis/
│   │   └── __init__.py
│   ├── ai_integration/
│   │   └── __init__.py
│   ├── content_generation/
│   │   └── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── market_data_15_min.py
│   │   ├── ohlcv_data_15_min.py
│   │   └── technical_indicators_15_min.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logger.py
│   ├── api/
│   │   └── __init__.py
│   ├── scheduler/
│   │   ├── __init__.py
│   │   └── tasks.py
│   ├── app.py
│   └── constants.py
├── tests/
│   ├── __init__.py
│   ├── __main__.py
│   ├── data_collection/
│   │   └── __init__.py
│   ├── data_processing/
│   │   └── __init__.py
│   ├── analysis/
│   │   └── __init__.py
│   ├── ai_integration/
│   │   └── __init__.py
│   ├── content_generation/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   ├── utils/
│   │   └── __init__.py
│   ├── api/
│   │   └── __init__.py
│   └── scheduler/
│       └── __init__.py
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
└── requirements.txt
```
## Setup

1. Clone the repository: 
`git clone https://github.com/Warren8824/xrp_insight.git`
`cd xrp_insight`

2. Create a virtual environment and activate it: `python -m venv venv`
`source venv/bin/activate`  # On Windows, use `venv\Scripts\activate`

3. Install the required packages: `pip install -r requirements.txt`

4. Create a `.env` file in the project root and add your API keys and database connection string: 
```
COINGECKO_API_KEY=your_coingecko_api_key
COINAPI_API_KEY=your_coinapi_api_key
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://username:password@localhost:5432/xrp_insight
APP_ENV=development # Set this to development/staging/production
```
5. Update the `config/config.yaml` file with your desired configuration:

```yaml
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
6. Initialize the database: `python scripts/init_db.py`

7. (Optional) Run the data backfill script to populate historical data: `python scripts/data_backfill.py`

## Running the Application

To start the XRP Insight application:
`python src/app.py`

## Running Tests

To run the tests, use the following command from the project root directory:
`python -m pytest`

This will discover and run all tests in the tests directory and its subdirectories.

## Configuration

This project uses a flexible configuration system that combines settings from a YAML file (`config/config.yaml`) and environment variables (`.env`). The configuration system provides:

- Centralized management of application settings
- Environment-specific configurations
- Secure handling of API keys and sensitive information

Key components:
- `config/config.yaml`: Contains general settings for database, data collection, content generation, logging, and API endpoints.
- `.env`: Stores sensitive information like API keys and environment setting.
- `src/utils/config.py`: Loads and merges configuration from both sources.

To use the configuration in your code:

```python
from utils.config import config

database_url = config['database']['url']
coingecko_api_endpoint = config['api_endpoints']['coingecko']
```
For detailed information about the configuration system, including setup instructions and best practices, please refer to the configuration documentation.
## Constants

The project uses a set of predefined constants to maintain consistency across different modules. These constants include:

Internal constants: Such as the Coingecko ID for XRP, maximum content length, and maximum tokens for AI responses.
Default values: Like the default database name, which can be overridden in the configuration file.

To use these constants in your code:

```
from src.constants import XRP_ID, MAX_CONTENT_LENGTH

# Example usage
def fetch_xrp_data():
    return coingecko_client.get_coin_data(XRP_ID)
```
For a complete list of constants and their usage, please refer to the constants documentation.
## Database Models

XRP Insight uses TimescaleDB (a PostgreSQL extension) for efficient time-series data management. The base configuration for all database models is defined in src/models/base.py.

Key features:

TimescaleDB for time-series data management
SQLAlchemy ORM for database interactions
Hypertables for optimized time-series queries
Continuous aggregates for efficient data summarization

To define a new model: 
```
from src.models.base import Base
from sqlalchemy import Column, Integer, String

class YourModel(Base):
    __tablename__ = "your_table_name"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # Add more columns as needed
```

The database is initialized using the scripts/init_db.py script (see Setup instructions). When adding new models, make sure they are imported in this script to ensure their tables are created.
For detailed information about the database setup, model creation, and initialization process, please refer to the database schema documentation.
## Continuous Integration

This project uses GitHub Actions for continuous integration. The workflow is defined in .github/workflows/ci.yaml. It automatically runs tests and checks code quality on every push and pull request.

## Usage

XRP Insight automatically collects data, performs analysis, and generates content based on the configured intervals. You can monitor the application logs for information about its operations.
For detailed API documentation and usage examples, please refer to the API Integration documentation.
## Logging

This project uses a comprehensive logging system that provides environment-specific logging configurations and separate loggers for each module. For detailed information about the logging system, including usage instructions and best practices, please refer to the logger documentation.
Key features of the logging system:

Environment-specific configurations (development, staging, production)
Separate loggers for each module
Rotating file handlers to manage log file sizes
Console output with environment-specific log levels

To use a logger in your code:

```
from utils.logger import data_collection_logger

data_collection_logger.info("Starting data collection process")
```

## Contributing

1. Fork the repository
2. Create your feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## License

Distributed under the MIT License. See LICENSE for more information.

## Contact

Warren Bebbington - @your_twitter - warrenbebbington88@gmail.com
Project Link: https://github.com/Warren8824/xrp_insight

# Logging Utility

The logging utility provides a flexible and environment-aware logging setup for the XRP Insight project.

## Key Features

- Environment-specific logging configurations (development, staging, production)
- Rotating file handler to manage log file sizes and backups
- Console and file logging with separate log levels for each
- Separate loggers for different modules of the application, making it easy to track and filter logs by module
- Automatic logger setup based on environment variables

## Usage

To use a logger in your code:

```python
from src.utils.logger import data_collection_logger

data_collection_logger.info("Starting data collection process")
data_collection_logger.error("An error occurred: %s", str(error))
```

Loggers are automatically initialized based on the environment (development, staging, or production). Make sure the `.env` file has the appropriate `APP_ENV` variable set.

`APP_ENV=development  # or 'production', 'staging'`

## Available Loggers

* ai_integration_logger
* analysis_logger
* api_logger
* content_generation_logger
* data_collection_logger
* data_processing_logger
* models_logger
* scheduler_logger
* utils_logger 

## Log Levels

The log levels are set based on the environment:

* Production:
    File: INFO
    Console: WARNING
* Staging:
File: DEBUG
Console: INFO
* Development:
File: DEBUG
Console: DEBUG

## Customization

You can customize the logging setup by modifying the `setup_logger` function in `src/utils/logger.py`. You can also add or remove loggers as needed by editing the `configure_loggers` function.
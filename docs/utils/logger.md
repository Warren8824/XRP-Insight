# Logging Utility

The logging utility provides a flexible and environment-aware logging setup for the XRP Insight project.

## Key Features

- Environment-specific logging configurations (development, staging, production)
- Rotating file handler to manage log file sizes
- Console and file logging
- Separate loggers for different modules of the application

## Usage

To use a logger in your code:

```python
from src.utils.logger import data_collection_logger

data_collection_logger.info("Starting data collection process")
data_collection_logger.error("An error occurred: %s", str(error))
```

## Available Loggers

- ai_analysis_logger
- analysis_logger
- api_logger
- data_collection_logger
- models_logger
- tweet_generation_logger
- utils_logger

## Log Levels
The log levels are set based on the environment:

 ```Production```: File - INFO, Console - WARNING

```Staging```: File - DEBUG, Console - INFO

```Development```: File - DEBUG, Console - DEBUG

Customization
You can customize the logging setup by modifying the setup_logger function in ```src/utils/logger.py```.

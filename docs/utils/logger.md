# logger.py

This file sets up the logging system for the XRP Insight project, providing customized loggers for different components of the application.

## Functions

### setup_logger(name, log_directory, file_level, console_level)

Sets up a logger with both file and console handlers.

#### Parameters:
- `name`: Name of the logger
- `log_directory`: Directory to store log files
- `file_level`: Logging level for file output
- `console_level`: Logging level for console output

#### Returns:
Configured logger object

### configure_loggers()

Configures all loggers for the application based on the current environment.

#### Returns:
Dictionary of configured loggers

### get_loggers()

Retrieves or initializes the global logger dictionary.

#### Returns:
Dictionary of configured loggers

## Key Components

- Uses Python's built-in `logging` module.
- Implements rotating file handlers to manage log file sizes.
- Configures different logging levels based on the environment (development, staging, production).
- Creates separate log files for each component of the application.

## Global Logger Objects

The following logger objects are initialized and available globally:
- `ai_integration_logger`
- `analysis_logger`
- `api_logger`
- `content_generation_logger`
- `data_collection_logger`
- `data_processing_logger`
- `models_logger`
- `scheduler_logger`
- `utils_logger`
- `scripts_logger`

## Usage

```python
from src.utils.logger import data_collection_logger

data_collection_logger.info("Starting data collection process")
data_collection_logger.error("An error occurred: %s", error_message)
```

## Notes

- Log files are stored in the logs directory.
- Log file names include the environment (e.g., data_collection_development.log).
- Logging levels are adjusted based on the APP_ENV environment variable.
- Ensure the logs directory exists or has write permissions.
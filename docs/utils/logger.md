# Logging System Documentation

## Overview

This document outlines the logging system implemented in the XRP Market Bot project. The logging system is designed to provide flexible and environment-specific logging capabilities, with separate loggers for each module of the project. This allows for granular control over logging outputs and makes it easier to trace issues within specific components of the system.

## Features

- Environment-specific logging configurations
- Separate loggers for each module
- Distinct log files for each module
- Separate log levels for file and console outputs
- Rotating file handler to manage log file sizes
- Consistent log formatting across all modules and environments

## Configuration

The logging system uses the following key components:

1. **Environment Variables**: The `APP_ENV` environment variable determines the current environment.
2. **Logging Levels**: Different logging levels are set for file and console outputs based on the environment.
3. **RotatingFileHandler**: Manages log file sizes and maintains a set number of backup files for each module.

### Environment Setup

The system recognizes three environments:

- Development (`APP_ENV=development`)
- Staging (`APP_ENV=staging`)
- Production (`APP_ENV=production`)

If `APP_ENV` is not set, the system defaults to the development environment.

### Logging Levels

Logging levels are configured as follows for each environment:

| Environment | File Logging Level | Console Logging Level |
|-------------|--------------------|-----------------------|
| Development | DEBUG              | DEBUG                 |
| Staging     | DEBUG              | INFO                  |
| Production  | INFO               | WARNING               |

## Module-specific Loggers

The following loggers are set up for different modules of the project:

1. `ai_analysis_logger`
2. `analysis_logger`
3. `api_logger`
4. `data_collection_logger`
5. `models_logger`
6. `tweet_generation_logger`
7. `utils_logger`

Each logger writes to its own log file and the console, allowing for module-specific log management and easier debugging.

## Usage

### Setting Up the Loggers

The loggers are set up using the `setup_logger` function:

```python
logger = setup_logger(
    name='module_name',
    log_directory=log_directory,
    file_level=file_level,
    console_level=console_level
)
```

### Logging Messages

Use the following methods to log messages at different levels:

```python
ai_analysis_logger.debug("This is a debug message")
analysis_logger.info("This is an info message")
api_logger.warning("This is a warning message")
data_collection_logger.error("This is an error message")
utils_logger.critical("This is a critical message")
```

Replace `logger` with the specific logger for the module you're working in (e.g., `ai_analysis_logger`, `api_logger`, etc.).

## Log File Management

- Log files are named `<module_name>_<environment>.log` (e.g., `ai_analysis_production.log`).
- Each log file has a maximum size of 10 MB.
- When a log file reaches the maximum size, it is renamed with a numbered suffix (e.g., `.1`), and a new log file is created.
- A maximum of 5 backup files are maintained for each module's log.

## Logging Behavior by Environment

### Development Environment
- File: Logs all messages (DEBUG and above) for each module
- Console: Logs all messages (DEBUG and above) for each module

### Staging Environment
- File: Logs all messages (DEBUG and above) for each module
- Console: Logs INFO messages and above for each module

### Production Environment
- File: Logs INFO messages and above for each module
- Console: Logs WARNING messages and above for each module

## Implementation Details

### Key Components

1. **RotatingFileHandler**: Manages log file rotation for each module.
2. **StreamHandler**: Handles console output for each module.
3. **Formatter**: Formats log messages consistently across all modules.

### Log Message Format

Log messages are formatted as follows:
```
%(asctime)s %(levelname)s %(message)s
```

Example: `2023-09-04 10:30:15,123 INFO This is an info message`

## Best Practices

1. Use the appropriate logger for each module to keep logs organized.
2. Use appropriate log levels:
   - DEBUG: Detailed information, typically of interest only when diagnosing problems.
   - INFO: Confirmation that things are working as expected.
   - WARNING: An indication that something unexpected happened, or indicative of some problem in the near future.
   - ERROR: Due to a more serious problem, the software has not been able to perform some function.
   - CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
3. Set the `APP_ENV` environment variable correctly for each environment where the bot is running.
4. Regularly review and archive log files in production to manage disk space.
5. Use log messages judiciously to avoid performance impacts, especially in the production environment.

## Customization

To modify the logging behavior:

1. Adjust log levels in the `setup_logger` function calls for specific modules.
2. Modify the `maxBytes` and `backupCount` parameters in the `RotatingFileHandler` to change log rotation behavior.
3. Update the log message format by modifying the `Formatter` string.
4. Add or remove module-specific loggers as your project structure evolves.

---

For any questions or issues regarding the logging system, please contact the project maintainer.
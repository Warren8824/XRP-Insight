import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env


def setup_logger(name, log_directory, file_level=logging.INFO, console_level=logging.WARNING):
    """Sets up a logger with both file and console handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set to lowest level to catch all logs

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create environment-specific log file
    env = os.getenv('APP_ENV', 'development')
    log_file = os.path.join(log_directory, f'{name}_{env}.log')

    try:
        # File Handler
        file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(file_level)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Failed to set up file handler for {name}: {e}")

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(console_level)
    logger.addHandler(console_handler)

    logger.info(f"Logging initialized for environment: {env}")
    return logger


def configure_loggers():
    """Configures all loggers for the application."""
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    env = os.getenv('APP_ENV', 'development')

    if env == 'production':
        file_level = logging.INFO
        console_level = logging.WARNING
    elif env == 'staging':
        file_level = logging.DEBUG
        console_level = logging.INFO
    else:  # development
        file_level = logging.DEBUG
        console_level = logging.DEBUG

    loggers = {
        'ai_intergration': file_level,
        'analysis': file_level,
        'api': file_level,
        'content_generation': file_level,
        'data_collection': file_level,
        'data_processing': file_level,
        'models': file_level,
        'scheduler': file_level,
        'utils': file_level
    }

    for name, level in loggers.items():
        setup_logger(name, log_directory, file_level=level, console_level=console_level)


# Initialize all loggers
if __name__ == "__main__":
    configure_loggers()


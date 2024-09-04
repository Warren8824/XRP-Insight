from dotenv import load_dotenv
import logging
import os
from logging.handlers import RotatingFileHandler

load_dotenv()  # Load environment variables from .env


def setup_logger(name, log_directory, file_level=logging.INFO, console_level=logging.WARNING):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set to lowest level to catch all logs

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    # Create environment-specific log file without timestamp
    env: str = os.getenv('APP_ENV', 'development')
    log_file = os.path.join(log_directory, f'{name}_{env}.log')

    # File Handler
    file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(file_level)
    logger.addHandler(file_handler)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(console_level)
    logger.addHandler(console_handler)

    logger.info(f"Logging initialized for environment: {env}")
    return logger


log_directory: str = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set the log levels based on environment or set to development if not supplied
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

ai_analysis_logger = setup_logger(
    name='ai_analysis',
    log_directory=log_directory,
    file_level=file_level,
    console_level=console_level
)
analysis_logger = setup_logger(
    name='analysis',
    log_directory=log_directory,
    file_level=file_level,
    console_level=console_level
)
api_logger = setup_logger(
    name='api',
    log_directory=log_directory,
    file_level=file_level,
    console_level=console_level
)
data_collection_logger = setup_logger(
    name='data_collecion_analysis',
    log_directory=log_directory,
    file_level=file_level,
    console_level=console_level
)
models_logger = setup_logger(
    name='models',
    log_directory=log_directory,
    file_level=file_level,
    console_level=console_level
)
tweet_generation_logger = setup_logger(
    name='tweet_generation',
    log_directory=log_directory,
    file_level=file_level,
    console_level=console_level
)
utils_logger = setup_logger(
    name='utils',
    log_directory=log_directory,
    file_level=file_level,
    console_level=console_level
)
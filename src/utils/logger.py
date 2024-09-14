from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

load_dotenv()  # Load environment variables from .env

def setup_logger(name, log_directory, file_level=logging.INFO, console_level=logging.WARNING):
    """Sets up a logger with both file and console handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set to lowest level to catch all logs

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create environment-specific log file
    env = os.getenv('APP_ENV', 'development')
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

    logger.debug(f"Logging initialized for environment: {env}")
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

    return {
        'ai_integration': setup_logger('ai_integration', log_directory, file_level, console_level),
        'analysis': setup_logger('analysis', log_directory, file_level, console_level),
        'api': setup_logger('api', log_directory, file_level, console_level),
        'content_generation': setup_logger('content_generation', log_directory, file_level, console_level),
        'data_collection': setup_logger('data_collection', log_directory, file_level, console_level),
        'data_processing': setup_logger('data_processing', log_directory, file_level, console_level),
        'models': setup_logger('models', log_directory, file_level, console_level),
        'scheduler': setup_logger('scheduler', log_directory, file_level, console_level),
        'utils': setup_logger('utils', log_directory, file_level, console_level),
        'scripts': setup_logger('scripts', log_directory, file_level, console_level),
    }

# Use a global variable to track if loggers have been initialized


loggers = None


def get_loggers():
    global loggers
    if loggers is None:
        loggers = configure_loggers()
    return loggers

# Initialize and expose loggers globally
loggers = get_loggers()
ai_integration_logger = loggers['ai_integration']
analysis_logger = loggers['analysis']
api_logger = loggers['api']
content_generation_logger = loggers['content_generation']
data_collection_logger = loggers['data_collection']
data_processing_logger = loggers['data_processing']
models_logger = loggers['models']
scheduler_logger = loggers['scheduler']
utils_logger = loggers['utils']
scripts_logger = loggers['scripts']

if __name__ == "__main__":
    print("Loggers initialized successfully")


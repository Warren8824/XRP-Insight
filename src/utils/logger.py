import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Usage
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logger = setup_logger(name='xrp_market_bot', log_file='logs/xrp_market_bot.log')

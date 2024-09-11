import os
import sys

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from sqlalchemy import create_engine, text
from src.models.base import Base
from src.models.ohlcv_data_15_min import OHLCVData15Min
from src.models.market_data_15_min import MarketData15Min
from src.models.technical_indicators_15_min import TechnicalIndicators15Min
from src.utils.config import config


def init_db():
    engine = create_engine(config['database']['url'])

    # Create TimescaleDB extension
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb"))

    # Create tables
    Base.metadata.create_all(engine)

    # Create hypertables
    with engine.connect() as conn:
        conn.execute(text("SELECT create_hypertable('ohlcv_15_data', 'timestamp', if_not_exists => TRUE)"))
        conn.execute(text("SELECT create_hypertable('market_data_15_min', 'timestamp', if_not_exists => TRUE)"))
        conn.execute(text("SELECT create_hypertable('technical_indicators', 'timestamp', if_not_exists => TRUE)"))


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
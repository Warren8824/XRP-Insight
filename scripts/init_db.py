import os
import sys

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from sqlalchemy import create_engine, text, inspect
from src.models import Base, MarketData15Min, OHLCVData15Min, TechnicalIndicators15Min
from src.utils.config import config


def init_db():
    engine = create_engine(config['database']['url'])
    inspector = inspect(engine)

    # Create TimescaleDB extension
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb"))

    # Create tables
    Base.metadata.create_all(engine)

    # Convert tables to hypertables
    with engine.connect() as conn:
        tables = [
            ("market_data_15_min", "timestamp"),
            ("ohlcv_data_15_min", "timestamp"),
            ("technical_indicators_15_min", "timestamp")
        ]

        for table_name, time_column in tables:
            if table_name in inspector.get_table_names():
                try:
                    conn.execute(text(
                        f"SELECT create_hypertable('{table_name}', '{time_column}', if_not_exists => TRUE, chunk_time_interval => INTERVAL '1 hour', migrate_data => TRUE)"))
                    print(f"Created hypertable for {table_name}")
                except Exception as e:
                    print(f"Error creating hypertable for {table_name}: {str(e)}")
            else:
                print(f"Table {table_name} does not exist")


if __name__ == "__main__":
    init_db()
    print("Database initialization process completed.")
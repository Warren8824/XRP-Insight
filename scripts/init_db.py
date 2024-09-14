from sqlalchemy import create_engine, text, inspect
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.utils.logger import scripts_logger
from src.models import Base, MarketData15Min, OHLCVData15Min, TechnicalIndicators15Min
from src.utils.config import config


def init_db():
    engine = create_engine(config['database']['url'])
    inspector = inspect(engine)

    # Check if any tables exist in the database
    existing_tables = inspector.get_table_names()

    if existing_tables:
        scripts_logger.info(f"Existing tables found: {existing_tables}. Dropping all tables.")
        Base.metadata.drop_all(engine)
        scripts_logger.info("All tables dropped successfully.")

    # Create TimescaleDB extension if it doesn't exist
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb"))

    # Create tables
    Base.metadata.create_all(engine)
    scripts_logger.info("All tables created successfully.")

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
                        f"SELECT create_hypertable('{table_name}', '{time_column}', if_not_exists => TRUE, chunk_time_interval => INTERVAL '1 hour', migrate_data => TRUE)"
                    ))
                    scripts_logger.info(f"Created hypertable for {table_name}")
                except Exception as e:
                    scripts_logger.error(f"Error creating hypertable for {table_name}: {str(e)}", exc_info=True)
            else:
                scripts_logger.warning(f"Table {table_name} does not exist")


def main():
    scripts_logger.info("Starting database initialization script.")

    try:
        # Initialize the database
        scripts_logger.info("Initializing the database...")
        init_db()
        scripts_logger.info("Database initialized successfully.")

    except Exception as e:
        scripts_logger.error(f"Error during database initialization: {e}", exc_info=True)

    finally:
        scripts_logger.info("Database initialization script finished.")


if __name__ == "__main__":
    main()

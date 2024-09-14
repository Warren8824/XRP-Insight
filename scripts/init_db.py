import os
import sys
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import OperationalError
import psycopg2

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.utils.logger import scripts_logger
from src.models import Base, MarketData15Min, OHLCVData15Min, TechnicalIndicators15Min
from src.utils.config import config


def check_tables_exist(inspector):
    required_tables = {"market_data_15_min", "ohlcv_data_15_min", "technical_indicators_15_min"}
    existing_tables = set(inspector.get_table_names())
    return required_tables.issubset(existing_tables)


def init_db():
    try:
        engine = create_engine(config['database']['url'])
        scripts_logger.info(f"Attempting to connect to database.")

        # Test the connection
        with engine.connect():
            scripts_logger.info("Successfully connected to the database.")

        inspector = inspect(engine)

        if check_tables_exist(inspector):
            scripts_logger.info("All required tables already exist. Database is already set up.")
            return

        scripts_logger.info("Initializing the database...")

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

    except OperationalError as e:
        scripts_logger.error(f"Database connection error: {str(e)}")
        if "Connection refused" in str(e):
            scripts_logger.error("Please check if the PostgreSQL server is running and accessible.")
        elif "database does not exist" in str(e):
            scripts_logger.error("The specified database does not exist. Please create it first.")
        else:
            scripts_logger.error("An unexpected database error occurred.")
        raise

    except Exception as e:
        scripts_logger.error(f"An unexpected error occurred: {str(e)}")
        raise


def main():
    scripts_logger.info("Starting database initialization script.")

    try:
        # Initialize the database
        init_db()
        scripts_logger.info("Database initialization script finished.")

    except Exception as e:
        scripts_logger.error(f"Error during database initialization: {e}", exc_info=True)


if __name__ == "__main__":
    main()

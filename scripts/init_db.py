from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import OperationalError
import psycopg2
from psycopg2 import sql

import os
import sys

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.utils.logger import scripts_logger
from src.utils.config import config
from src.models import get_models

# Setup model instances
models = get_models()
Base = models["Base"]
MarketData15Min = models["MarketData15Min"]
OHLCVData15Min = models["OHLCVData15Min"]
TechnicalIndicators15Min = models["TechnicalIndicators15Min"]


def create_database_if_not_exists(db_url):
    # Extract database name from the URL
    db_name = db_url.split("/")[-1]

    # Connect to the default 'postgres' database to create a new database
    conn = psycopg2.connect(
        host=config["database"]["host"],
        user=config["database"]["user"],
        password=config["database"]["password"],
        dbname="postgres",
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Check if the database exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
    if cursor.fetchone() is None:
        scripts_logger.info(f"Database {db_name} does not exist, creating it...")
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        scripts_logger.info(f"Database {db_name} created successfully.")
    else:
        scripts_logger.info(f"Database {db_name} already exists.")

    cursor.close()
    conn.close()


def check_tables_exist(inspector):
    required_tables = {
        "market_data_15_min",
        "ohlcv_data_15_min",
        "technical_indicators_15_min",
    }
    existing_tables = set(inspector.get_table_names())
    return required_tables.issubset(existing_tables)


def drop_database(db_url):
    db_name = config["database"]["url"]
    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    cursor = conn.cursor()

    # Terminate active connections to the database
    cursor.execute(
        sql.SQL(
            """
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = %s AND pid <> pg_backend_pid()
    """
        ),
        [db_name],
    )

    # Drop the database
    scripts_logger.info(f"Dropping database {db_name}...")
    cursor.execute(
        sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(db_name))
    )
    scripts_logger.info(f"Database {db_name} dropped successfully.")

    cursor.close()
    conn.close()


def init_db():
    try:
        # Database connection URL
        db_url = config["database"]["url"]

        # Check if the database exists, create if not
        create_database_if_not_exists(db_url)

        # Create SQLAlchemy engine
        engine = create_engine(db_url)
        scripts_logger.info(f"Attempting to connect to the database.")

        # Test the connection
        with engine.connect():
            scripts_logger.info("Successfully connected to the database.")

        # Create the database inspector
        inspector = inspect(engine)

        # Check if all required tables exist
        if check_tables_exist(inspector):
            scripts_logger.info(
                "All required tables already exist. Database is already set up."
            )
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
                ("technical_indicators_15_min", "timestamp"),
            ]

            for table_name, time_column in tables:
                if table_name in inspector.get_table_names():
                    try:
                        conn.execute(
                            text(
                                f"SELECT create_hypertable('{table_name}', '{time_column}', if_not_exists => TRUE, chunk_time_interval => INTERVAL '1 hour', migrate_data => TRUE)"
                            )
                        )
                        scripts_logger.info(f"Created hypertable for {table_name}")
                    except Exception as e:
                        scripts_logger.error(
                            f"Error creating hypertable for {table_name}: {str(e)}",
                            exc_info=True,
                        )
                else:
                    scripts_logger.warning(
                        f"Table {table_name} does not exist (should have been created)"
                    )

    except OperationalError as e:
        scripts_logger.error(f"Database connection error: {str(e)}")
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
        scripts_logger.error(
            f"Error during database initialization: {e}", exc_info=True
        )


if __name__ == "__main__":
    main()

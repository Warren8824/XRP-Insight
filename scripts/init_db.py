from sqlalchemy import create_engine, text, inspect, func
from sqlalchemy.exc import OperationalError
import psycopg2
from psycopg2 import sql

import sys
import functools

import path_setup  # Needed to access src folder
from src.utils.logger import scripts_logger
from src.utils.config import config
from src.models import get_models

# Setup model instances
models = get_models()
Base = models["Base"]
MarketData15Min = models["MarketData15Min"]
OHLCVData15Min = models["OHLCVData15Min"]
TechnicalIndicators15Min = models["TechnicalIndicators15Min"]

# Define global table information
TABLES = [
    {"name": "market_data_15_min", "model": MarketData15Min},
    {"name": "ohlcv_data_15_min", "model": OHLCVData15Min},
    {"name": "technical_indicators_15_min", "model": TechnicalIndicators15Min},
]


def create_database_if_not_exists(db_url):
    db_name = db_url.split("/")[-1]
    conn = psycopg2.connect(
        host=config["database"]["host"],
        user=config["database"]["user"],
        password=config["database"]["password"],
        dbname="postgres",
    )
    conn.autocommit = True
    cursor = conn.cursor()

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
    required_tables = set(table["name"] for table in TABLES)
    existing_tables = set(inspector.get_table_names())
    return required_tables.issubset(existing_tables)


def drop_and_recreate_all_tables(engine):
    scripts_logger.info("Starting drop_and_recreate_all_tables function")
    try:
        with engine.begin() as conn:  # Use begin() instead of connect() to ensure transaction
            try:
                # Set a timeout to prevent hanging
                conn.execute(text("SET statement_timeout = '30000';"))

                # Drop all tables
                scripts_logger.info("Dropping all tables...")
                for table in TABLES:
                    scripts_logger.info(f"Attempting to drop {table['name']}")
                    drop_table(conn, table["name"])
                    # Verify the drop
                    result = conn.execute(
                        text(
                            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = :table_name)"
                        ),
                        {"table_name": table["name"]},
                    ).scalar()
                    if not result:
                        scripts_logger.info(f"Successfully dropped {table['name']}")
                    else:
                        scripts_logger.error(f"Failed to drop {table['name']}")
                        raise Exception(f"Failed to drop {table['name']}")

                scripts_logger.info(
                    "All tables dropped. Attempting to recreate tables..."
                )

                # Recreate all tables
                scripts_logger.info(
                    "Recreating all tables based on current model schema..."
                )
                Base.metadata.create_all(bind=conn)  # Use the same connection

                # Verify tables were created
                for table in TABLES:
                    result = conn.execute(
                        text(
                            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = :table_name)"
                        ),
                        {"table_name": table["name"]},
                    ).scalar()
                    if result:
                        scripts_logger.info(f"Successfully created {table['name']}")
                    else:
                        scripts_logger.error(f"Failed to create {table['name']}")
                        raise Exception(f"Failed to create {table['name']}")

                scripts_logger.info("All tables have been recreated.")

            finally:
                # Reset timeout
                try:
                    conn.execute(text("SET statement_timeout = '0';"))
                except Exception as e:
                    scripts_logger.error(f"Error resetting statement timeout: {str(e)}")
    except Exception as e:
        scripts_logger.error(
            f"Error in drop_and_recreate_all_tables: {str(e)}", exc_info=True
        )
        raise
    finally:
        scripts_logger.info("Exiting drop_and_recreate_all_tables function")


def drop_table(conn, table_name):
    try:
        # First, ensure no other sessions are connected to this table
        conn.execute(
            text(
                """
            SELECT pg_terminate_backend(pid) 
            FROM pg_stat_activity 
            WHERE datname = current_database()
            AND pid <> pg_backend_pid()
            AND state = 'idle'
        """
            )
        )

        # Drop the table
        conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE;"))
        scripts_logger.info(f"Dropped table: {table_name}")
    except Exception as e:
        scripts_logger.error(f"Error dropping table {table_name}: {str(e)}")
        raise  # Re-raise the exception to be handled by the calling function


def prompt_user_for_action(engine):
    try:
        with engine.connect() as connection:
            # Start a new transaction
            with connection.begin():
                try:
                    # Set a timeout to prevent hanging
                    connection.execute(
                        text("SET statement_timeout = '30000';")
                    )  # 30 seconds

                    for table in TABLES:
                        table_name = table["name"]
                        try:
                            row_count = connection.execute(
                                text(f"SELECT COUNT(*) FROM {table_name};")
                            ).scalar()

                            if row_count > 0:
                                user_input = (
                                    input(
                                        f"Table {table_name} has {row_count} rows. Do you want to delete all data from this table and begin fresh? (yes/no): "
                                    )
                                    .strip()
                                    .lower()
                                )

                                if user_input == "yes":
                                    return True  # Signal to drop and recreate tables
                                elif user_input == "no":
                                    scripts_logger.info(
                                        f"Continuing with the existing data in {table_name}."
                                    )
                                else:
                                    print("Invalid input. Please enter 'yes' or 'no'.")
                                    return prompt_user_for_action(engine)
                            else:
                                scripts_logger.info(f"Table {table_name} has no data.")

                        except Exception as e:
                            scripts_logger.error(
                                f"Error checking table {table_name}: {str(e)}"
                            )
                            raise

                finally:
                    # Always reset timeout
                    try:
                        connection.execute(text("SET statement_timeout = '0';"))
                    except Exception as e:
                        scripts_logger.error(
                            f"Error resetting statement timeout: {str(e)}"
                        )

    except Exception as e:
        scripts_logger.error(f"Error in prompt_user_for_action: {str(e)}")
        raise

    update_schema = (
        input("Do you require all tables to be reset for schema updates? (yes/no): ")
        .strip()
        .lower()
    )
    if update_schema == "yes":
        return True  # Signal to drop and recreate tables
    elif update_schema == "no":
        scripts_logger.info("Table schema not modified.")
        return False
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")
        return prompt_user_for_action(engine)


def init_db():
    try:
        db_url = config["database"]["url"]
        create_database_if_not_exists(db_url)
        engine = create_engine(db_url)
        scripts_logger.info("Attempting to connect to the database.")

        with engine.connect():
            scripts_logger.info("Successfully connected to the database.")

        inspector = inspect(engine)

        if check_tables_exist(inspector):
            print("All required tables already exist.")
            should_recreate = prompt_user_for_action(engine)
            if should_recreate:
                drop_and_recreate_all_tables(engine)
        else:
            scripts_logger.info("Initializing the database...")
            Base.metadata.create_all(engine)
            scripts_logger.info("All required tables created successfully.")

    except OperationalError as e:
        scripts_logger.error(f"Database connection error: {str(e)}")
        raise
    except Exception as e:
        scripts_logger.error(f"An unexpected error occurred: {str(e)}")
        raise


def main():
    scripts_logger.info("Starting database initialization script.")
    try:
        init_db()
        scripts_logger.info("Database initialization script finished.")
    except Exception as e:
        scripts_logger.error(
            f"Error during database initialization: {e}", exc_info=True
        )


if __name__ == "__main__":
    main()

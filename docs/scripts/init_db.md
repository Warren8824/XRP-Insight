# init_db.py

This script initializes the database for the XRP Insight project, creating necessary tables and setting up TimescaleDB hypertables.

## Key Functions

### create_database_if_not_exists(db_url)
Checks if the specified database exists and creates it if it doesn't.

### check_tables_exist(inspector)
Verifies if all required tables are present in the database.

### drop_database(db_url)
Drops the existing database (used for resetting the database).

### init_db()
Main function to initialize the database:
- Connects to the database
- Creates tables if they don't exist
- Sets up TimescaleDB extension
- Converts tables to hypertables

## Process

1. Connects to the database using configuration from `config.py`
2. Creates the database if it doesn't exist
3. Creates tables: market_data_15_min, ohlcv_data_15_min, technical_indicators_15_min
4. Sets up TimescaleDB extension
5. Converts tables to TimescaleDB hypertables

## Usage

Run this script to initialize or reset the database: `python scripts/init_db.py`

## Notes

- Requires SQLAlchemy, psycopg2, and TimescaleDB
- Logs all operations and errors
- Handles database connection errors and unexpected exceptions
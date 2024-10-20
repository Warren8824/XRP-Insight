from datetime import datetime, timedelta, timezone
import math

import path_setup  # Needed to access src folder
from src.data_collection.collector import collect_historical_data
from src.models.base import SessionLocal
from src.utils.logger import scripts_logger as logger
from src.utils.config import config
from sqlalchemy import func
from src.models import get_models

# Get the models
models = get_models()
OHLCVData15Min = models["OHLCVData15Min"]

# Constants
API_CALLS_PER_DAY = 96  # 15-minute intervals for 24 hours
ROWS_PER_API_CALL = 100
DAILY_LIMIT = config["api_limits"]["coinapi_daily"]
MAX_BACKFILL_DAYS = 90


def round_to_15_minutes(dt):
    minutes_to_subtract = dt.minute % 15
    return dt.replace(minute=dt.minute - minutes_to_subtract, second=0, microsecond=0)


def calculate_api_calls(intervals):
    return math.ceil(intervals / ROWS_PER_API_CALL)


def update_daily_limit(api_calls_used):
    global DAILY_LIMIT
    DAILY_LIMIT -= api_calls_used


def bf_data(start_date, end_date):
    db = SessionLocal()
    try:
        collect_historical_data(db, start_date, end_date)
    finally:
        db.close()


def get_last_data_timestamp():
    db = SessionLocal()
    try:
        last_timestamp = db.query(func.max(OHLCVData15Min.timestamp)).scalar()
        return last_timestamp.astimezone(timezone.utc)
    finally:
        db.close()


def calculate_missing_intervals(last_timestamp, current_time):
    if last_timestamp is None:
        return None
    time_difference = current_time - last_timestamp
    return int(time_difference.total_seconds() / (15 * 60))  # 15 minutes in seconds


def prompt_user_for_days():
    while True:
        try:
            days = int(
                input("How many days of historical data do you want to retrieve? ")
            )
            if days <= 0:
                print("Please enter a positive number of days.")
                continue

            api_calls = calculate_api_calls(days * API_CALLS_PER_DAY)
            print(
                f"Retrieving {days} days of data will require approximately {api_calls} API calls."
            )

            if api_calls > DAILY_LIMIT:
                print(
                    f"Warning: This exceeds the daily limit of {DAILY_LIMIT} API calls."
                )

            confirm = input("Do you want to proceed? (y/n): ").lower()
            if confirm == "y":
                return days
            elif confirm == "n":
                print("Operation cancelled.")
                return None
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def prompt_user_for_backfill(missing_intervals):
    api_calls = calculate_api_calls(missing_intervals)
    print(f"There are {missing_intervals} missing 15-minute intervals.")
    print(f"This will require approximately {api_calls} API calls.")

    if api_calls > DAILY_LIMIT:
        print(f"Warning: This exceeds the daily limit of {DAILY_LIMIT} API calls.")

    while True:
        confirm = input("Do you want to proceed with the back-fill? (y/n): ").lower()
        if confirm == "y":
            return True
        elif confirm == "n":
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


if __name__ == "__main__":
    current_time = round_to_15_minutes(datetime.now(timezone.utc))
    last_timestamp = get_last_data_timestamp()

    if last_timestamp is None:
        logger.info("No existing data found. Prompting for initial back-fill.")
        days = prompt_user_for_days()
        if days is not None:
            start_date = round_to_15_minutes(current_time - timedelta(days=days))
            end_date = current_time

            logger.info(
                f"Starting historical data back-fill from {start_date} to {end_date}"
            )
            bf_data(start_date, end_date)

            api_calls_used = calculate_api_calls(days * API_CALLS_PER_DAY)
            update_daily_limit(api_calls_used)

            logger.info(
                f"Historical data back-fill completed. {api_calls_used} API calls used."
            )
            logger.info(f"Remaining daily API calls: {DAILY_LIMIT}")
        else:
            logger.info("Historical data back-fill cancelled by user.")
    else:
        missing_intervals = calculate_missing_intervals(last_timestamp, current_time)

        if missing_intervals == 0:
            logger.info("Database is up to date. No backfill needed.")

        elif missing_intervals > MAX_BACKFILL_DAYS * API_CALLS_PER_DAY:
            logger.info(
                f"The data gap is more than {MAX_BACKFILL_DAYS} days. Please run init_db.py to reset all tables."
            )
        else:
            if prompt_user_for_backfill(missing_intervals):
                start_date = last_timestamp + timedelta(minutes=15)
                end_date = round_to_15_minutes(current_time)

                logger.info(
                    f"Starting historical data back-fill from {start_date} to {end_date}"
                )
                bf_data(start_date, end_date)

                api_calls_used = calculate_api_calls(missing_intervals)
                update_daily_limit(api_calls_used)

                logger.info(
                    f"Historical data back-fill completed. {api_calls_used} API calls used."
                )
                logger.info(f"Remaining daily API calls: {DAILY_LIMIT}")
            else:
                logger.info("Historical data back-fill cancelled by user.")

    # Next interval's data collection
    next_interval_start = round_to_15_minutes(current_time + timedelta(minutes=15))
    logger.info(f"Next data collection will be at {next_interval_start}")
    logger.debug("This will use 1 API call.")

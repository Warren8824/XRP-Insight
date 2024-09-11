from datetime import datetime, timedelta, timezone
from src.data_collection.collector import collect_historical_data
from src.models.base import SessionLocal
from src.utils.logger import utils_logger as logger


def bf_data(start_date, end_date):
    db = SessionLocal()
    try:
        collect_historical_data(db, start_date, end_date)
    finally:
        db.close()


if __name__ == "__main__":
    # Get the current date and time
    end_date = datetime.now(timezone.utc)

    # Calculate the date 90 days before the current date
    start_date = end_date - timedelta(days=90)

    logger.info(f"Starting historical data backfill from {start_date} to {end_date}")
    bf_data(start_date, end_date)
    logger.info("Historical data backfill completed")

from datetime import datetime, timedelta, timezone

import path_setup # Needed to access src folder
from src.data_collection.collector import collect_historical_data
from src.models.base import SessionLocal
from src.utils.logger import scripts_logger as logger


def bf_data(start_date, end_date):
    db = SessionLocal()
    try:
        collect_historical_data(db, start_date, end_date)
    finally:
        db.close()


if __name__ == "__main__":
    end_date = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    start_date = end_date - timedelta(days=1)  # Start with just 1 day
    logger.info(f"Starting historical data back-fill from {start_date} to {end_date}")
    bf_data(start_date, end_date)
    logger.info("Historical data back-fill completed")

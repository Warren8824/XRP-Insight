import schedule
import time
from src.data_collection.collector import run_data_collection
from src.models.base import SessionLocal
from src.utils.logger import utils_logger as logger


def job():
    db = SessionLocal()
    try:
        run_data_collection(db)
    finally:
        db.close()


def run_scheduler():
    schedule.every(15).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    logger.info("Starting scheduler")
    run_scheduler()
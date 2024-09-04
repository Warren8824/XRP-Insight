import requests
from datetime import datetime, timedelta, timezone
import pandas as pd
from sqlalchemy import func
from src.models.base import Base, get_db
from src.models.ohlcv_15_min_data import OHLCV15Data
from src.utils.config import config
from src.utils.logger import data_collection_logger

API_KEY = config['api_keys']['coinapi']
BASE_URL = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_XRP_USD/history'


def fetch_ohlcv_historic_data(start_date, end_date):
    headers = {'X-CoinAPI-Key': API_KEY}
    params = {
        'period_id': '15MIN',
        'time_start': start_date.isoformat(),
        'time_end': end_date.isoformat(),
        'limit': 3456
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        data_collection_logger.info(f"OHLCV historic data received for period: {start_date.isoformat()} to {end_date.isoformat()}")
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


def get_earliest_timestamp(db):
    return db.query(func.min(OHLCV15Data.timestamp)).scalar()


def process_and_save_data(data, db):
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['time_period_start'])
    df['price_change'] = df['price_close'] - df['price_open']

    for _, row in df.iterrows():
        ohlcv_data = OHLCV15Data(
            timestamp=row['timestamp'],
            open=row['price_open'],
            high=row['price_high'],
            low=row['price_low'],
            close=row['price_close'],
            volume=row['volume_traded'],
            price_change=row['price_change']
        )
        db.add(ohlcv_data)

    db.commit()


# Main execution
def main():
    db = next(get_db())
    Base.metadata.create_all(bind=db.bind)  # Ensure the table is created

    earliest_timestamp = get_earliest_timestamp(db)

    if earliest_timestamp:
        end_date = earliest_timestamp
    else:
        end_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

    start_date = end_date - timedelta(days=36)

    data = fetch_ohlcv_historic_data(start_date, end_date)
    if data:
        process_and_save_data(data, db)
        print(f"Saved data for period: {start_date} to {end_date}")
    else:
        print(f"Failed to fetch data for period: {start_date} to {end_date}")

    print("Script execution complete. Run again for the next chunk of data.")


if __name__ == "__main__":
    main()

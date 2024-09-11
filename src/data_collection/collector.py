from sqlalchemy.orm import Session

from datetime import datetime, timezone, timedelta

from src.data_collection.coingecko_client import CoinGeckoClient
from src.data_collection.coinapi_client import CoinAPIClient
from src.models.market_data_15_min import MarketData15Min
from src.models.ohlcv_data_15_min import OHLCVData15Min
from src.utils.config import config
from src.utils.logger import data_collection_logger as logger

coingecko_client = CoinGeckoClient()
coinapi_client = CoinAPIClient()


def collect_and_store_market_data(db: Session):
    try:
        market_data = coingecko_client.get_xrp_data()

        # Convert the timestamp to a datetime object
        timestamp = datetime.fromtimestamp(market_data['last_updated_at'], tz=timezone.utc)

        new_market_data = MarketData15Min(
            timestamp=timestamp,
            price_usd=market_data['market_data']['current_price']['usd'],
            market_cap=market_data['market_data']['market_cap']['usd'],
            total_volume=market_data['market_data']['total_volume']['usd'],
            circulating_supply=market_data['market_data']['circulating_supply'],
            total_supply=market_data['market_data']['total_supply'],
            max_supply=market_data['market_data']['max_supply']
        )

        db.add(new_market_data)
        db.commit()
        logger.info(f"Stored market data for timestamp: {new_market_data.timestamp}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error collecting market data: {str(e)}")


def collect_and_store_ohlcv_data(db: Session):
    try:
        ohlcv_data = coinapi_client.get_ohlcv_data()

        for candle in ohlcv_data:
            # Parse the ISO 8601 timestamp
            timestamp = datetime.fromisoformat(candle['time_period_start'].rstrip('Z')).replace(tzinfo=timezone.utc)

            new_ohlcv = OHLCVData15Min(
                timestamp=timestamp,
                open=candle['price_open'],
                high=candle['price_high'],
                low=candle['price_low'],
                close=candle['price_close'],
                volume=candle['volume_traded'],
                price_change=candle['price_close'] - candle['price_open']
            )

            db.add(new_ohlcv)

        db.commit()
        logger.info(f"Stored OHLCV data for {len(ohlcv_data)} intervals")
    except Exception as e:
        db.rollback()
        logger.error(f"Error collecting OHLCV data: {str(e)}")


def collect_historical_data(db: Session, start_date: datetime, end_date: datetime):
    try:
        current_date = start_date
        while current_date < end_date:
            next_date = min(current_date + timedelta(days=1), end_date)
            ohlcv_data = coinapi_client.get_historical_ohlcv_data(current_date, next_date)

            for candle in ohlcv_data:
                timestamp = datetime.fromisoformat(candle['time_period_start'].rstrip('Z')).replace(tzinfo=timezone.utc)

                new_ohlcv = OHLCVData15Min(
                    timestamp=timestamp,
                    open=candle['price_open'],
                    high=candle['price_high'],
                    low=candle['price_low'],
                    close=candle['price_close'],
                    volume=candle['volume_traded'],
                    price_change=candle['price_close'] - candle['price_open']
                )

                db.add(new_ohlcv)

            db.commit()
            logger.info(f"Stored historical OHLCV data for {current_date.date()}")
            current_date = next_date
    except Exception as e:
        db.rollback()
        logger.error(f"Error collecting historical data: {str(e)}")


def run_data_collection(db: Session):
    collect_and_store_market_data(db)
    collect_and_store_ohlcv_data(db)


if __name__ == "__main__":
    from src.models.base import SessionLocal

    db = SessionLocal()
    try:
        run_data_collection(db)
    finally:
        db.close()

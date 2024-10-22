import requests
from sqlalchemy.orm import Session

from datetime import datetime, timezone, timedelta

from src.data_collection.coingecko_client import CoinGeckoClient
from src.data_collection.coinapi_client import CoinAPIClient
from src.models.market_data_15_min import MarketData15Min
from src.models.ohlcv_data_15_min import OHLCVData15Min
from ..utils.logger import data_collection_logger


def collect_and_store_market_data(
    db: Session, coingecko_client: CoinGeckoClient = None
):
    """
    Collect current market data for XRP from CoinGecko and store it in the database.

    This function retrieves the latest market data for XRP cryptocurrency from the
    CoinGecko API, including current price, market cap, volume, and supply information.
    It then stores this data in the provided database.

    Args:
        db: A database session object for storing the collected data.

    Returns:
        None

    Raises:
        Any exceptions raised by the CoinGecko API or database operations.
    """
    if coingecko_client is None:
        coingecko_client = CoinGeckoClient()
    try:
        data_collection_logger.info("Collecting XRP market data from CoinGecko...")
        market_data = coingecko_client.get_market_data()
        timestamp_str = market_data["last_updated"]
        timestamp = datetime.fromisoformat(timestamp_str.rstrip("Z")).replace(
            tzinfo=timezone.utc
        )

        new_market_data = MarketData15Min(
            timestamp=timestamp,
            price_usd=market_data["market_data"]["current_price"]["usd"],
            market_cap=market_data["market_data"]["market_cap"]["usd"],
            total_volume=market_data["market_data"]["total_volume"]["usd"],
            circulating_supply=market_data["market_data"]["circulating_supply"],
            total_supply=market_data["market_data"]["total_supply"],
            max_supply=market_data["market_data"]["max_supply"],
        )

        db.add(new_market_data)
        db.commit()
        data_collection_logger.info(
            f"Stored market data for timestamp: {new_market_data.timestamp}"
        )
    except Exception as e:
        db.rollback()
        data_collection_logger.error(f"Error collecting market data: {str(e)}")
        raise


def collect_and_store_ohlcv_data(db: Session, coinapi_client: CoinAPIClient = None):
    """
    Collect and store the latest OHLCV (Open, High, Low, Close, Volume) data for XRP.

    This function retrieves the most recent OHLCV data for XRP cryptocurrency from
    the CoinAPI. It then stores this data in the provided database.

    Args:
        db: A database session object for storing the collected data.

    Returns:
        None

    Raises:
        Any exceptions raised by the CoinAPI or database operations.
    """
    if coinapi_client is None:
        coinapi_client = CoinAPIClient()
    try:
        data_collection_logger.info("Collecting XRP OHLCV data from CoinAPI...")
        ohlcv_data = coinapi_client.get_ohlcv_data()

        for candle in ohlcv_data:
            timestamp_str = candle["time_period_end"].rstrip("Z")
            if "." in timestamp_str:
                timestamp_str = timestamp_str[
                    : timestamp_str.index(".")
                ]  # Keep 0 decimals
            timestamp = datetime.fromisoformat(timestamp_str).replace(
                tzinfo=timezone.utc
            )

            new_ohlcv = OHLCVData15Min(
                timestamp=timestamp,
                open=candle["price_open"],
                high=candle["price_high"],
                low=candle["price_low"],
                close=candle["price_close"],
                volume=candle["volume_traded"],
                trades_count=candle["trades_count"],
                price_change=candle["price_close"] - candle["price_open"],
            )

            db.add(new_ohlcv)

        db.commit()
        data_collection_logger.info(
            f"Stored OHLCV data for {len(ohlcv_data)} intervals"
        )
    except Exception as e:
        db.rollback()
        data_collection_logger.error(f"Error collecting OHLCV data: {str(e)}")
        raise


def collect_historical_data(
    db: Session,
    start_date: datetime,
    end_date: datetime,
    coinapi_client: CoinAPIClient = None,
):
    """
    Collect and store historical OHLCV data for XRP within a specified date range.

    This function retrieves historical OHLCV data for XRP cryptocurrency from CoinAPI
    for the period between start_date and end_date. It then stores this data in the
    provided database.

    Args:
        db: A database session object for storing the collected data.
        start_date (datetime): The start date for the historical data collection.
        end_date (datetime): The end date for the historical data collection.

    Returns:
        None

    Raises:
        Any exceptions raised by the CoinAPI or database operations.
    """
    if coinapi_client is None:
        coinapi_client = CoinAPIClient()
    try:
        current_date = start_date
        data_collection_logger.info(
            f"Collecting historical OHLCV data from {start_date} to {end_date}..."
        )

        while current_date <= end_date:
            next_date = min(current_date + timedelta(days=1), end_date)
            ohlcv_data = coinapi_client.get_historical_ohlcv_data(
                current_date, next_date
            )

            data_collection_logger.info(
                f"Retrieved {len(ohlcv_data)} data points for {current_date.date()}"
            )

            for candle in ohlcv_data:
                timestamp_str = candle["time_period_end"].rstrip("Z")
                if "." in timestamp_str:
                    timestamp_str = timestamp_str[
                        : timestamp_str.index(".")
                    ]  # Keep 0 decimal places
                timestamp = datetime.fromisoformat(timestamp_str).replace(
                    tzinfo=timezone.utc
                )

                new_ohlcv = OHLCVData15Min(
                    timestamp=timestamp,
                    open=candle["price_open"],
                    high=candle["price_high"],
                    low=candle["price_low"],
                    close=candle["price_close"],
                    volume=candle["volume_traded"],
                    trades_count=candle["trades_count"],
                    price_change=candle["price_close"] - candle["price_open"],
                )

                db.add(new_ohlcv)

            db.commit()
            data_collection_logger.info(
                f"Stored historical OHLCV data for {current_date.date()}"
            )
            current_date = next_date
            if (
                current_date >= end_date
            ):  # Break loop after collecting most recent timestamp
                break
    except Exception as e:
        db.rollback()
        data_collection_logger.error(f"Error collecting historical data: {str(e)}")
        raise


def run_data_collection(
    db: Session,
    coingecko_client: CoinGeckoClient = None,
    coinapi_client: CoinAPIClient = None,
):
    """
    Run both market data and ohlcv collect and store functions.
    :param db:
    :param coingecko_client: Get market data, get historical data
    :param coinapi_client: Get ohlcv data, get historical ohlcv data
    :return: Nothing - Stores data in db
    """
    try:
        data_collection_logger.info("Starting data collection process...")
        collect_and_store_market_data(db, coingecko_client)
        collect_and_store_ohlcv_data(db, coinapi_client)
        data_collection_logger.info("Data collection completed successfully.")
    except Exception as e:
        data_collection_logger.error(f"Error in data collection process: {str(e)}")


if __name__ == "__main__":
    from src.models.base import SessionLocal

    db = SessionLocal()
    try:
        run_data_collection(db)
    finally:
        db.close()
        logger.info("Database connection closed.")

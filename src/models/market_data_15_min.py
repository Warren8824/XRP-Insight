from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.orm import validates
from sqlalchemy import event

from src.models.base import Base
from src.utils.logger import models_logger  # Import directly from utils

class MarketData15Min(Base):
    __tablename__ = "market_data_15_min"

    timestamp = Column(DateTime(timezone=True), primary_key=True)
    id = Column(Integer, primary_key=True, index=True)
    price_usd = Column(Float, nullable=False)
    market_cap = Column(Float, nullable=False)
    total_volume = Column(Float, nullable=False)
    circulating_supply = Column(Float, nullable=False)
    total_supply = Column(Float, nullable=False)
    max_supply = Column(Float, nullable=True)

    def __repr__(self):
        return f'<MarketData15Min(id={self.id}, timestamp={self.timestamp}, price_usd={self.price_usd})>'

    @validates('price_usd')
    def validate_price_usd(self, key, value):
        if value < 0:
            models_logger.warning(f"Attempted to set negative price_usd: {value}")
        return value

    @validates('market_cap')
    def validate_market_cap(self, key, value):
        if value < 0:
            models_logger.warning(f"Attempted to set negative market_cap: {value}")
        return value


@event.listens_for(MarketData15Min, 'after_insert')
def after_insert(mapper, connection, target):
    models_logger.info(f"Inserted MarketData15Min record: {target}")


@event.listens_for(MarketData15Min, 'after_update')
def after_update(mapper, connection, target):
    models_logger.info(f"Updated MarketData15Min record: {target}")


@event.listens_for(MarketData15Min, 'after_delete')
def after_delete(mapper, connection, target):
    models_logger.info(f"Deleted MarketData15Min record: {target}")

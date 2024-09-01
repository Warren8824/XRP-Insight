from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func
from src.models.base import Base

class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    price_usd = Column(Float)
    market_cap = Column(Float)
    volume_24h = Column(Float)
    price_change_24h = Column(Float)

    def __repr__(self):
        return f"<MarketData(id={self.id}, timestamp={self.timestamp}, price_usd={self.price_usd})>"
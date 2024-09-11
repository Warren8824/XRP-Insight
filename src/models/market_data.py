from sqlalchemy import Column, Integer, Float, DateTime
from .base import Base


class MarketData(Base):
    __tablename__ = "market_15_data"
    __table_args__ = {"info": {"is_hypertable": True, "hypertable_interval": "15 minute"}}

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), index=True)
    price_usd = Column(Float)
    market_cap = Column(Float)
    volume_24h = Column(Float)
    price_change_24h = Column(Float)

    def __repr__(self):
        return f"<MarketData(id={self.id}, timestamp={self.timestamp}, price_usd={self.price_usd})>"

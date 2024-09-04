from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func
from src.models.base import Base

class OHLCV15Data(Base):
    __tablename__ = "ohlcv_15_data"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    price_change = Column(Float)

    def __repr__(self):
        return f"<OHLCV15Data(id={self.id}, timestamp={self.timestamp}, price_usd={self.price_usd})>"
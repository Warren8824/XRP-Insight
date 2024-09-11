from sqlalchemy import Column, Integer, Float, DateTime
from src.models.base import Base

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
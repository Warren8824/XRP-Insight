from sqlalchemy import Column, Integer, Float, DateTime
from src.models.base import Base


class TechnicalIndicators15Min(Base):
    __tablename__ = "technical_indicators_15_min"

    timestamp = Column(DateTime(timezone=True), primary_key=True)
    id = Column(Integer, primary_key=True, index=True)
    rsi_14 = Column(Float)
    macd_line = Column(Float)
    macd_signal = Column(Float)
    macd_histogram = Column(Float)
    bb_upper = Column(Float)
    bb_middle = Column(Float)
    bb_lower = Column(Float)
    ema_12 = Column(Float)
    ema_26 = Column(Float)
    sma_50 = Column(Float)
    sma_200 = Column(Float)

    def __repr__(self):
        return f'<TechnicalIndicators(id={self.id}, timestamp={self.timestamp})>'
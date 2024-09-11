from sqlalchemy import Column, Integer, Float, DateTime
from src.models.base import Base


class TechnicalIndicators15Min(Base):
    __tablename__ = "technical_indicators_15_min"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), index=True, unique=True)
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

    __table_args__ = (
        {"info": {"is_hypertable": True, "hypertable_interval": "15 minute"}},
    )

    def __repr__(self):
        return f'<TechnicalIndicators(id={self.id}, timestamp={self.timestamp})>'

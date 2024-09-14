from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.orm import validates
from sqlalchemy import event

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

    @validates('rsi_14')
    def validate_rsi_14(self, key, value):
        if value is not None and (value < 0 or value > 100):
            models_logger.warning(f"Invalid RSI value: {value}")
        return value

    @validates('bb_upper', 'bb_middle', 'bb_lower', 'ema_12', 'ema_26', 'sma_50', 'sma_200')
    def validate_positive_float(self, key, value):
        if value is not None and value < 0:
            models_logger.warning(f"Negative value for {key}: {value}")
        return value

@event.listens_for(TechnicalIndicators15Min, 'after_insert')
def after_insert(mapper, connection, target):
    models_logger.info(f"Inserted TechnicalIndicators15Min record: {target}")

@event.listens_for(TechnicalIndicators15Min, 'after_update')
def after_update(mapper, connection, target):
    models_logger.info(f"Updated TechnicalIndicators15Min record: {target}")

@event.listens_for(TechnicalIndicators15Min, 'after_delete')
def after_delete(mapper, connection, target):
    models_logger.info(f"Deleted TechnicalIndicators15Min record: {target}")

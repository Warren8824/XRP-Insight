from sqlalchemy import Column, Integer, Float, DateTime, CheckConstraint
from sqlalchemy.orm import validates
from sqlalchemy import event

from src.models.base import Base


class OHLCVData15Min(Base):
    __tablename__ = "ohlcv_data_15_min"

    timestamp = Column(DateTime(timezone=True), primary_key=True)
    id = Column(Integer, primary_key=True, index=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    price_change = Column(Float, nullable=False)

    def __repr__(self):
        return f'<OHLCV15Data(id={self.id}, timestamp={self.timestamp}, close={self.close})>'

    @validates('open', 'high', 'low', 'close', 'volume', 'price_change')
    def validate_fields(self, key, value):
        # Check for negative values
        if value < 0:
            models_logger.warning(f"Attempted to set negative {key}: {value}")

        # Special checks for 'high' and 'low'
        if key in ['high', 'low']:
            if key == 'high' and hasattr(self, 'low') and value < self.low:
                models_logger.warning(f"High value {value} is less than low value {self.low}")
            elif key == 'low' and hasattr(self, 'high') and value > self.high:
                models_logger.warning(f"Low value {value} is greater than high value {self.high}")

        return value

@event.listens_for(OHLCVData15Min, 'after_insert')
def after_insert(mapper, connection, target):
    models_logger.info(f"Inserted OHLCVData15Min record: {target}")

@event.listens_for(OHLCVData15Min, 'after_update')
def after_update(mapper, connection, target):
    models_logger.info(f"Updated OHLCVData15Min record: {target}")

@event.listens_for(OHLCVData15Min, 'after_delete')
def after_delete(mapper, connection, target):
    models_logger.info(f"Deleted OHLCVData15Min record: {target}")
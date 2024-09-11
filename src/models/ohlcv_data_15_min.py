from sqlalchemy import Column, Integer, Float, DateTime, CheckConstraint
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

    __table_args__ = (
        CheckConstraint('high >= low', name='check_high_low'),
    )

    def __repr__(self):
        return f'<OHLCV15Data(id={self.id}, timestamp={self.timestamp}, close={self.close})>'

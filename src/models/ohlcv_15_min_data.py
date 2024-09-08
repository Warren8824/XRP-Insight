from sqlalchemy import Column, Integer, Float, DateTime, CheckConstraint
from src.models.base import Base


class OHLCV15Data(Base):
    __tablename__ = "ohlcv_15_data"


    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), index=True, unique=True)
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

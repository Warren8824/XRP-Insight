# Market Data Model Documentation

## Overview

This document outlines the `MarketData` model in the XRP Market Bot project. The `MarketData` model is responsible for storing historical market data for XRP, including price, market cap, volume, and price changes.

## Model Definition

The `MarketData` model is defined in `src/models/market_data.py` and inherits from the `Base` class defined in `src/models/base.py`.

```python
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
```

## Attributes

The `MarketData` model has the following attributes:

1. **id**: Integer
   - Primary key for the table
   - Automatically incremented

2. **timestamp**: DateTime
   - Represents the time when the market data was recorded
   - Automatically set to the current time when a new record is created
   - Includes timezone information
   - Indexed for faster querying

3. **price_usd**: Float
   - The price of XRP in USD at the time of recording

4. **market_cap**: Float
   - The market capitalization of XRP at the time of recording

5. **volume_24h**: Float
   - The trading volume of XRP in the last 24 hours

6. **price_change_24h**: Float
   - The price change of XRP in the last 24 hours

## Usage

### Creating a new MarketData record

To create a new market data record:

```python
from src.models.market_data import MarketData
from src.models.base import get_db

def save_market_data(price_usd, market_cap, volume_24h, price_change_24h):
    db = next(get_db())
    try:
        new_data = MarketData(
            price_usd=price_usd,
            market_cap=market_cap,
            volume_24h=volume_24h,
            price_change_24h=price_change_24h
        )
        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        return new_data
    finally:
        db.close()
```

### Querying MarketData records

To query market data records:

```python
from src.models.market_data import MarketData
from src.models.base import get_db

def get_latest_market_data():
    db = next(get_db())
    try:
        return db.query(MarketData).order_by(MarketData.timestamp.desc()).first()
    finally:
        db.close()

def get_market_data_range(start_date, end_date):
    db = next(get_db())
    try:
        return db.query(MarketData).filter(
            MarketData.timestamp.between(start_date, end_date)
        ).all()
    finally:
        db.close()
```

## Best Practices

1. Always use the `get_db()` function from `src.models.base` to obtain a database session.
2. Close the database session after use, preferably using a try-finally block.
3. When adding new fields to the model, make sure to update any existing data ingestion and processing logic accordingly.
4. Use appropriate data types for each field to ensure data integrity and optimal storage.

## Customization

To modify the `MarketData` model:

1. Add, remove, or modify columns as needed.
2. Update any functions or methods that interact with the `MarketData` model.
3. If making significant changes, consider creating a database migration to update the existing database schema.

---

For any questions or issues regarding the MarketData model, please contact the project maintainer.
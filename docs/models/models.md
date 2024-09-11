# Database Models Module

The database models module defines the structure of the database tables used in the XRP Insight project. It uses SQLAlchemy ORM (Object-Relational Mapping) to interact with the TimescaleDB database.

## Base Configuration (base.py)

This file sets up the SQLAlchemy engine, session, and base model. It includes:

- Database URL configuration
- SQLAlchemy engine creation
- Session creation
- Base model definition
- Custom compile function for TimescaleDB hypertables
- Database initialization function

### Key Functions:
- `get_db()`: Yields a database session
- `init_db()`: Initializes the database and creates the TimescaleDB extension

## Market Data Model (market_data_15_min.py)

This model represents 15-minute interval market data for XRP.

### Columns:
- timestamp (primary key)
- id (primary key)
- price_usd
- market_cap
- total_volume
- circulating_supply
- total_supply
- max_supply

## OHLCV Data Model (ohlcv_data_15_min.py)

This model represents 15-minute interval OHLCV (Open, High, Low, Close, Volume) data for XRP.

### Columns:
- timestamp (primary key)
- id (primary key)
- open
- high
- low
- close
- volume
- price_change

### Constraints:
- Check constraint to ensure high >= low

## Technical Indicators Model (technical_indicators_15_min.py)

This model represents various technical indicators calculated at 15-minute intervals.

### Columns:
- timestamp (primary key)
- id (primary key)
- rsi_14
- macd_line
- macd_signal
- macd_histogram
- bb_upper
- bb_middle
- bb_lower
- ema_12
- ema_26
- sma_50
- sma_200

## Usage

To use these models in your code:

```python
from src.models import MarketData15Min, OHLCVData15Min, TechnicalIndicators15Min
from src.models.base import get_db

# Example: Inserting market data
def insert_market_data(data):
    db = next(get_db())
    try:
        new_data = MarketData15Min(**data)
        db.add(new_data)
        db.commit()
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()
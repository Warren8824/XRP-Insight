# market_data_15_min.py

This file defines the `MarketData15Min` model, which represents 15-minute interval market data for XRP.

## Class: MarketData15Min

Inherits from `Base` (SQLAlchemy declarative base).

### Table Name
`market_data_15_min`

### Columns

- `timestamp` (DateTime, primary key): The timestamp of the market data point (timezone-aware)
- `id` (Integer, primary key, indexed): Unique identifier for the record
- `price_usd` (Float, non-nullable): The price of XRP in USD
- `market_cap` (Float, non-nullable): The market capitalization of XRP
- `total_volume` (Float, non-nullable): The total trading volume
- `circulating_supply` (Float, non-nullable): The circulating supply of XRP
- `total_supply` (Float, non-nullable): The total supply of XRP
- `max_supply` (Float, nullable): The maximum supply of XRP (if applicable)

### Methods

#### __repr__()
Returns a string representation of the MarketData15Min instance.

### Validators

#### validate_price_usd(key, value)
Validates the `price_usd` value, logging a warning if it's negative.

#### validate_market_cap(key, value)
Validates the `market_cap` value, logging a warning if it's negative.

### Event Listeners

The following SQLAlchemy event listeners are defined:

- `after_insert`: Logs info about inserted records
- `after_update`: Logs info about updated records
- `after_delete`: Logs info about deleted records

## Usage

```python
from src.models import MarketData15Min
from datetime import datetime, timezone

# Create a new market data entry
new_data = MarketData15Min(
    timestamp=datetime.now(timezone.utc),
    price_usd=0.5,
    market_cap=1000000000,
    total_volume=500000000,
    circulating_supply=45000000000,
    total_supply=100000000000,
    max_supply=100000000000
)

# Add to session and commit
db.add(new_data)
db.commit()
```
## Notes

- The model uses timezone-aware timestamps.
- Validation is performed on price_usd and market_cap to warn about negative values.
- All database operations (insert, update, delete) are logged using models_logger.
- Make sure to import and use models_logger at the top of the file for logging to work correctly.
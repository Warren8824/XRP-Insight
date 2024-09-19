# ohlcv_data_15_min.py

This file defines the `OHLCVData15Min` model, which represents 15-minute interval OHLCV (Open, High, Low, Close, Volume) data for XRP.

## Class: OHLCVData15Min

Inherits from `Base` (SQLAlchemy declarative base).

### Table Name
`ohlcv_data_15_min`

### Columns

- `timestamp` (DateTime, primary key): The timestamp of the OHLCV data point (timezone-aware)
- `id` (Integer, primary key, indexed): Unique identifier for the record
- `open` (Float, non-nullable): The opening price for the interval
- `high` (Float, non-nullable): The highest price during the interval
- `low` (Float, non-nullable): The lowest price during the interval
- `close` (Float, non-nullable): The closing price for the interval
- `volume` (Float, non-nullable): The trading volume during the interval
- `price_change` (Float, non-nullable): The price change during the interval

### Methods

#### __repr__()
Returns a string representation of the OHLCVData15Min instance.

### Validators

#### validate_fields(key, value)
Validates all fields (`open`, `high`, `low`, `close`, `volume`, `price_change`):
- Checks for negative values and logs a warning if found
- For `high` and `low`, ensures that `high` is not less than `low` and vice versa

### Event Listeners

The following SQLAlchemy event listeners are defined:

- `after_insert`: Logs info about inserted records
- `after_update`: Logs info about updated records
- `after_delete`: Logs info about deleted records

## Usage

```python
from src.models import OHLCVData15Min
from datetime import datetime, timezone

# Create a new OHLCV data entry
new_data = OHLCVData15Min(
    timestamp=datetime.now(timezone.utc),
    open=0.5,
    high=0.55,
    low=0.48,
    close=0.52,
    volume=1000000,
    price_change=0.02
)

# Add to session and commit
db.add(new_data)
db.commit()
```
## Notes

- The model uses timezone-aware timestamps.
- Validation is performed on all fields to warn about negative values and inconsistent high/low values.
- All database operations (insert, update, delete) are logged using models_logger.
- Make sure to import and use models_logger at the top of the file for logging to work correctly.
- Consider adding a CheckConstraint to ensure high >= low at the database level for extra data integrity.
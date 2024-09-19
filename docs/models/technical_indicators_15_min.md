# technical_indicators_15_min.py

This file defines the `TechnicalIndicators15Min` model, which represents 15-minute interval technical indicators for XRP.

## Class: TechnicalIndicators15Min

Inherits from `Base` (SQLAlchemy declarative base).

### Table Name
`technical_indicators_15_min`

### Columns

- `timestamp` (DateTime, primary key): The timestamp of the indicators (timezone-aware)
- `id` (Integer, primary key, indexed): Unique identifier for the record
- `rsi_14` (Float): 14-period Relative Strength Index
- `macd_line` (Float): MACD Line
- `macd_signal` (Float): MACD Signal Line
- `macd_histogram` (Float): MACD Histogram
- `bb_upper` (Float): Upper Bollinger Band
- `bb_middle` (Float): Middle Bollinger Band
- `bb_lower` (Float): Lower Bollinger Band
- `ema_12` (Float): 12-period Exponential Moving Average
- `ema_26` (Float): 26-period Exponential Moving Average
- `sma_50` (Float): 50-period Simple Moving Average
- `sma_200` (Float): 200-period Simple Moving Average

### Methods

#### __repr__()
Returns a string representation of the TechnicalIndicators15Min instance.

### Validators

#### validate_rsi_14(key, value)
Validates the RSI value:
- Checks if the value is between 0 and 100
- Logs a warning if the value is outside this range

#### validate_positive_float(key, value)
Validates that certain indicators are positive:
- Applies to bb_upper, bb_middle, bb_lower, ema_12, ema_26, sma_50, sma_200
- Logs a warning if a negative value is encountered

### Event Listeners

The following SQLAlchemy event listeners are defined:

- `after_insert`: Logs info about inserted records
- `after_update`: Logs info about updated records
- `after_delete`: Logs info about deleted records

## Usage

```python
from src.models import TechnicalIndicators15Min
from datetime import datetime, timezone

# Create a new technical indicators entry
new_indicators = TechnicalIndicators15Min(
    timestamp=datetime.now(timezone.utc),
    rsi_14=65.5,
    macd_line=0.002,
    macd_signal=0.001,
    macd_histogram=0.001,
    bb_upper=0.55,
    bb_middle=0.52,
    bb_lower=0.49,
    ema_12=0.51,
    ema_26=0.52,
    sma_50=0.53,
    sma_200=0.50
)

# Add to session and commit
db.add(new_indicators)
db.commit()
```

## Notes

- The model uses timezone-aware timestamps.
- Validation is performed on RSI to ensure it's within the 0-100 range.
- Validation is performed on several indicators to warn about negative values.
- All database operations (insert, update, delete) are logged using models_logger.
- Make sure to import and use models_logger at the top of the file for logging to work correctly.
- Consider adding additional validations or constraints for other indicators if needed.
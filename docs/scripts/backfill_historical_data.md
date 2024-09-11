# backfill_historical_data.py

This script backfills historical data for the past 90 days.

## Key Operations:

1. Calculates the date range (current date to 90 days ago).
2. Calls the collect_historical_data function to fetch and store historical data.

## Usage:

```python
scripts/backfill_historical_data.py
```

Note: Ensure that the database is properly initialized before running the backfill script.

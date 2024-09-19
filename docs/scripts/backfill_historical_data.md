# backfill_historical_data.py

This script is used to backfill historical data for the XRP Insight project.

## Key Function

### bf_data(start_date, end_date)
Collects historical data for the specified date range and stores it in the database.

## Process

1. Creates a database session
2. Calls `collect_historical_data` function from the collector module
3. Closes the database session after completion

## Usage

When run as a main script, it backfills data for the last 24 hours: `python scripts/backfill_historical_data.py`

## Customization

To backfill data for a different time range, modify the `start_date` calculation in the `__main__` block:

```python
start_date = end_date - timedelta(days=30)  # Change to desired number of days
```

## Notes

- Uses UTC timezone for all dates
- Logs the start and completion of the backfill process
- Ensures proper closure of the database session
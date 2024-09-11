# init_db.py

This script initializes the database for the XRP Insight project.

### Key Operations:

1. Creates the TimescaleDB extension.
2. Creates all tables defined in the models.
3. Converts relevant tables to TimescaleDB hypertables.

### Usage:

```bash
python scripts/init_db.py
```


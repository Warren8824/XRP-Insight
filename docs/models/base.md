# base.py

This file sets up the SQLAlchemy database connection and provides utility functions for database operations.

## Key Components

1. **Database Connection**
   - Uses the database URL from the config file
   - Creates a SQLAlchemy engine and session factory

2. **Base Declarative Class**
   - `Base = declarative_base()`: Used as the base class for all SQLAlchemy models

3. **TimescaleDB Support**
   - Custom compiler for CreateTable to support TimescaleDB hypertables

4. **Database Session Management**
   - `get_db()`: A generator function that yields a database session and ensures it's closed after use

5. **Database Initialization**
   - `init_db()`: Initializes the database, creates all tables, and sets up the TimescaleDB extension

## Functions

### get_db()
Yields a database session and ensures it's properly closed.

### init_db()
Initializes the database by creating all tables and setting up the TimescaleDB extension.

## Usage

```python
from src.models.base import get_db, init_db

# Initialize the database
init_db()

# Use the database session
db = next(get_db())
try:
    # Perform database operations
    ...
finally:
    db.close()
```

## Notes

1. The file uses `models_logger` for logging database operations and errors.
2. It supports TimescaleDB hypertables through a custom SQLAlchemy compiler.
3. Error handling is implemented to catch and log any exceptions during database operations.
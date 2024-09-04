# Base Model Documentation

## Overview

This document outlines the base configuration for database models in the XRP Market Bot project. The `base.py` script sets up the SQLAlchemy ORM (Object-Relational Mapping) and provides the foundation for all database models used in the application.

## Components

1. **Database Configuration**: Retrieves database settings from the project configuration.
2. **SQLAlchemy Engine**: Creates the database engine for SQLite.
3. **Session Factory**: Sets up a factory for creating database sessions.
4. **Declarative Base**: Provides a base class for declarative class definitions.
5. **Database Session Generator**: A function to yield database sessions.

## Implementation Details

### Database Configuration

The script retrieves the database name and path from the project configuration:

```python
db_name = config['database']['name']
db_path = config['database']['path']
```

It then constructs the full path to the database file:

```python
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
full_db_path = os.path.join(project_root, db_path, db_name)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{full_db_path}"
```

### SQLAlchemy Engine

The database engine is created with SQLite-specific configuration:

```python
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
```

The `check_same_thread=False` argument is used to allow SQLite to work with multiple threads, which is necessary for web applications.

### Session Factory

A session factory is created to generate new database sessions:

```python
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### Declarative Base

A declarative base class is created, which will be used as the base for all model classes:

```python
Base = declarative_base()
```

### Database Session Generator

A generator function is provided to yield database sessions:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

This function ensures that the database session is properly closed after use, even if an exception occurs.

## Usage

### Defining Models

To define a new model, create a new class that inherits from `Base`:

```python
from .base import Base
from sqlalchemy import Column, Integer, String

class YourModel(Base):
    __tablename__ = "your_table_name"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # Add more columns as needed
```

### Using Database Sessions

To use a database session in your application code:

```python
from .base import get_db

def some_function():
    db = next(get_db())
    try:
        # Perform database operations
        result = db.query(YourModel).filter(YourModel.name == "example").first()
        # ...
    finally:
        db.close()
```

## Best Practices

1. Always use the `get_db()` function to obtain a database session, ensuring proper resource management.
2. Keep the `base.py` file focused on database configuration and avoid adding application-specific logic to it.
3. When defining new models, import `Base` from this module to ensure consistency across all models.
4. If you need to modify the database configuration, update the `config.yaml` file rather than changing this script directly.

## Customization

To modify the database configuration:

1. Update the database settings in `config.yaml`.
2. If switching to a different database system (e.g., PostgreSQL), modify the `create_engine()` call and update the `SQLALCHEMY_DATABASE_URL` accordingly.

---

For any questions or issues regarding the database configuration or ORM setup, please contact the project maintainer.
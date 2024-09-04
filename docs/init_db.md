# Database Initialization Script Documentation

## Overview

This document outlines the database initialization script (`init_db.py`) for the XRP Market Bot project. This script is responsible for creating all the necessary database tables based on the defined SQLAlchemy models.

## Script Location

The `init_db.py` script is located in the `scripts/` directory of the project.

## Script Content

```python
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.models.base import Base, engine
from src.models.market_data import MarketData

# Import other models as needed, for example:
# from src.models.on_chain_data import OnChainData
# from src.models.social_sentiment import SocialSentiment
# from src.models.news_data import NewsData

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    init_db()
```

## Functionality

The `init_db.py` script performs the following tasks:

1. Adds the project root directory to the Python path to ensure all project modules can be imported correctly.
2. Imports the necessary components from the project's model files:
   - `Base` and `engine` from `src.models.base`
   - `MarketData` from `src.models.market_data`
3. Defines an `init_db()` function that creates all database tables based on the imported models.
4. Provides a main block to run the `init_db()` function when the script is executed directly.

## Usage

To initialize the database and create all tables, run the following command from the project root directory:

```
python scripts/init_db.py
```

This will create all the necessary tables in the database specified in your configuration.

## Adding New Models

When you create a new model, follow these steps to ensure it's included in the database initialization:

1. Create your new model file in the `src/models/` directory (e.g., `src/models/new_model.py`).
2. In `init_db.py`, import your new model:
   ```python
   from src.models.new_model import NewModel
   ```
3. There's no need to modify the `init_db()` function, as it will automatically create tables for all models that inherit from `Base`.

## Best Practices

1. Always run this script after setting up a new development environment or when deploying to a new server.
2. Run this script after adding new models or making changes to existing models.
3. In a production environment, consider using database migration tools (like Alembic) for managing schema changes instead of recreating all tables.
4. Keep this script updated with all your models to ensure a complete database setup.

## Troubleshooting

If you encounter any issues while running the script:

1. Ensure that your database configuration in `config.yaml` is correct.
2. Check that all model files are correctly imported and there are no syntax errors.
3. Verify that you have the necessary permissions to create tables in the specified database.

---

For any questions or issues regarding the database initialization script, please contact the project maintainer.
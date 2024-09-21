from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.ddl import CreateTable

from src.utils.config import config
from src.utils.logger import models_logger

# Config settings
SQLALCHEMY_DATABASE_URL = config["database"]["url"]

# SQLAlchemy engine and session creation
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarative class for models
Base = declarative_base()


# This is to support TimescaleDB hypertables
@compiles(CreateTable, "postgresql")
def compile_create_table(element, compiler, **kw):
    table = element.element
    if table.info.get("is_hypertable", False):
        models_logger.info(
            f"Creating hypertable for table {table.name} with interval {table.info['hypertable_interval']}"
        )
        return f"{compiler.visit_create_table(element)} WITH (hypertable_interval = '{table.info['hypertable_interval']}')"
    models_logger.info(f"Creating regular table {table.name}")
    return compiler.visit_create_table(element)


def get_db():
    db = SessionLocal()
    models_logger.info("Database session started")
    try:
        yield db
    except Exception as e:
        models_logger.error(f"An error occurred with the DB session: {str(e)}")
        raise
    finally:
        db.close()
        models_logger.info("Database session closed")


def init_db():
    try:
        models_logger.info("Starting database initialization...")
        Base.metadata.create_all(bind=engine)
        models_logger.info("All tables created successfully")

        # Create TimescaleDB extension
        with engine.connect() as conn:
            conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb")
            models_logger.info(
                "TimescaleDB extension created (if it didn't already exist)"
            )

    except Exception as e:
        models_logger.error(f"Error during database initialization: {str(e)}")
        raise

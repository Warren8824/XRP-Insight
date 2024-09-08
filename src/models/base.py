from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.ddl import CreateTable

from src.utils.config import config

SQLALCHEMY_DATABASE_URL = config['database']['url']

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# This is to support TimescaleDB hypertables
@compiles(CreateTable, "postgresql")
def compile_create_table(element, compiler, **kw):
    table = element.element
    if table.info.get("is_hypertable", False):
        return f"{compiler.visit_create_table(element)} WITH (hypertable_interval = '{table.info['hypertable_interval']}')"
    return compiler.visit_create_table(element)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)

    # Create TimescaleDB extension
    with engine.connect() as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb")

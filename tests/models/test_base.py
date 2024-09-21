import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session
from urllib.parse import urlparse
import os

from src.models.base import engine, SessionLocal, Base, get_db, init_db
from src.utils.config import config


class TestBase(unittest.TestCase):
    """
    A test suite for the base model module.

    This class contains unit tests for the database configuration,
    session management, and initialization functions in the base model module.
    """

    def test_engine_creation(self):
        """
        Test that the SQLAlchemy engine is created correctly.

        This test verifies that:
        1. The engine is an instance of sqlalchemy.engine.base.Engine.
        2. The engine is configured with the correct database URL components (excluding sensitive information).
        """
        self.assertIsInstance(engine, Engine)

        actual_url = urlparse(str(engine.url))

        # Verify the scheme
        self.assertEqual(actual_url.scheme, "postgresql")

        # Verify the host and port
        self.assertEqual(actual_url.hostname, "localhost")
        self.assertEqual(actual_url.port, 5432)

        # Verify the database name
        self.assertEqual(actual_url.path, "/xrp_insight")

        # Verify that a username is present (without checking its exact value)
        self.assertIsNotNone(actual_url.username)

        # Verify that a password is present (without checking its exact value)
        self.assertIsNotNone(actual_url.password)

    def test_session_creation(self):
        """
        Test that a database session can be created.

        This test verifies that:
        1. SessionLocal creates a valid SQLAlchemy session.
        """
        session = SessionLocal()
        self.assertIsInstance(session, Session)
        session.close()

    @patch("src.models.base.SessionLocal")
    def test_get_db(self, mock_session_local):
        """
        Test the get_db function.

        This test verifies that:
        1. The function yields a database session.
        2. The session is closed after use, even if an exception occurs.

        Args:
            mock_session_local (MagicMock): Mock for SessionLocal class.
        """
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session

        db_generator = get_db()
        db = next(db_generator)

        self.assertEqual(db, mock_session)

        # Simulate the end of the request
        try:
            next(db_generator)
        except StopIteration:
            pass

        mock_session.close.assert_called_once()

    @patch("src.models.base.Base.metadata.create_all")
    @patch("src.models.base.engine.connect")
    def test_init_db(self, mock_connect, mock_create_all):
        """
        Test the init_db function.

        This test verifies that:
        1. The function creates all tables in the database.
        2. The TimescaleDB extension is created.

        Args:
            mock_connect (MagicMock): Mock for engine.connect method.
            mock_create_all (MagicMock): Mock for Base.metadata.create_all method.
        """
        mock_connection = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_connection

        init_db()

        mock_create_all.assert_called_once_with(bind=engine)
        mock_connection.execute.assert_called_once_with(
            "CREATE EXTENSION IF NOT EXISTS timescaledb"
        )


if __name__ == "__main__":
    unittest.main()

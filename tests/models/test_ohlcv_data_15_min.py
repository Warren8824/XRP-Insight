import unittest
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from src.models import get_models, models_logger
from src.models.base import Base, engine

# Get the models
models = get_models()
OHLCVData15Min = models["OHLCVData15Min"]


class TestOHLCVData15Min(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test database and session."""
        cls.Session = sessionmaker(bind=engine)
        cls.engine = engine

    def setUp(self):
        """Create a new session for each test."""
        self.session = self.Session()
        self.session.begin_nested()  # Start a savepoint

    def tearDown(self):
        """Rollback to the savepoint and close the session after each test."""
        self.session.rollback()  # Rollback to the savepoint
        self.session.close()

    @classmethod
    def tearDownClass(cls):
        """Clean up all test data after all tests are done."""
        session = cls.Session()
        try:
            # Delete all data inserted during the tests
            session.query(OHLCVData15Min).delete()
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            models_logger.error(f"Error during test data cleanup: {str(e)}")
        except Exception as e:
            session.rollback()
            models_logger.error(f"Unexpected error during test data cleanup: {str(e)}")
        finally:
            session.close()

    def test_ohlcv_data_creation(self):
        ohlcv_data = OHLCVData15Min(
            id=1,  # Explicitly set the ID
            timestamp=datetime.now(),
            open=100.0,
            high=110.0,
            low=90.0,
            close=105.0,
            volume=1000000.0,
            trades_count=20,
            price_change=5.0,
        )
        self.session.add(ohlcv_data)
        self.session.flush()  # Flush to get the ID, but don't commit

        retrieved_data = self.session.query(OHLCVData15Min).filter_by(id=1).first()
        self.assertIsNotNone(retrieved_data)
        self.assertEqual(retrieved_data.open, 100.0)
        self.assertEqual(retrieved_data.close, 105.0)

    def test_negative_value_validation(self):
        with self.assertLogs(models_logger, level="WARNING") as cm:
            ohlcv_data = OHLCVData15Min(
                id=2,  # Explicitly set the ID
                timestamp=datetime.now(),
                open=-100.0,
                high=-90.0,
                low=-110.0,
                close=-105.0,
                volume=-1000000.0,
                price_change=-5.0,
                trades_count=22,
            )
            self.session.add(ohlcv_data)
            self.session.flush()  # Flush to trigger SQL, but don't commit

        self.assertEqual(len(cm.output), 5)  # 5 warnings for 5 negative values
        self.assertIn("Attempted to set negative open: -100.0", cm.output[0])
        self.assertIn("Attempted to set negative high: -90.0", cm.output[1])
        self.assertIn("Attempted to set negative low: -110.0", cm.output[2])
        self.assertIn("Attempted to set negative close: -105.0", cm.output[3])
        self.assertIn("Attempted to set negative volume: -1000000.0", cm.output[4])

        retrieved_data = self.session.query(OHLCVData15Min).filter_by(id=2).first()
        self.assertEqual(retrieved_data.open, -100.0)
        self.assertEqual(retrieved_data.volume, -1000000.0)

    def test_high_low_validation(self):
        with self.assertLogs(models_logger, level="WARNING") as cm:
            ohlcv_data = OHLCVData15Min(
                id=3,  # Explicitly set the ID
                timestamp=datetime.now(),
                open=100.0,
                low=110.0,
                high=90.0,  # High less than low
                close=105.0,
                volume=1000000.0,
                price_change=5.0,
                trades_count=200,
            )
            self.session.add(ohlcv_data)
            self.session.flush()  # Flush to trigger SQL, but don't commit

        self.assertIn("High value 90.0 is less than low value 110.0", cm.output[0])

        retrieved_data = self.session.query(OHLCVData15Min).filter_by(id=3).first()
        self.assertEqual(retrieved_data.high, 90.0)
        self.assertEqual(retrieved_data.low, 110.0)


if __name__ == "__main__":
    unittest.main()

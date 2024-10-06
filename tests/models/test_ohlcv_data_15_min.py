import unittest
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from src.models import get_models, models_logger
from src.models.base import Base, engine

# Get the models
models = get_models()
OHLCVData15Min = models["OHLCVData15Min"]


class TestOHLCVData15Min(unittest.TestCase):
    """
    A test suite for the OHLCVData15Min model.

    This class contains unit tests for the OHLCVData15Min model,
    including its initialization, validation, and event listeners.
    """

    @classmethod
    def setUpClass(cls):
        """Set up the test database and session."""
        Base.metadata.create_all(engine)
        cls.Session = sessionmaker(bind=engine)

    def setUp(self):
        """Create a new session and begin a nested transaction for each test."""
        self.session = self.Session()
        # Start a new transaction for the test case
        self.transaction = self.session.begin_nested()

    def tearDown(self):
        """Rollback the nested transaction and close the session after each test."""
        if self.transaction.is_active:
            self.transaction.rollback()  # Rollback only if the transaction is still active
        self.session.close()  # Close the session

    def test_ohlcv_data_creation(self):
        """
        Test the creation of an OHLCVData15Min instance.

        This test verifies that:
        1. An OHLCVData15Min instance can be created with valid data.
        2. The instance can be added to the session and committed to the database.
        3. The data can be retrieved from the database correctly.
        """
        ohlcv_data = OHLCVData15Min(
            timestamp=datetime.now(),
            id=1,
            open=100.0,
            high=110.0,
            low=90.0,
            close=105.0,
            volume=1000000.0,
            price_change=5.0,
        )
        self.session.add(ohlcv_data)
        self.session.commit()

        retrieved_data = self.session.query(OHLCVData15Min).filter_by(id=1).first()
        self.assertIsNotNone(retrieved_data)
        self.assertEqual(retrieved_data.open, 100.0)
        self.assertEqual(retrieved_data.close, 105.0)

    def test_negative_value_validation(self):
        """
        Test the validation of negative values.

        This test verifies that:
        1. A warning is logged when attempting to set negative values for any field except price change.
        2. The negative values are still set (as per the current implementation).
        """
        with self.assertLogs(models_logger, level="WARNING") as cm:
            ohlcv_data = OHLCVData15Min(
                timestamp=datetime.now(),
                id=2,
                open=-100.0,
                high=-90.0,
                low=-110.0,
                close=-105.0,
                volume=-1000000.0,
                price_change=-5.0,
            )
            self.session.add(ohlcv_data)
            self.session.commit()

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
        """
        Test the validation of high and low values.

        This test verifies that:
        1. A warning is logged when the high value is less than the low value.
        2. The values are still set (as per the current implementation).
        """
        with self.assertLogs(models_logger, level="WARNING") as cm:
            ohlcv_data = OHLCVData15Min(
                timestamp=datetime.now(),
                id=3,
                open=100.0,
                low=110.0,
                high=90.0,  # High less than low
                close=105.0,
                volume=1000000.0,
                price_change=5.0,
            )
            self.session.add(ohlcv_data)
            self.session.commit()

        self.assertIn("High value 90.0 is less than low value 110.0", cm.output[0])

        retrieved_data = self.session.query(OHLCVData15Min).filter_by(id=3).first()
        self.assertEqual(retrieved_data.high, 90.0)
        self.assertEqual(retrieved_data.low, 110.0)


if __name__ == "__main__":
    unittest.main()

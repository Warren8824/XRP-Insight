import unittest
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from src.models.technical_indicators_15_min import TechnicalIndicators15Min
from src.models.base import Base, engine
from src.models import models_logger

class TestTechnicalIndicators15Min(unittest.TestCase):
    """
    A test suite for the TechnicalIndicators15Min model.

    This class contains unit tests for the TechnicalIndicators15Min model,
    including its initialization, validation, and event listeners.
    """

    @classmethod
    def setUpClass(cls):
        """Set up the test database and session."""
        Base.metadata.create_all(engine)
        cls.Session = sessionmaker(bind=engine)

    def setUp(self):
        """Create a new session for each test."""
        self.session = self.Session()

    def tearDown(self):
        """Close the session after each test."""
        self.session.rollback()
        self.session.close()

    def test_technical_indicators_creation(self):
        """
        Test the creation of a TechnicalIndicators15Min instance.

        This test verifies that:
        1. A TechnicalIndicators15Min instance can be created with valid data.
        2. The instance can be added to the session and committed to the database.
        3. The data can be retrieved from the database correctly.
        """
        indicators = TechnicalIndicators15Min(
            timestamp=datetime.now(),
            id=1,
            rsi_14=50.0,
            macd_line=0.5,
            macd_signal=0.3,
            macd_histogram=0.2,
            bb_upper=110.0,
            bb_middle=100.0,
            bb_lower=90.0,
            ema_12=105.0,
            ema_26=98.0,
            sma_50=102.0,
            sma_200=95.0
        )
        self.session.add(indicators)
        self.session.commit()

        retrieved_data = self.session.query(TechnicalIndicators15Min).filter_by(id=1).first()
        self.assertIsNotNone(retrieved_data)
        self.assertEqual(retrieved_data.rsi_14, 50.0)
        self.assertEqual(retrieved_data.macd_line, 0.5)

    def test_rsi_validation(self):
        """
        Test the validation of the RSI field.

        This test verifies that:
        1. A warning is logged when attempting to set an RSI value outside the 0-100 range.
        2. The invalid value is still set (as per the current implementation).
        """
        with self.assertLogs(models_logger, level='WARNING') as cm:
            indicators = TechnicalIndicators15Min(
                timestamp=datetime.now(),
                id=2,
                rsi_14=150.0,  # Invalid RSI value
                macd_line=0.5,
                macd_signal=0.3,
                macd_histogram=0.2,
                bb_upper=110.0,
                bb_middle=100.0,
                bb_lower=90.0,
                ema_12=105.0,
                ema_26=98.0,
                sma_50=102.0,
                sma_200=95.0
            )
            self.session.add(indicators)
            self.session.commit()

        self.assertIn("Invalid RSI value: 150.0", cm.output[0])

        retrieved_data = self.session.query(TechnicalIndicators15Min).filter_by(id=2).first()
        self.assertEqual(retrieved_data.rsi_14, 150.0)

    def test_negative_value_validation(self):
        """
        Test the validation of negative values for certain fields.

        This test verifies that:
        1. A warning is logged when attempting to set negative values for fields that should be positive.
        2. The negative values are still set (as per the current implementation).
        """
        with self.assertLogs(models_logger, level='WARNING') as cm:
            indicators = TechnicalIndicators15Min(
                timestamp=datetime.now(),
                id=3,
                rsi_14=50.0,
                macd_line=0.5,
                macd_signal=0.3,
                macd_histogram=0.2,
                bb_upper=-110.0,  # Negative value
                bb_middle=-100.0,  # Negative value
                bb_lower=-90.0,   # Negative value
                ema_12=-105.0,    # Negative value
                ema_26=-98.0,     # Negative value
                sma_50=-102.0,    # Negative value
                sma_200=-95.0     # Negative value
            )
            self.session.add(indicators)
            self.session.commit()

        self.assertIn("Negative value for bb_upper: -110.0", cm.output[0])
        self.assertIn("Negative value for bb_middle: -100.0", cm.output[1])
        self.assertIn("Negative value for bb_lower: -90.0", cm.output[2])
        self.assertIn("Negative value for ema_12: -105.0", cm.output[3])
        self.assertIn("Negative value for ema_26: -98.0", cm.output[4])
        self.assertIn("Negative value for sma_50: -102.0", cm.output[5])
        self.assertIn("Negative value for sma_200: -95.0", cm.output[6])

        retrieved_data = self.session.query(TechnicalIndicators15Min).filter_by(id=3).first()
        self.assertEqual(retrieved_data.bb_upper, -110.0)
        self.assertEqual(retrieved_data.ema_12, -105.0)

if __name__ == '__main__':
    unittest.main()
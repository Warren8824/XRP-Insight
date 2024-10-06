import unittest
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from src.models.technical_indicators_15_min import TechnicalIndicators15Min
from src.models.base import Base, engine
from src.models import models_logger


class TestTechnicalIndicators15Min(unittest.TestCase):
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
            session.query(TechnicalIndicators15Min).delete()
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            models_logger.error(f"Error during test data cleanup: {str(e)}")
        except Exception as e:
            session.rollback()
            models_logger.error(f"Unexpected error during test data cleanup: {str(e)}")
        finally:
            session.close()

    def test_technical_indicators_creation(self):
        indicators = TechnicalIndicators15Min(
            id=1,  # Explicitly set the ID
            timestamp=datetime.now(),
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
            sma_200=95.0,
        )
        self.session.add(indicators)
        self.session.flush()  # Flush to get the ID, but don't commit

        retrieved_data = (
            self.session.query(TechnicalIndicators15Min).filter_by(id=1).first()
        )
        self.assertIsNotNone(retrieved_data)
        self.assertEqual(retrieved_data.rsi_14, 50.0)
        self.assertEqual(retrieved_data.macd_line, 0.5)

    def test_rsi_validation(self):
        with self.assertLogs(models_logger, level="WARNING") as cm:
            indicators = TechnicalIndicators15Min(
                id=2,  # Explicitly set the ID
                timestamp=datetime.now(),
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
                sma_200=95.0,
            )
            self.session.add(indicators)
            self.session.flush()  # Flush to trigger SQL, but don't commit

        self.assertIn("Invalid RSI value: 150.0", cm.output[0])
        retrieved_data = (
            self.session.query(TechnicalIndicators15Min).filter_by(id=2).first()
        )
        self.assertEqual(retrieved_data.rsi_14, 150.0)

    def test_negative_value_validation(self):
        with self.assertLogs(models_logger, level="WARNING") as cm:
            indicators = TechnicalIndicators15Min(
                id=3,  # Explicitly set the ID
                timestamp=datetime.now(),
                rsi_14=50.0,
                macd_line=0.5,
                macd_signal=0.3,
                macd_histogram=0.2,
                bb_upper=-110.0,  # Negative value
                bb_middle=-100.0,  # Negative value
                bb_lower=-90.0,  # Negative value
                ema_12=-105.0,  # Negative value
                ema_26=-98.0,  # Negative value
                sma_50=-102.0,  # Negative value
                sma_200=-95.0,  # Negative value
            )
            self.session.add(indicators)
            self.session.flush()  # Flush to trigger SQL, but don't commit

        self.assertIn("Negative value for bb_upper: -110.0", cm.output[0])
        self.assertIn("Negative value for bb_middle: -100.0", cm.output[1])
        self.assertIn("Negative value for bb_lower: -90.0", cm.output[2])
        self.assertIn("Negative value for ema_12: -105.0", cm.output[3])
        self.assertIn("Negative value for ema_26: -98.0", cm.output[4])
        self.assertIn("Negative value for sma_50: -102.0", cm.output[5])
        self.assertIn("Negative value for sma_200: -95.0", cm.output[6])

        retrieved_data = (
            self.session.query(TechnicalIndicators15Min).filter_by(id=3).first()
        )
        self.assertEqual(retrieved_data.bb_upper, -110.0)
        self.assertEqual(retrieved_data.ema_12, -105.0)


if __name__ == "__main__":
    unittest.main()

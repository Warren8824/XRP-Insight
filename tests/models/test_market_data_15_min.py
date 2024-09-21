import unittest
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from src.models.market_data_15_min import MarketData15Min
from src.models.base import Base, engine
from src.models import models_logger  # Change this line

class TestMarketData15Min(unittest.TestCase):
    """
    A test suite for the MarketData15Min model.

    This class contains unit tests for the MarketData15Min model,
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

    def test_market_data_creation(self):
        """
        Test the creation of a MarketData15Min instance.

        This test verifies that:
        1. A MarketData15Min instance can be created with valid data.
        2. The instance can be added to the session and committed to the database.
        3. The data can be retrieved from the database correctly.
        """
        market_data = MarketData15Min(
            timestamp=datetime.now(),
            id=1,
            price_usd=100.0,
            market_cap=1000000.0,
            total_volume=500000.0,
            circulating_supply=1000000.0,
            total_supply=2000000.0,
            max_supply=3000000.0
        )
        self.session.add(market_data)
        self.session.commit()

        retrieved_data = self.session.query(MarketData15Min).filter_by(id=1).first()
        self.assertIsNotNone(retrieved_data)
        self.assertEqual(retrieved_data.price_usd, 100.0)
        self.assertEqual(retrieved_data.market_cap, 1000000.0)

    def test_price_usd_validation(self):
        """
        Test the validation of the price_usd field.

        This test verifies that:
        1. A warning is logged when attempting to set a negative price_usd.
        2. The negative value is still set (as per the current implementation).
        """
        with self.assertLogs(models_logger, level='WARNING') as cm:
            market_data = MarketData15Min(
                timestamp=datetime.now(),
                id=2,
                price_usd=-100.0,
                market_cap=1000000.0,
                total_volume=500000.0,
                circulating_supply=1000000.0,
                total_supply=2000000.0
            )
            self.session.add(market_data)
            self.session.commit()

        self.assertIn("Attempted to set negative price_usd: -100.0", cm.output[0])
        retrieved_data = self.session.query(MarketData15Min).filter_by(id=2).first()
        self.assertEqual(retrieved_data.price_usd, -100.0)

    def test_market_cap_validation(self):
        """
        Test the validation of the market_cap field.

        This test verifies that:
        1. A warning is logged when attempting to set a negative market_cap.
        2. The negative value is still set (as per the current implementation).
        """
        with self.assertLogs(models_logger, level='WARNING') as cm:
            market_data = MarketData15Min(
                timestamp=datetime.now(),
                id=3,
                price_usd=100.0,
                market_cap=-1000000.0,
                total_volume=500000.0,
                circulating_supply=1000000.0,
                total_supply=2000000.0
            )
            self.session.add(market_data)
            self.session.commit()

        self.assertIn("Attempted to set negative market_cap: -1000000.0", cm.output[0])
        retrieved_data = self.session.query(MarketData15Min).filter_by(id=3).first()
        self.assertEqual(retrieved_data.market_cap, -1000000.0)

if __name__ == '__main__':
    unittest.main()
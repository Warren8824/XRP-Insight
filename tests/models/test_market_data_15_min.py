from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

import unittest
from datetime import datetime

from src.models.market_data_15_min import MarketData15Min
from src.models.base import Base, engine
from src.models import models_logger


class TestMarketData15Min(unittest.TestCase):
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
            session.query(MarketData15Min).delete()
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            models_logger.error(f"Error during test data cleanup: {str(e)}")
        except Exception as e:
            session.rollback()
            models_logger.error(f"Unexpected error during test data cleanup: {str(e)}")
        finally:
            session.close()

    def test_market_data_creation(self):
        market_data = MarketData15Min(
            id=1,
            timestamp=datetime.now(),
            price_usd=100.0,
            market_cap=1000000.0,
            total_volume=500000.0,
            circulating_supply=1000000.0,
            total_supply=2000000.0,
            max_supply=3000000.0,
        )
        self.session.add(market_data)
        self.session.flush()  # Flush to get the ID, but don't commit

        retrieved_data = self.session.query(MarketData15Min).filter_by(id=market_data.id).first()
        self.assertIsNotNone(retrieved_data)
        self.assertEqual(retrieved_data.price_usd, 100.0)
        self.assertEqual(retrieved_data.market_cap, 1000000.0)
        self.assertEqual(retrieved_data.max_supply, 3000000.0)

    def test_price_usd_validation(self):
        with self.assertLogs(models_logger, level="WARNING") as cm:
            market_data = MarketData15Min(
                id=2,
                timestamp=datetime.now(),
                price_usd=-100.0,
                market_cap=1000000.0,
                total_volume=500000.0,
                circulating_supply=1000000.0,
                total_supply=2000000.0,
            )
            self.session.add(market_data)
            self.session.flush()  # Flush to trigger SQL, but don't commit

        self.assertIn("Attempted to set negative price_usd: -100.0", cm.output[0])
        retrieved_data = self.session.query(MarketData15Min).filter_by(id=market_data.id).first()
        self.assertEqual(retrieved_data.price_usd, -100.0)

    def test_market_cap_validation(self):
        with self.assertLogs(models_logger, level="WARNING") as cm:
            market_data = MarketData15Min(
                id=3,
                timestamp=datetime.now(),
                price_usd=100.0,
                market_cap=-1000000.0,
                total_volume=500000.0,
                circulating_supply=1000000.0,
                total_supply=2000000.0,
            )
            self.session.add(market_data)
            self.session.flush()  # Flush to trigger SQL, but don't commit

        self.assertIn("Attempted to set negative market_cap: -1000000.0", cm.output[0])
        retrieved_data = self.session.query(MarketData15Min).filter_by(id=market_data.id).first()
        self.assertEqual(retrieved_data.market_cap, -1000000.0)


if __name__ == "__main__":
    unittest.main()

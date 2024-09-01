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
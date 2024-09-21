from src.utils.logger import models_logger


# Don't import the models directly here
# Instead, we'll use a function to import them when needed

def get_models():
    from .base import Base
    from .market_data_15_min import MarketData15Min
    from .ohlcv_data_15_min import OHLCVData15Min
    from .technical_indicators_15_min import TechnicalIndicators15Min

    return {
        'Base': Base,
        'MarketData15Min': MarketData15Min,
        'OHLCVData15Min': OHLCVData15Min,
        'TechnicalIndicators15Min': TechnicalIndicators15Min
    }


__all__ = ['models_logger', 'get_models']
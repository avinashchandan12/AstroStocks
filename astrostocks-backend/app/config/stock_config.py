"""
Stock Configuration Module
Manages tracked stock symbols and market data settings
"""
import os
from typing import List


def get_tracked_stocks() -> List[str]:
    """
    Get list of stocks to track from environment variable
    
    Returns:
        List of stock symbols (without exchange suffix)
    """
    stocks_str = os.getenv(
        "NSE_STOCKS", 
        "RELIANCE,TCS,HDFCBANK,INFY,TATASTEEL,SUNPHARMA,ITC,HINDUNILVR,SBIN,BAJFINANCE"
    )
    return [s.strip() for s in stocks_str.split(",") if s.strip()]


def get_cache_ttl_hours() -> int:
    """Get cache TTL in hours from environment"""
    return int(os.getenv("MARKET_DATA_CACHE_TTL_HOURS", "1"))


def use_real_market_data() -> bool:
    """Check if real market data should be used"""
    return os.getenv("USE_REAL_MARKET_DATA", "true").lower() == "true"


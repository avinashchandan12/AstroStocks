"""
Mock Data Generator for Testing
Provides sample stock and planetary transit data
Can use real ephemeris data when available
"""
from datetime import date, datetime
from typing import List, Dict, Any, Optional
import os

# Try to import ephemeris service
try:
    from app.services.ephemeris_service import get_planetary_transits as get_real_transits, SWISSEPH_AVAILABLE
except ImportError:
    SWISSEPH_AVAILABLE = False
    get_real_transits = None


def get_mock_stock_data() -> List[Dict[str, Any]]:
    """Generate mock stock market data across various sectors"""
    return [
        {
            "symbol": "TATACHEM",
            "sector": "Chemicals",
            "past_6m_return": 15.5,
            "volatility": "Medium",
            "pe_ratio": 18.5,
            "price_trend": "Upward",
            "news_sentiment": "Positive"
        },
        {
            "symbol": "UPL",
            "sector": "Chemicals",
            "past_6m_return": 12.3,
            "volatility": "High",
            "pe_ratio": 22.1,
            "price_trend": "Sideways",
            "news_sentiment": "Neutral"
        },
        {
            "symbol": "TCS",
            "sector": "Technology",
            "past_6m_return": 8.7,
            "volatility": "Low",
            "pe_ratio": 28.3,
            "price_trend": "Upward",
            "news_sentiment": "Positive"
        },
        {
            "symbol": "INFY",
            "sector": "Technology",
            "past_6m_return": 6.5,
            "volatility": "Low",
            "pe_ratio": 25.6,
            "price_trend": "Upward",
            "news_sentiment": "Positive"
        },
        {
            "symbol": "HDFCBANK",
            "sector": "Banking",
            "past_6m_return": 10.2,
            "volatility": "Medium",
            "pe_ratio": 19.8,
            "price_trend": "Upward",
            "news_sentiment": "Positive"
        },
        {
            "symbol": "ICICIBANK",
            "sector": "Banking",
            "past_6m_return": 14.8,
            "volatility": "Medium",
            "pe_ratio": 17.5,
            "price_trend": "Upward",
            "news_sentiment": "Very Positive"
        },
        {
            "symbol": "RELIANCE",
            "sector": "Oil & Gas",
            "past_6m_return": 5.3,
            "volatility": "Medium",
            "pe_ratio": 24.2,
            "price_trend": "Sideways",
            "news_sentiment": "Neutral"
        },
        {
            "symbol": "ONGC",
            "sector": "Oil & Gas",
            "past_6m_return": -2.1,
            "volatility": "High",
            "pe_ratio": 8.5,
            "price_trend": "Downward",
            "news_sentiment": "Negative"
        },
        {
            "symbol": "SUNPHARMA",
            "sector": "Pharmaceuticals",
            "past_6m_return": 18.9,
            "volatility": "Medium",
            "pe_ratio": 32.4,
            "price_trend": "Upward",
            "news_sentiment": "Very Positive"
        },
        {
            "symbol": "DRREDDY",
            "sector": "Pharmaceuticals",
            "past_6m_return": 11.2,
            "volatility": "Low",
            "pe_ratio": 28.7,
            "price_trend": "Upward",
            "news_sentiment": "Positive"
        },
        {
            "symbol": "MARUTI",
            "sector": "Automotive",
            "past_6m_return": 9.8,
            "volatility": "Medium",
            "pe_ratio": 26.3,
            "price_trend": "Upward",
            "news_sentiment": "Positive"
        },
        {
            "symbol": "TATASTEEL",
            "sector": "Iron & Steel",
            "past_6m_return": 3.2,
            "volatility": "High",
            "pe_ratio": 12.1,
            "price_trend": "Sideways",
            "news_sentiment": "Neutral"
        },
        {
            "symbol": "DLF",
            "sector": "Real Estate",
            "past_6m_return": 22.5,
            "volatility": "High",
            "pe_ratio": 45.2,
            "price_trend": "Upward",
            "news_sentiment": "Very Positive"
        },
        {
            "symbol": "BHARTIARTL",
            "sector": "Telecom",
            "past_6m_return": 7.4,
            "volatility": "Medium",
            "pe_ratio": 35.8,
            "price_trend": "Upward",
            "news_sentiment": "Positive"
        },
        {
            "symbol": "ITC",
            "sector": "FMCG",
            "past_6m_return": 4.5,
            "volatility": "Low",
            "pe_ratio": 22.9,
            "price_trend": "Sideways",
            "news_sentiment": "Neutral"
        }
    ]


def get_mock_planetary_transits_static() -> List[Dict[str, Any]]:
    """Generate mock planetary transit data (static fallback)"""
    today = date.today()
    
    return [
        {
            "planet": "Jupiter",
            "sign": "Taurus",
            "motion": "Direct",
            "status": "Normal",
            "date": today.isoformat()
        },
        {
            "planet": "Saturn",
            "sign": "Aquarius",
            "motion": "Direct",
            "status": "Normal",
            "date": today.isoformat()
        },
        {
            "planet": "Mars",
            "sign": "Capricorn",
            "motion": "Direct",
            "status": "Exalted",
            "date": today.isoformat()
        },
        {
            "planet": "Venus",
            "sign": "Pisces",
            "motion": "Direct",
            "status": "Exalted",
            "date": today.isoformat()
        },
        {
            "planet": "Mercury",
            "sign": "Virgo",
            "motion": "Direct",
            "status": "Exalted",
            "date": today.isoformat()
        },
        {
            "planet": "Sun",
            "sign": "Aries",
            "motion": "Direct",
            "status": "Exalted",
            "date": today.isoformat()
        },
        {
            "planet": "Moon",
            "sign": "Cancer",
            "motion": "Direct",
            "status": "Normal",
            "date": today.isoformat()
        },
        {
            "planet": "Rahu",
            "sign": "Pisces",
            "motion": "Retrograde",
            "status": "Normal",
            "date": today.isoformat()
        },
        {
            "planet": "Ketu",
            "sign": "Virgo",
            "motion": "Retrograde",
            "status": "Normal",
            "date": today.isoformat()
        }
    ]


def get_mock_planetary_transits(use_real: Optional[bool] = None) -> List[Dict[str, Any]]:
    """
    Get planetary transit data - uses real ephemeris if available, otherwise mock
    
    Args:
        use_real: Force use of real ephemeris (True) or mock (False). 
                 None = auto-detect based on environment
    
    Returns:
        List of planetary transit dictionaries
    """
    # Determine if we should use real ephemeris
    if use_real is None:
        use_real = SWISSEPH_AVAILABLE and os.getenv("USE_REAL_EPHEMERIS", "true").lower() == "true"
    
    # Try to use real ephemeris
    if use_real and get_real_transits:
        try:
            real_transits = get_real_transits()
            if real_transits:
                print("✅ Using real ephemeris data")
                return real_transits
        except Exception as e:
            print(f"⚠️  Error getting real ephemeris data: {e}. Falling back to mock.")
    
    # Fallback to mock data
    print("ℹ️  Using mock planetary transit data")
    return get_mock_planetary_transits_static()


def get_mock_sector_list() -> List[str]:
    """Get list of all sectors in the mock data"""
    return [
        "Chemicals",
        "Technology",
        "Banking",
        "Oil & Gas",
        "Pharmaceuticals",
        "Automotive",
        "Iron & Steel",
        "Real Estate",
        "Telecom",
        "FMCG"
    ]


def get_stocks_by_sector(sector: str, stocks: List[Dict[str, Any]]) -> List[str]:
    """Get top stock symbols for a given sector"""
    sector_stocks = [s for s in stocks if s.get("sector") == sector]
    # Sort by 6-month returns
    sector_stocks.sort(key=lambda x: x.get("past_6m_return", 0), reverse=True)
    return [s["symbol"] for s in sector_stocks[:3]]


"""
Market Data Cache Service
Manages caching of stock data with TTL in PostgreSQL
"""
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import update

from app.models.models import MarketDataCache
from app.services.alpha_vantage_service import AlphaVantageService
from app.config.stock_config import get_cache_ttl_hours


class MarketDataCacheService:
    """
    Service for managing market data cache with Alpha Vantage integration
    Implements 1-hour TTL caching strategy
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.alpha_vantage = AlphaVantageService()
        self.cache_ttl_hours = get_cache_ttl_hours()
    
    def get_stock_data(
        self, 
        symbols: List[str], 
        force_refresh: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get stock data from cache or fetch from Alpha Vantage
        
        Args:
            symbols: List of stock symbols to fetch
            force_refresh: If True, bypass cache and fetch fresh data
            
        Returns:
            List of dictionaries with stock data
        """
        results = []
        symbols_to_fetch = []
        
        print(f"📊 Retrieving data for {len(symbols)} symbols...")
        
        for symbol in symbols:
            if not force_refresh:
                # Try to get from cache
                cached = self._get_from_cache(symbol)
                if cached:
                    results.append(cached)
                    print(f"  ✅ {symbol} - from cache")
                    continue
            
            # Need to fetch this symbol
            symbols_to_fetch.append(symbol)
            print(f"  ⏳ {symbol} - needs refresh")
        
        # Fetch missing symbols from Alpha Vantage
        if symbols_to_fetch:
            print(f"\n🌐 Fetching {len(symbols_to_fetch)} symbols from Alpha Vantage...")
            fresh_data = self.alpha_vantage.fetch_multiple_stocks(symbols_to_fetch)
            
            for data in fresh_data:
                # Save to cache
                self._save_to_cache(data)
                results.append(data)
        
        print(f"✅ Total: {len(results)} stocks retrieved\n")
        
        return results
    
    def _get_from_cache(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Check cache for valid data
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with stock data or None if not cached/expired
        """
        cached = self.db.query(MarketDataCache).filter(
            MarketDataCache.symbol == symbol,
            MarketDataCache.expires_at > datetime.utcnow()
        ).first()
        
        if cached:
            return self._model_to_dict(cached)
        
        return None
    
    def _save_to_cache(self, data: Dict[str, Any]):
        """
        Save or update cache entry with TTL
        
        Args:
            data: Stock data dictionary
        """
        symbol = data.get("symbol")
        if not symbol:
            return
        
        expires_at = datetime.utcnow() + timedelta(hours=self.cache_ttl_hours)
        
        # Check if entry exists
        existing = self.db.query(MarketDataCache).filter(
            MarketDataCache.symbol == symbol
        ).first()
        
        if existing:
            # Update existing entry
            update_stmt = update(MarketDataCache).where(
                MarketDataCache.symbol == symbol
            ).values(
                current_price=data.get("current_price"),
                open_price=data.get("open_price"),
                high=data.get("high"),
                low=data.get("low"),
                volume=data.get("volume"),
                change_percent=data.get("change_percent"),
                pe_ratio=data.get("pe_ratio"),
                market_cap=data.get("market_cap"),
                week_52_high=data.get("week_52_high"),
                week_52_low=data.get("week_52_low"),
                sector=data.get("sector", "Unknown"),
                cached_at=datetime.utcnow(),
                expires_at=expires_at
            )
            self.db.execute(update_stmt)
        else:
            # Insert new entry
            cache_entry = MarketDataCache(
                symbol=symbol,
                current_price=data.get("current_price"),
                open_price=data.get("open_price"),
                high=data.get("high"),
                low=data.get("low"),
                volume=data.get("volume"),
                change_percent=data.get("change_percent"),
                pe_ratio=data.get("pe_ratio"),
                market_cap=data.get("market_cap"),
                week_52_high=data.get("week_52_high"),
                week_52_low=data.get("week_52_low"),
                sector=data.get("sector", "Unknown"),
                expires_at=expires_at
            )
            self.db.add(cache_entry)
        
        try:
            self.db.commit()
        except Exception as e:
            print(f"⚠️  Error saving cache for {symbol}: {e}")
            self.db.rollback()
    
    def _model_to_dict(self, model: MarketDataCache) -> Dict[str, Any]:
        """
        Convert SQLAlchemy model to dictionary
        
        Args:
            model: MarketDataCache model instance
            
        Returns:
            Dictionary representation
        """
        return {
            "symbol": model.symbol,
            "current_price": model.current_price,
            "open_price": model.open_price,
            "high": model.high,
            "low": model.low,
            "volume": model.volume,
            "change_percent": model.change_percent,
            "pe_ratio": model.pe_ratio,
            "market_cap": model.market_cap,
            "week_52_high": model.week_52_high,
            "week_52_low": model.week_52_low,
            "sector": model.sector,
            "cached_at": model.cached_at.isoformat() if model.cached_at else None,
            "expires_at": model.expires_at.isoformat() if model.expires_at else None,
            # Add fields expected by analysis
            "past_6m_return": None,  # To be calculated separately
            "volatility": "Medium",
            "price_trend": "Upward" if model.change_percent and model.change_percent > 0 else "Downward",
            "news_sentiment": "Neutral"
        }
    
    def clear_expired_cache(self):
        """Remove expired cache entries"""
        try:
            deleted = self.db.query(MarketDataCache).filter(
                MarketDataCache.expires_at <= datetime.utcnow()
            ).delete()
            self.db.commit()
            if deleted > 0:
                print(f"🗑️  Cleared {deleted} expired cache entries")
        except Exception as e:
            print(f"⚠️  Error clearing cache: {e}")
            self.db.rollback()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total = self.db.query(MarketDataCache).count()
        valid = self.db.query(MarketDataCache).filter(
            MarketDataCache.expires_at > datetime.utcnow()
        ).count()
        expired = total - valid
        
        return {
            "total_entries": total,
            "valid_entries": valid,
            "expired_entries": expired
        }


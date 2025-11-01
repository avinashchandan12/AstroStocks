"""
Market Data API Routes
Real-time and cached stock market data endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from app.database.config import get_db
from app.services.market_data_cache import MarketDataCacheService
from app.config.stock_config import get_tracked_stocks, use_real_market_data

router = APIRouter(prefix="/market", tags=["Market Data"])


@router.get("/stocks/live")
async def get_live_stocks(
    force_refresh: bool = Query(False, description="Force refresh from Alpha Vantage"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get current market data for tracked NSE stocks
    
    Returns cached data if available and not expired (1-hour TTL),
    otherwise fetches fresh data from Alpha Vantage.
    
    Args:
        force_refresh: If True, bypass cache and fetch fresh data
        db: Database session
        
    Returns:
        Dictionary with stock data and metadata
    """
    if not use_real_market_data():
        raise HTTPException(
            status_code=503,
            detail="Real market data is disabled. Set USE_REAL_MARKET_DATA=true in environment."
        )
    
    try:
        cache_service = MarketDataCacheService(db)
        symbols = get_tracked_stocks()
        
        if not symbols:
            raise HTTPException(
                status_code=400,
                detail="No stocks configured. Set NSE_STOCKS in environment."
            )
        
        stocks = cache_service.get_stock_data(symbols, force_refresh=force_refresh)
        
        return {
            "success": True,
            "count": len(stocks),
            "stocks": stocks,
            "symbols_requested": symbols,
            "force_refresh": force_refresh
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching stock data: {str(e)}"
        )


@router.get("/stocks/{symbol}")
async def get_stock_detail(
    symbol: str,
    force_refresh: bool = Query(False, description="Force refresh from Alpha Vantage"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get detailed data for a specific stock
    
    Args:
        symbol: Stock symbol (e.g., "RELIANCE", "TCS")
        force_refresh: If True, bypass cache
        db: Database session
        
    Returns:
        Dictionary with stock details
    """
    if not use_real_market_data():
        raise HTTPException(
            status_code=503,
            detail="Real market data is disabled. Set USE_REAL_MARKET_DATA=true in environment."
        )
    
    try:
        cache_service = MarketDataCacheService(db)
        stocks = cache_service.get_stock_data([symbol.upper()], force_refresh=force_refresh)
        
        if not stocks:
            raise HTTPException(
                status_code=404,
                detail=f"Stock '{symbol}' not found or data unavailable"
            )
        
        return {
            "success": True,
            "stock": stocks[0]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching stock data: {str(e)}"
        )


@router.get("/cache/stats")
async def get_cache_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get cache statistics
    
    Returns information about cached entries, valid entries, and expired entries.
    """
    try:
        cache_service = MarketDataCacheService(db)
        stats = cache_service.get_cache_stats()
        
        return {
            "success": True,
            "cache_stats": stats
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching cache stats: {str(e)}"
        )


@router.post("/cache/clear-expired")
async def clear_expired_cache(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Clear expired cache entries
    
    Removes all cache entries that have passed their expiration time.
    """
    try:
        cache_service = MarketDataCacheService(db)
        cache_service.clear_expired_cache()
        
        stats = cache_service.get_cache_stats()
        
        return {
            "success": True,
            "message": "Expired cache entries cleared",
            "cache_stats": stats
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing cache: {str(e)}"
        )


@router.get("/tracked-symbols")
async def get_tracked_symbols() -> Dict[str, Any]:
    """
    Get list of currently tracked stock symbols
    
    Returns the symbols configured in the NSE_STOCKS environment variable.
    """
    symbols = get_tracked_stocks()
    
    return {
        "success": True,
        "count": len(symbols),
        "symbols": symbols
    }


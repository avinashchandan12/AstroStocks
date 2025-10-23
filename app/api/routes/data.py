"""
Data API Routes
Endpoints for retrieving stock, transit, and prediction data
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database.config import get_db
from app.schemas.schemas import Transit, SectorPrediction
from app.models import models
from app.services.mock_data import get_mock_planetary_transits, get_mock_stock_data

# Try to import ephemeris service
try:
    from app.services.ephemeris_service import (
        get_current_planetary_positions,
        get_moon_nakshatra,
        ephemeris_service,
        SWISSEPH_AVAILABLE
    )
except ImportError:
    SWISSEPH_AVAILABLE = False
    get_current_planetary_positions = None
    get_moon_nakshatra = None
    ephemeris_service = None

router = APIRouter(tags=["Data"])


@router.get("/planetary-transits")
async def get_planetary_transits() -> dict:
    """
    Get current planetary transit data
    
    Returns mock transit data showing current planetary positions
    in various zodiac signs.
    """
    transits = get_mock_planetary_transits()
    
    return {
        "transits": transits,
        "timestamp": datetime.utcnow().isoformat(),
        "note": "Mock data for MVP - will be replaced with real ephemeris data"
    }


@router.get("/sector-trends", response_model=List[SectorPrediction])
async def get_sector_trends(
    limit: int = Query(10, ge=1, le=100, description="Number of recent predictions to return"),
    sector: Optional[str] = Query(None, description="Filter by specific sector"),
    db: Session = Depends(get_db)
) -> List[SectorPrediction]:
    """
    Get latest sector predictions from database
    
    Returns the most recent sector trend predictions generated
    by the analysis engine.
    """
    try:
        query = db.query(models.SectorPrediction).order_by(
            models.SectorPrediction.created_at.desc()
        )
        
        if sector:
            query = query.filter(models.SectorPrediction.sector == sector)
        
        predictions = query.limit(limit).all()
        
        return predictions
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch trends: {str(e)}")


@router.get("/stocks")
async def get_stocks(
    sector: Optional[str] = Query(None, description="Filter stocks by sector")
) -> dict:
    """
    Get mock stock market data
    
    Returns sample stock data across various sectors for testing.
    """
    stocks = get_mock_stock_data()
    
    if sector:
        stocks = [s for s in stocks if s.get("sector") == sector]
    
    return {
        "stocks": stocks,
        "count": len(stocks),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/sectors")
async def get_sectors() -> dict:
    """
    Get list of all available sectors
    """
    stocks = get_mock_stock_data()
    sectors = list(set(s.get("sector") for s in stocks))
    sectors.sort()
    
    return {
        "sectors": sectors,
        "count": len(sectors)
    }


@router.get("/planetary-positions/live")
async def get_live_planetary_positions(
    date_str: Optional[str] = Query(None, description="Optional date in YYYY-MM-DD format (defaults to now)")
) -> dict:
    """
    Get real-time planetary positions using Swiss Ephemeris
    
    This endpoint provides accurate astronomical calculations including:
    - Planetary longitudes and latitudes
    - Zodiac signs
    - Retrograde motion
    - Exaltation/Debilitation status
    - Nakshatras
    
    Requires pyswisseph to be installed and USE_REAL_EPHEMERIS=true
    """
    if not SWISSEPH_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Swiss Ephemeris not available. Install pyswisseph to use this endpoint."
        )
    
    if not ephemeris_service.use_real_ephemeris:
        raise HTTPException(
            status_code=503,
            detail="Real ephemeris disabled. Set USE_REAL_EPHEMERIS=true in environment."
        )
    
    try:
        # Parse date if provided
        calc_date = None
        if date_str:
            try:
                calc_date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid date format. Use YYYY-MM-DD"
                )
        
        # Get planetary positions
        print("Getting planetary positions")
        print("date>", calc_date)
        positions = ephemeris_service.get_all_planetary_positions(calc_date)
        
        # Get Moon nakshatra
        moon_nakshatra = ephemeris_service.get_moon_nakshatra(calc_date)
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "calculation_date": calc_date.isoformat() if calc_date else datetime.utcnow().isoformat(),
            "positions": positions,
            "moon_nakshatra": moon_nakshatra,
            "count": len(positions),
            "source": "Swiss Ephemeris"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating planetary positions: {str(e)}"
        )


@router.get("/nakshatra")
async def get_current_nakshatra() -> dict:
    """
    Get current Moon nakshatra (lunar mansion)
    
    Returns the current nakshatra, pada, and Moon's position
    """
    if not SWISSEPH_AVAILABLE or not ephemeris_service.use_real_ephemeris:
        return {
            "error": "Swiss Ephemeris not available",
            "message": "Install pyswisseph and set USE_REAL_EPHEMERIS=true"
        }
    
    try:
        nakshatra_data = get_moon_nakshatra()
        if not nakshatra_data:
            raise HTTPException(status_code=500, detail="Could not calculate nakshatra")
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "nakshatra": nakshatra_data["name"],
            "pada": nakshatra_data["pada"],
            "moon_longitude": nakshatra_data["moon_position"]["longitude"],
            "moon_sign": nakshatra_data["moon_position"]["sign"],
            "source": "Swiss Ephemeris"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating nakshatra: {str(e)}"
        )


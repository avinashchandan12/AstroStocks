"""
Transits API Routes
Endpoint for retrieving transit data by date with caching
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.database.config import get_db
from app.models import models
from app.schemas.schemas import TransitResponse
from app.services.ephemeris_service import get_planetary_transits, SWISSEPH_AVAILABLE

router = APIRouter(tags=["Transits"])


@router.get("/transits", response_model=TransitResponse)
async def get_transits(
    date: Optional[str] = Query(
        None,
        description="Date in YYYY-MM-DD format. If not provided, uses current date."
    ),
    hard_refresh: bool = Query(
        False,
        description="If true, bypass cache and regenerate transit data for the specified date."
    ),
    db: Session = Depends(get_db)
) -> TransitResponse:
    """
    Get planetary transit data for a specific date
    
    Returns transit data for all planets including:
    - Current sign position (Rashi)
    - Nakshatra for each planet
    - Transit start and end dates
    - Motion (Direct/Retrograde)
    - Status (Exalted/Debilitated/Normal)
    
    Data is cached by date. If the date already exists in cache,
    returns cached data. Otherwise calculates and stores new data.
    
    Use hard_refresh=true to bypass cache and regenerate data.
    """
    if not SWISSEPH_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Swiss Ephemeris not available. Install pyswisseph to use this endpoint."
        )
    
    try:
        # Parse date or use current date
        if date:
            try:
                target_date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid date format. Use YYYY-MM-DD"
                )
        else:
            target_date = datetime.utcnow().date()
        
        # If hard_refresh is true, delete existing cache for this date
        if hard_refresh:
            db.query(models.Transit).filter(models.Transit.date == target_date).delete()
            db.commit()
        
        # Check cache first - query all transits for this date
        # Expected number of planets: 9 (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu)
        cached_transits = db.query(models.Transit).filter(
            models.Transit.date == target_date
        ).all()
        
        # Consider cached if we have at least 8 planets (allowing for edge cases)
        if not hard_refresh and cached_transits and len(cached_transits) >= 8:
            # Convert Transit models to PlanetaryTransit format
            transits_list = []
            for transit in cached_transits:
                transits_list.append({
                    "planet": transit.planet,
                    "sign": transit.sign,
                    "motion": transit.motion or "Direct",
                    "status": transit.status or transit.dignity or "Normal",
                    "dignity": transit.dignity or transit.status or "Normal",
                    "date": transit.date.isoformat(),
                    "longitude": transit.longitude or 0.0,
                    "latitude": transit.latitude or 0.0,
                    "degree_in_sign": transit.degree_in_sign or 0.0,
                    "retrograde": (transit.retrograde == "True" if transit.retrograde else False) or (transit.motion == "Retrograde"),
                    "speed": transit.speed or 0.0,
                    "nakshatra": transit.nakshatra,
                    "transit_start": transit.transit_start,
                    "transit_end": transit.transit_end
                })
            
            # Get the most recent timestamp from cached transits
            latest_timestamp = max(
                [t.updated_at or t.created_at for t in cached_transits if t.updated_at or t.created_at],
                default=datetime.utcnow()
            )
            
            return TransitResponse(
                date=target_date.isoformat(),
                transits=transits_list,
                cached=True,
                timestamp=latest_timestamp
            )
        
        # Calculate new transit data
        calc_datetime = datetime.combine(target_date, datetime.min.time())
        transits = get_planetary_transits(calc_datetime)
        
        if not transits:
            raise HTTPException(
                status_code=500,
                detail="Failed to calculate planetary transits"
            )
        
        # Delete any existing partial transit data for this date before storing new data
        # This ensures we don't have stale partial data
        db.query(models.Transit).filter(models.Transit.date == target_date).delete()
        
        # Store in Transit table - one row per planet
        for transit_data in transits:
            transit_record = models.Transit(
                planet=transit_data.get("planet"),
                sign=transit_data.get("sign"),
                motion=transit_data.get("motion", "Direct"),
                status=transit_data.get("status") or transit_data.get("dignity", "Normal"),
                date=target_date,
                longitude=transit_data.get("longitude", 0.0),
                latitude=transit_data.get("latitude", 0.0),
                degree_in_sign=transit_data.get("degree_in_sign", 0.0),
                retrograde="True" if transit_data.get("retrograde") or transit_data.get("motion") == "Retrograde" else "False",
                speed=transit_data.get("speed", 0.0),
                dignity=transit_data.get("dignity") or transit_data.get("status", "Normal"),
                nakshatra=transit_data.get("nakshatra"),
                transit_start=transit_data.get("transit_start"),
                transit_end=transit_data.get("transit_end")
            )
            db.add(transit_record)
        
        db.commit()
        
        return TransitResponse(
            date=target_date.isoformat(),
            transits=transits,
            cached=False,
            timestamp=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving transit data: {str(e)}"
        )


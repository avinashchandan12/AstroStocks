"""
Sector API Routes
Endpoints for managing and retrieving sector data
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database.config import get_db
from app.schemas.schemas import Sector, SectorCreate
from app.models import models

router = APIRouter(prefix="/sectors", tags=["Sectors"])


@router.get("", response_model=List[Sector])
async def get_sectors(
    limit: int = Query(100, ge=1, le=1000, description="Number of sectors to return"),
    db: Session = Depends(get_db)
) -> List[Sector]:
    """
    Get all sectors
    
    Returns a list of all sectors in the database.
    """
    try:
        sectors = db.query(models.Sector).limit(limit).all()
        return sectors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch sectors: {str(e)}")


@router.get("/{sector_id}", response_model=Sector)
async def get_sector(
    sector_id: int,
    db: Session = Depends(get_db)
) -> Sector:
    """
    Get a specific sector by ID
    
    Returns detailed information about a sector including performance metrics.
    """
    try:
        sector = db.query(models.Sector).filter(models.Sector.id == sector_id).first()
        
        if not sector:
            raise HTTPException(status_code=404, detail=f"Sector with ID {sector_id} not found")
        
        return sector
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch sector: {str(e)}")


@router.post("", response_model=Sector, status_code=201)
async def create_sector(
    sector: SectorCreate,
    db: Session = Depends(get_db)
) -> Sector:
    """
    Create a new sector
    
    Creates a new sector with the provided information.
    """
    try:
        # Check if sector already exists
        existing = db.query(models.Sector).filter(models.Sector.name == sector.name).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Sector with name '{sector.name}' already exists"
            )
        
        # Create new sector
        db_sector = models.Sector(**sector.model_dump())
        db.add(db_sector)
        db.commit()
        db.refresh(db_sector)
        
        return db_sector
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create sector: {str(e)}")


@router.put("/{sector_id}", response_model=Sector)
async def update_sector(
    sector_id: int,
    sector_update: SectorCreate,
    db: Session = Depends(get_db)
) -> Sector:
    """
    Update a sector
    
    Updates sector information including performance metrics.
    """
    try:
        sector = db.query(models.Sector).filter(models.Sector.id == sector_id).first()
        
        if not sector:
            raise HTTPException(status_code=404, detail=f"Sector with ID {sector_id} not found")
        
        # Check if name is being changed to an existing one
        if sector_update.name != sector.name:
            existing = db.query(models.Sector).filter(models.Sector.name == sector_update.name).first()
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail=f"Sector with name '{sector_update.name}' already exists"
                )
        
        # Update fields
        for field, value in sector_update.model_dump().items():
            setattr(sector, field, value)
        
        sector.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(sector)
        
        return sector
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update sector: {str(e)}")


@router.delete("/{sector_id}", status_code=204)
async def delete_sector(
    sector_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a sector
    
    Deletes a sector. Note: This will fail if there are stocks associated with this sector.
    """
    try:
        sector = db.query(models.Sector).filter(models.Sector.id == sector_id).first()
        
        if not sector:
            raise HTTPException(status_code=404, detail=f"Sector with ID {sector_id} not found")
        
        # Check if there are stocks associated with this sector
        stock_count = db.query(models.Stock).filter(models.Stock.sector_id == sector_id).count()
        if stock_count > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot delete sector with ID {sector_id}. There are {stock_count} stocks associated with this sector."
            )
        
        db.delete(sector)
        db.commit()
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete sector: {str(e)}")


@router.get("/{sector_id}/stocks")
async def get_sector_stocks(
    sector_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all stocks in a specific sector
    
    Returns a list of all stocks that belong to this sector.
    """
    try:
        sector = db.query(models.Sector).filter(models.Sector.id == sector_id).first()
        
        if not sector:
            raise HTTPException(status_code=404, detail=f"Sector with ID {sector_id} not found")
        
        stocks = db.query(models.Stock).filter(models.Stock.sector_id == sector_id).all()
        
        return {
            "sector": {
                "id": sector.id,
                "name": sector.name,
                "description": sector.description
            },
            "count": len(stocks),
            "stocks": stocks
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch sector stocks: {str(e)}")


@router.get("/search/by-name")
async def search_sector_by_name(
    name: str = Query(..., description="Sector name to search for"),
    db: Session = Depends(get_db)
):
    """
    Search for a sector by name
    
    Returns sector information based on name search.
    """
    try:
        # Case-insensitive search
        sector = db.query(models.Sector).filter(
            models.Sector.name.ilike(f"%{name}%")
        ).first()
        
        if not sector:
            raise HTTPException(status_code=404, detail=f"No sector found matching '{name}'")
        
        return sector
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search sector: {str(e)}")


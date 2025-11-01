"""
Sector Mapper - Maps astrology engine sectors to database sectors
This service bridges the gap between astrological sector predictions and database sectors
"""
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from app.database.config import SessionLocal
from app.models.models import Sector


class SectorMapper:
    """Maps astrology engine sector names to database sector records"""
    
    # Mapping from astrology engine sectors to database sector names
    SECTOR_NAME_MAPPING = {
        # Oil & Gas / Energy
        "Oil": "Oil & Gas",
        "Energy": "Utilities & Power",
        "Power": "Utilities & Power",
        
        # Automotive
        "Automotive": "Auto & Auto Components",
        
        # Real Estate
        "Real Estate": "Real Estate / Realty",
        
        # Agriculture
        "Agriculture": "Agriculture & Agrochemicals",
        
        # Mining
        "Mining": "Metals & Mining",
        "Iron & Steel": "Metals & Mining",
        
        # Construction
        "Construction": "Construction & Construction Materials",
        
        # FMCG
        "FMCG": "Consumer Staples / FMCG",
        
        # Chemicals
        "Chemicals": "Chemicals & Petrochemicals",
        "Pharmaceuticals": "Healthcare / Pharmaceuticals",
        "Pharma": "Healthcare / Pharmaceuticals",
        
        # Beverages
        "Beverages": "Food Products & Beverages",
        
        # Marine
        "Marine": "Logistics, Transport & Marine",
        
        # Technology
        "Technology": "Information Technology",
        "IT": "Information Technology",
        
        # Telecom
        "Telecom": "Telecommunication / Telecom",
        "Communication": "Telecommunication / Telecom",
        
        # Aviation
        "Aviation": "Aviation",
        
        # Media
        "Media": "Media & Entertainment",
        "Entertainment": "Media & Entertainment",
        
        # Banking & Finance
        "Banking": "Banking",
        "Finance": "Financial Services",
        
        # Insurance
        "Insurance": "Insurance",
        
        # Education
        "Education": "Education & Training",
        
        # Hospitality
        "Hospitality": "Hospitality & Tourism",
        
        # Government/Defense
        "Government": "Security & Defense",
        "Defense": "Security & Defense",
        
        # Fashion/Luxury
        "Luxury Goods": "Gems, Jewellery & Luxury Goods",
        "Fashion": "Textiles, Apparel & Footwear",
        
        # Consumer Discretionary
        "Consumer Discretionary": "Consumer Discretionary",
        
        # Consumer Electronics
        "Electronics": "Household Durables & Consumer Electronics",
        
        # Machinery
        "Machinery": "Capital Goods / Industrials",
        
        # Public Services / Dairy
        "Dairy": "Consumer Staples / FMCG",
        "Public Services": "Consumer Staples / FMCG",
        
        # Retail
        "Retail": "Retail",
        
        # Trading
        "Trading": "Trading & Distribution",
        "Commerce": "Trading & Distribution",
        
        # Misc
        "Speculation": "Financial Services",
        "Research": "Healthcare / Pharmaceuticals",
        "Spirituality": "Miscellaneous / Other",
        "Occult": "Miscellaneous / Other",
        
        # Additional mappings
        "Gold": "Gems, Jewellery & Luxury Goods",
        "Foreign Trade": "Trading & Distribution",
    }
    
    def __init__(self, db: Optional[Session] = None):
        """Initialize mapper with optional database session"""
        self.db = db or SessionLocal()
        self._sector_cache = None
    
    def _load_sectors(self) -> Dict[str, Sector]:
        """Load all sectors from database into a cache"""
        if self._sector_cache is None:
            sectors = self.db.query(Sector).all()
            self._sector_cache = {s.name: s for s in sectors}
        return self._sector_cache
    
    def map_to_database_sector(self, astrology_sector: str) -> Optional[Sector]:
        """
        Map an astrology engine sector name to a database sector record
        
        Args:
            astrology_sector: Sector name from astrology engine
            
        Returns:
            Sector object from database or None if not found
        """
        # Load sectors if not cached
        sectors = self._load_sectors()
        
        # Try direct match first
        if astrology_sector in sectors:
            return sectors[astrology_sector]
        
        # Try mapping
        mapped_name = self.SECTOR_NAME_MAPPING.get(astrology_sector)
        if mapped_name and mapped_name in sectors:
            return sectors[mapped_name]
        
        # Try case-insensitive match
        for sector_name, sector in sectors.items():
            if sector_name.lower() == astrology_sector.lower():
                return sector
        
        # Try partial match
        for sector_name, sector in sectors.items():
            if astrology_sector.lower() in sector_name.lower() or sector_name.lower() in astrology_sector.lower():
                return sector
        
        # Return None if no match found
        return None
    
    def map_sector_influences_to_db_sectors(
        self, 
        sector_influences: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[Sector, List[Dict[str, Any]]]:
        """
        Map astrology engine sector influences to database sectors
        
        Args:
            sector_influences: Dictionary mapping sector names to influences from astrology engine
            
        Returns:
            Dictionary mapping Sector objects to influences
        """
        mapped_influences = {}
        unmatched_sectors = []
        
        for sector_name, influences in sector_influences.items():
            db_sector = self.map_to_database_sector(sector_name)
            
            if db_sector:
                # Aggregate influences if sector already exists
                if db_sector in mapped_influences:
                    mapped_influences[db_sector].extend(influences)
                else:
                    mapped_influences[db_sector] = influences
            else:
                unmatched_sectors.append(sector_name)
        
        # Log unmatched sectors
        if unmatched_sectors:
            print(f"⚠️  Could not map {len(unmatched_sectors)} sectors to database:")
            for sector in unmatched_sectors:
                print(f"   - {sector}")
        
        return mapped_influences
    
    def get_all_database_sectors(self) -> List[Sector]:
        """Get all sectors from database"""
        return list(self._load_sectors().values())
    
    def close(self):
        """Close database session if we created it"""
        if self.db and hasattr(self.db, 'close'):
            self.db.close()


#!/usr/bin/env python3
"""
Script to populate initial sectors in the database

This script creates comprehensive Indian stock market sectors.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database.config import SessionLocal
from app.models.models import Sector


# Comprehensive Indian stock market sectors
SECTORS_DATA = [
    {
        "name": "Auto & Auto Components",
        "description": "Passenger cars, 2/3 wheelers, commercial vehicles, and auto parts & components",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Banking",
        "description": "Public and private sector banks (including retail and corporate banking)",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Financial Services",
        "description": "NBFCs, capital markets, exchanges, asset managers, and other non-bank financial firms",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Consumer Discretionary",
        "description": "Consumer goods and services that are non-essential — e.g. retail, leisure, autos",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Consumer Staples / FMCG",
        "description": "Fast-moving consumer goods, packaged food, personal care and household products",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Information Technology",
        "description": "Software, IT services, IT products, and IT-enabled services",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Healthcare / Pharmaceuticals",
        "description": "Pharmaceutical manufacturers, healthcare services, hospitals and allied healthcare",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Oil & Gas",
        "description": "Upstream, midstream, downstream oil & gas companies and refiners",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Chemicals & Petrochemicals",
        "description": "Commodity and specialty chemicals, petrochemical manufacturers and distributors",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Metals & Mining",
        "description": "Ferrous & non-ferrous metals, mining and mineral extraction",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Capital Goods / Industrials",
        "description": "Engineering, industrial machinery, capital goods and heavy equipment manufacturers",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Construction & Construction Materials",
        "description": "Cement, construction materials, contractors and large infrastructure developers",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Real Estate / Realty",
        "description": "Property developers, REITs, commercial and residential real estate businesses",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Telecommunication / Telecom",
        "description": "Telecommunication services, carriers and related network equipment",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Utilities & Power",
        "description": "Electric generation, transmission, distribution, and utilities (including renewable energy)",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Media & Entertainment",
        "description": "Broadcast, print, digital media, film and content production and distribution",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Retail",
        "description": "Organised retail chains and speciality retail businesses",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Textiles, Apparel & Footwear",
        "description": "Textile manufacturers, garments, apparel, footwear and related supply chain",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Food Products & Beverages",
        "description": "Packaged foods, beverages, tea, coffee, breweries and allied food processing",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Agriculture & Agrochemicals",
        "description": "Agri inputs, fertilizers, seeds, agrochemicals and agri-logistics",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Logistics, Transport & Marine",
        "description": "Freight, shipping, ports, logistics providers and transport services",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Aviation",
        "description": "Airlines, airport services and aviation support businesses",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Utilities - Power Generation & Distribution",
        "description": "Independent power producers, utilities and distribution companies",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Mining & Quarrying",
        "description": "Industrial minerals, stone, and other mining activities (distinct from metals production)",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Packaging & Paper",
        "description": "Paper, packaging materials and related manufacturers",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Glass, Ceramics & Building Products",
        "description": "Glass manufacturers, tiles, ceramics and home-building products",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Gems, Jewellery & Luxury Goods",
        "description": "Gold & jewelry manufacturers, luxury brands and related retail",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Education & Training",
        "description": "Schools, ed-tech companies, education services and training providers",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Hospitality & Tourism",
        "description": "Hotels, resorts, travel services and tourism operators",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Insurance",
        "description": "Life and non-life insurance companies and intermediaries",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Paints, Adhesives & Home Improvement",
        "description": "Paint manufacturers and related home-improvement product makers",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Household Durables & Consumer Electronics",
        "description": "Consumer durables, home appliances, electronics and white goods",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Electricals & Switchgear",
        "description": "Electrical equipment, switchgear and wiring manufacturers",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Packaging & Containers",
        "description": "Rigid & flexible packaging manufacturers, bottles, cans and containers",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Industrial Gases & Fuels",
        "description": "Industrial gas suppliers and fuel distribution businesses",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Trading & Distribution",
        "description": "Trading houses, distributors and broad commerce-oriented firms",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Professional Services & Consulting",
        "description": "Business services, consulting, audit, legal and advisory firms",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Renewables & Clean Energy",
        "description": "Solar, wind, bioenergy and other renewable energy equipment and producers",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Security & Defense",
        "description": "Defense production, aerospace and homeland security suppliers",
        "exchange": "Both",
        "country": "India"
    },
    {
        "name": "Miscellaneous / Other",
        "description": "Sectors not classified above or composite businesses",
        "exchange": "Both",
        "country": "India"
    },
]


def populate_sectors():
    """Populate sectors in the database"""
    db = SessionLocal()
    
    try:
        created_count = 0
        skipped_count = 0
        
        for sector_data in SECTORS_DATA:
            # Check if sector already exists
            existing = db.query(Sector).filter(Sector.name == sector_data["name"]).first()
            
            if existing:
                print(f"⏭️  Sector '{sector_data['name']}' already exists, skipping")
                skipped_count += 1
                continue
            
            # Create new sector
            sector = Sector(**sector_data)
            db.add(sector)
            created_count += 1
            print(f"✅ Created sector: {sector_data['name']}")
        
        db.commit()
        
        print("\n" + "=" * 60)
        print(f"✨ Sectors populated successfully!")
        print(f"   Created: {created_count}")
        print(f"   Skipped: {skipped_count}")
        print(f"   Total sectors available: {db.query(Sector).count()}")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error populating sectors: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Populating sectors in database...\n")
    populate_sectors()

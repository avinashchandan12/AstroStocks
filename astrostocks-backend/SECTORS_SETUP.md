# Sectors Database Setup Guide

## Overview

The Sector table has been added to store sector information and track sector-level performance metrics. Each stock is now linked to a sector through a foreign key relationship.

---

## Database Changes

### New Table: `sectors`

**Columns:**
- `id` (Primary Key)
- `name` (Unique, Required)
- `description` (Optional)
- `past_6m_return` (Average 6-month return)
- `past_1y_return` (Average 1-year return)
- `volatility` (High/Medium/Low)
- `market_cap` (Total market cap)
- `created_at` (Auto-generated)
- `updated_at` (Auto-updated)

### Modified Table: `stocks`

**New Column:**
- `sector_id` (ForeignKey to sectors.id, nullable for now)

**Existing Column:**
- `sector` (String, kept for backward compatibility)

---

## Setup Instructions

### 1. Run Database Migration

Apply the migration to create the sectors table:

```bash
# Activate virtual environment
source venv/bin/activate

# Run migration
alembic upgrade head
```

### 2. Populate Initial Sectors

Run the script to populate common Indian stock market sectors:

```bash
python3 scripts/populate_sectors.py
```

This will create 15 common sectors:
- Pharmaceuticals
- Chemicals
- Technology
- Banking
- Oil & Gas
- Automotive
- Iron & Steel
- Real Estate
- Telecom
- FMCG
- Infrastructure
- Power
- Cement
- Financial Services
- Metals & Mining

### 3. Link Existing Stocks to Sectors

After populating sectors, you'll need to link existing stocks to their sectors. You can do this through:

- The API (see endpoints below)
- A custom script
- Direct database queries

---

## API Endpoints

### Get All Sectors
```
GET /sectors
```
Returns a list of all sectors (with optional limit).

**Query Parameters:**
- `limit` (default: 100, max: 1000)

**Example:**
```bash
curl http://localhost:8000/sectors?limit=20
```

### Get Sector by ID
```
GET /sectors/{sector_id}
```
Returns detailed information about a specific sector.

**Example:**
```bash
curl http://localhost:8000/sectors/1
```

### Create Sector
```
POST /sectors
```
Creates a new sector.

**Request Body:**
```json
{
  "name": "Telecommunications",
  "description": "Telecom service providers",
  "volatility": "Medium",
  "past_6m_return": 8.5
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/sectors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Telecommunications",
    "description": "Telecom service providers",
    "volatility": "Medium"
  }'
```

### Update Sector
```
PUT /sectors/{sector_id}
```
Updates sector information.

**Example:**
```bash
curl -X PUT http://localhost:8000/sectors/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Technology",
    "volatility": "Low",
    "past_6m_return": 15.0
  }'
```

### Delete Sector
```
DELETE /sectors/{sector_id}
```
Deletes a sector (only if no stocks are associated with it).

**Example:**
```bash
curl -X DELETE http://localhost:8000/sectors/10
```

### Get Stocks in Sector
```
GET /sectors/{sector_id}/stocks
```
Returns all stocks belonging to a specific sector.

**Example:**
```bash
curl http://localhost:8000/sectors/3/stocks
```

### Search Sector by Name
```
GET /sectors/search/by-name?name={sector_name}
```
Searches for a sector by name (case-insensitive).

**Example:**
```bash
curl http://localhost:8000/sectors/search/by-name?name=pharma
```

---

## Usage in AI Analysis

The sector relationships can now be used in AI analysis:

1. **Sector-level aggregation**: Calculate average returns, volatility across all stocks in a sector
2. **Sector predictions**: Generate predictions for entire sectors based on planetary influences
3. **Stock recommendations**: Recommend stocks within favorable sectors
4. **Performance tracking**: Track sector performance over time

---

## Example: Linking a Stock to a Sector

### Via API (when creating/updating a stock)
```bash
curl -X POST http://localhost:8000/stocks \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "RELIANCE",
    "sector": "Oil & Gas",
    "sector_id": 5,
    "past_6m_return": 12.3,
    "volatility": "Medium"
  }'
```

### Via Python Script
```python
from app.database.config import SessionLocal
from app.models.models import Stock, Sector

db = SessionLocal()

# Get sector
sector = db.query(Sector).filter(Sector.name == "Oil & Gas").first()

# Update stock
stock = db.query(Stock).filter(Stock.symbol == "RELIANCE").first()
stock.sector_id = sector.id
stock.sector = sector.name

db.commit()
```

---

## Migration Rollback

If you need to rollback the migration:

```bash
alembic downgrade -1
```

This will:
- Drop the `sector_id` column from stocks
- Drop the sectors table
- Remove all indexes

---

## Next Steps

1. ✅ Run the migration
2. ✅ Populate sectors
3. ⏳ Link existing stocks to sectors
4. ⏳ Update AI analysis to use sector relationships
5. ⏳ Add sector performance tracking

---

**Setup Complete!** 🎉


# 🚀 Quick Start Guide - AstroFinanceAI

## Option 1: Docker (Recommended)

### Start Everything

```bash
docker-compose up --build
```

This will:
- Start PostgreSQL on port 5432
- Start FastAPI on port 8000
- Auto-reload on code changes

### Run Migrations

```bash
docker-compose exec api alembic upgrade head
```

### Access the API

- **API Root**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Get planetary transits
curl http://localhost:8000/planetary-transits

# Run analysis (uses mock data)
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{}'

# Get sector trends
curl http://localhost:8000/sector-trends
```

### Stop Everything

```bash
docker-compose down
```

---

## Option 2: Local Development (Without Docker)

### Prerequisites

- Python 3.11+
- PostgreSQL running locally

### Steps

1. **Start PostgreSQL**
   ```bash
   # On macOS with Homebrew
   brew services start postgresql@15
   
   # Or use Docker for just PostgreSQL
   docker-compose up -d postgres
   ```

2. **Create Database**
   ```bash
   createdb astrofinance_db
   ```

3. **Set Up Python Environment**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   # Copy example env file
   cp .env.example .env
   
   # Edit .env if needed (default settings should work)
   ```

5. **Run Migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the API**
   ```bash
   uvicorn app.main:app --reload
   ```

   Or use the startup script:
   ```bash
   ./run_local.sh
   ```

7. **Access the API**
   - http://localhost:8000/docs

---

## 🧪 Testing the Setup

### 1. Check Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "AstroFinanceAI Backend"
}
```

### 2. Get Mock Data

```bash
curl http://localhost:8000/planetary-transits
```

### 3. Run Analysis

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{}'
```

This will:
- Use mock stock data
- Use mock planetary transit data
- Run astrological analysis
- Store predictions in database
- Return structured predictions

### 4. View Saved Predictions

```bash
curl http://localhost:8000/sector-trends
```

---

## 📊 Understanding the Response

The `/analyze` endpoint returns predictions like:

```json
{
  "sector_predictions": [
    {
      "sector": "Technology",
      "planetary_influence": "Mercury in Virgo (Exalted), Rahu in Pisces",
      "trend": "Bullish",
      "reason": "Strong planetary support from Mercury and Rahu",
      "top_stocks": ["TCS", "INFY"],
      "confidence": "High",
      "ai_insights": "Technology sector shows strong momentum..."
    }
  ],
  "overall_market_sentiment": "Positive",
  "accuracy_estimate": "78%",
  "timestamp": "2025-10-23T12:00:00"
}
```

---

## 🔧 Troubleshooting

### Port Already in Use

If port 8000 or 5432 is already in use:

```bash
# For API (change port)
uvicorn app.main:app --reload --port 8001

# For Docker (edit docker-compose.yml)
# Change ports: "8001:8000" for API
# Change ports: "5433:5432" for PostgreSQL
```

### Database Connection Error

Make sure PostgreSQL is running:

```bash
# Check if running
pg_isready

# Or with Docker
docker-compose ps
```

### Migration Errors

Reset migrations:

```bash
# Drop and recreate database
dropdb astrofinance_db
createdb astrofinance_db

# Run migrations again
alembic upgrade head
```

---

## 📚 Next Steps

1. ✅ Verify all endpoints work
2. ✅ Check database tables were created
3. ✅ Explore Swagger documentation at `/docs`
4. 🔜 Integrate real stock market APIs
5. 🔜 Add OpenAI/Claude integration
6. 🔜 Build frontend

---

## 💡 Development Tips

- The API auto-reloads on code changes
- Mock data is in `app/services/mock_data.py`
- Astrology logic is in `app/services/astrology_engine.py`
- Add new endpoints in `app/api/routes/`
- Database models are in `app/models/models.py`

For full documentation, see [README.md](README.md)


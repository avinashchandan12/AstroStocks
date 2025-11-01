# 🪐 AstroFinanceAI Backend

> **Combining Vedic Astrology (Jyotish) with Stock Market Analytics using FastAPI, PostgreSQL & AI**

---

## 📘 Overview

AstroFinanceAI is an innovative system that merges **Vedic Astrology (Jyotish Shastra)** with **stock market data** to generate AI-driven, astrologically-informed predictions for different sectors and stocks.

### Key Features

- **FastAPI Backend** - High-performance REST API
- **PostgreSQL Database** - Robust data storage
- **Astrology Engine** - Vedic astrology logic mapping planets to market sectors
- **AI Service Layer** - Structured reasoning combining astrology with market data
- **Mock Data** - Complete testing environment with sample data

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- PostgreSQL (if running without Docker)

### Setup with Docker (Recommended)

1. **Clone the repository**
   ```bash
   cd /Users/avinash2/AstroStocks
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY if needed
   ```

3. **Start services with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Run database migrations**
   ```bash
   docker-compose exec api alembic upgrade head
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Setup without Docker (Local Development)

1. **Create virtual environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL database**
   ```bash
   createdb astrofinance_db
   ```

4. **Create .env file**
   ```bash
   cp .env.example .env
   # Update DATABASE_URL if needed
   ```

5. **Run migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

---

## 📚 API Documentation

### Main Endpoints

#### 1. **POST /analyze** - Astrological Market Analysis

Generate sector-wise predictions based on planetary transits and stock data.

**Request:**
```json
{
  "stocks": [],  // Optional: Use mock data if empty
  "transits": {}  // Optional: Use mock data if empty
}
```

**Response:**
```json
{
  "sector_predictions": [
    {
      "sector": "Chemicals",
      "planetary_influence": "Jupiter in Taurus (Normal), Venus in Pisces (Exalted (Very Strong))",
      "trend": "Bullish",
      "reason": "Influenced by Jupiter, Venus, Moon. Jupiter in Taurus (Normal). Venus in Pisces (Exalted (Very Strong)).",
      "top_stocks": ["TATACHEM", "UPL"],
      "confidence": "Medium",
      "ai_insights": "Strong positive momentum expected in Chemicals sector. Jupiter's favorable position supports growth. Venus's favorable position supports growth."
    }
  ],
  "overall_market_sentiment": "Positive",
  "accuracy_estimate": "78%",
  "timestamp": "2025-10-23T12:00:00"
}
```

#### 2. **GET /planetary-transits** - Current Planetary Positions

Get current planetary transit data (mock data for MVP).

**Response:**
```json
{
  "transits": [
    {
      "planet": "Jupiter",
      "sign": "Taurus",
      "motion": "Direct",
      "status": "Normal",
      "date": "2025-10-23"
    }
  ],
  "timestamp": "2025-10-23T12:00:00"
}
```

#### 3. **GET /sector-trends** - Latest Predictions

Get recent sector predictions from the database.

**Query Parameters:**
- `limit` (int): Number of predictions to return (default: 10)
- `sector` (str): Filter by specific sector

#### 4. **GET /stocks** - Stock Data

Get mock stock market data.

**Query Parameters:**
- `sector` (str): Filter by sector

#### 5. **GET /sectors** - Available Sectors

Get list of all available sectors in the system.

---

## 🗄️ Database Schema

### Tables

#### `stocks`
```sql
CREATE TABLE stocks (
  id SERIAL PRIMARY KEY,
  symbol VARCHAR(20),
  sector VARCHAR(50),
  past_6m_return FLOAT,
  volatility VARCHAR(20),
  pe_ratio FLOAT,
  price_trend VARCHAR(20),
  news_sentiment VARCHAR(50)
);
```

#### `transits`
```sql
CREATE TABLE transits (
  id SERIAL PRIMARY KEY,
  planet VARCHAR(20),
  sign VARCHAR(20),
  motion VARCHAR(20),
  status VARCHAR(20),
  date DATE
);
```

#### `sector_predictions`
```sql
CREATE TABLE sector_predictions (
  id SERIAL PRIMARY KEY,
  sector VARCHAR(50),
  planetary_influence TEXT,
  trend VARCHAR(20),
  reason TEXT,
  top_stocks JSONB,
  accuracy_estimate FLOAT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🧮 Architecture

```
┌─────────────────┐
│  FastAPI App    │
└────────┬────────┘
         │
    ┌────┴────────────────┐
    │                     │
┌───▼────────┐    ┌──────▼─────┐
│ API Routes │    │  Services  │
└────────────┘    └──────┬─────┘
                         │
              ┌──────────┼──────────┐
              │          │          │
      ┌───────▼───┐  ┌──▼──────┐  ┌▼─────────┐
      │ Astrology │  │AI Service│  │Mock Data │
      │  Engine   │  └──────────┘  └──────────┘
      └───────────┘
              │
      ┌───────▼────────┐
      │   PostgreSQL   │
      └────────────────┘
```

### Key Components

1. **Astrology Engine** (`app/services/astrology_engine.py`)
   - Planet-to-Element mapping
   - Element-to-Sector mapping
   - Transit analysis logic
   - Vedic astrology significations

2. **AI Service** (`app/services/ai_service.py`)
   - Combines astrological insights with market data
   - Mock AI reasoning (extensible to real LLM)
   - Knowledge base prompt template

3. **Mock Data Layer** (`app/services/mock_data.py`)
   - Sample stocks across 10+ sectors
   - Planetary transit data
   - Realistic market scenarios

4. **Database Models** (`app/models/models.py`)
   - SQLAlchemy ORM models
   - Stocks, Transits, Predictions tables

---

## 🧪 Testing the API

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Get planetary transits
curl http://localhost:8000/planetary-transits

# Run analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{}'

# Get sector trends
curl http://localhost:8000/sector-trends?limit=5
```

### Using Python

```python
import requests

# Run analysis
response = requests.post("http://localhost:8000/analyze", json={})
result = response.json()
print(result["overall_market_sentiment"])

# Get transits
transits = requests.get("http://localhost:8000/planetary-transits").json()
print(transits)
```

---

## 🔧 Development

### Project Structure

```
AstroStocks/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── api/
│   │   └── routes/
│   │       ├── analyze.py      # Analysis endpoints
│   │       └── data.py         # Data endpoints
│   ├── database/
│   │   └── config.py           # DB configuration
│   ├── models/
│   │   └── models.py           # SQLAlchemy models
│   ├── schemas/
│   │   └── schemas.py          # Pydantic schemas
│   └── services/
│       ├── astrology_engine.py # Core astrology logic
│       ├── ai_service.py       # AI integration
│       └── mock_data.py        # Test data
├── alembic/                    # Database migrations
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

### Running Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Adding New Features

1. Add models in `app/models/models.py`
2. Create Pydantic schemas in `app/schemas/schemas.py`
3. Implement business logic in `app/services/`
4. Create API routes in `app/api/routes/`
5. Update migrations with `alembic revision --autogenerate`

---

## 🌍 Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI (Python 3.11) |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Validation | Pydantic |
| Container | Docker & Docker Compose |
| Server | Uvicorn |

---

## 📈 Future Enhancements

- [ ] Real OpenAI/Claude API integration
- [ ] Actual ephemeris data (Swiss Ephemeris)
- [ ] Real-time stock data APIs (NSE, Yahoo Finance)
- [ ] Historical correlation analysis
- [ ] Machine learning model for accuracy validation
- [ ] User authentication & authorization
- [ ] WebSocket support for real-time updates
- [ ] React/Flutter frontend
- [ ] Celery for background tasks
- [ ] Redis caching layer

---

## 📝 Environment Variables

Create a `.env` file with:

```env
DATABASE_URL=postgresql://astrofinance_user:astrofinance_pass@localhost:5432/astrofinance_db
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🤝 Contributing

This is currently an MVP. Future contributions welcome for:
- Real API integrations
- Frontend development
- ML model training
- Ephemeris integration
- Testing & documentation

---

## 📄 License

© 2025 AstroFinanceAI - Built by Avinash Chandan

---

## 🔗 Quick Links

- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

For questions or support, please open an issue on the repository.


# 🪐 AstroStocks - Astrological Stock Predictions

> **Combining Vedic Astrology with Stock Market Analytics**

A full-stack application that merges Vedic Astrology (Jyotish Shastra) with stock market data to generate AI-driven predictions for different sectors and stocks.

## 📁 Project Structure

```
astrostocks/
├── astrostocks-backend/          # FastAPI Python backend
│   ├── app/                      # Main application code
│   ├── alembic/                  # Database migrations
│   └── requirements.txt          # Python dependencies
├── astrostocks-frontend/         # Next.js TypeScript frontend
│   ├── app/                      # Next.js app router pages
│   ├── components/               # React components
│   ├── lib/                      # Utilities and API client
│   ├── prisma/                   # Database schema
│   └── package.json              # Node dependencies
└── ephe/                         # Swiss Ephemeris data files
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- PostgreSQL database

### Setup

1. **Start the database** (if not already running):
   ```bash
   docker-compose up -d  # From any directory
   ```

2. **Backend Setup:**
   ```bash
   cd astrostocks-backend
   source venv/bin/activate  # or create venv if needed
   pip install -r requirements.txt
   
   # Create all tables (one-time setup)
   python3 scripts/create_all_tables.py
   
   # Populate sectors
   python3 scripts/populate_sectors.py
   
   # Start server
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Frontend Setup:**
   ```bash
   cd astrostocks-frontend
   npm install
   
   # Create auth tables (one-time setup)
   DATABASE_URL="postgresql://astrofinance_user:astrofinance_pass@localhost:5432/astrofinance_db" \
     node scripts/create-auth-tables.js
   
   # Start dev server
   npm run dev
   ```

4. **Visit the application:**
   - Frontend: http://localhost:3000
   - Backend API docs: http://localhost:8000/docs

## ✨ Features

### Backend
- ✅ FastAPI with automatic OpenAPI docs
- ✅ SSE streaming for real-time predictions
- ✅ Intelligent caching system
- ✅ Swiss Ephemeris for planetary calculations
- ✅ AI-powered insights (DeepSeek)
- ✅ 40+ Indian stock sectors
- ✅ Market data integration (Alpha Vantage)

### Frontend
- ✅ Next.js 14+ with App Router
- ✅ TypeScript throughout
- ✅ Tailwind CSS with custom astronomy theme
- ✅ Authentication (login/signup)
- ✅ Protected dashboard
- ✅ Real-time streaming UI
- ✅ Date range filtering
- ✅ Planetary transit visualization
- ✅ Responsive design

### API Endpoints

**Standard:**
- `POST /predict` - Generate market predictions
- `POST /analyze` - Basic sector analysis
- `POST /analyze/enhanced` - Enhanced analysis
- `GET /sectors` - List all sectors
- `GET /data/planetary-transits` - Current planetary positions

**Streaming (SSE):**
- `POST /predict/stream` - Stream predictions
- `POST /analyze/stream` - Stream analysis
- `POST /analyze/enhanced/stream` - Stream enhanced analysis

## 🧪 Testing

### Test Backend:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"date":"2025-11-01"}'
```

### Test Frontend:
```bash
# Start servers, then visit http://localhost:3000
# Create account, login, and explore dashboard
```

## 📚 Documentation

- Backend API: http://localhost:8000/docs
- API Quick Reference: `API_QUICK_REFERENCE.md`
- Usage Guide: `docs/USAGE_GUIDE.md`
- Caching: `CACHING_IMPLEMENTATION.md`

## 🛠️ Tech Stack

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- Alembic (Migrations)
- pyswisseph (Astronomy calculations)
- DeepSeek API (AI insights)
- PostgreSQL (Database)

**Frontend:**
- Next.js 14+ (React framework)
- TypeScript
- Tailwind CSS v4
- NextAuth.js (Authentication)
- Prisma (ORM)
- Framer Motion (Animations)

## 📄 License

MIT License

## 🙏 Acknowledgments

- Swiss Ephemeris for precise planetary calculations
- DeepSeek for AI-powered insights
- Indian stock market sectors classification


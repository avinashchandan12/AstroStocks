# 🪐 AstroFinanceAI - Quick Reference Card

## ⚡ Start Application (2 Steps)

```bash
# 1. Start services
docker-compose up -d

# 2. Run migrations (wait 10 seconds first)
docker-compose exec api alembic upgrade head
```

**Access**: http://localhost:8000/docs

---

## 🎯 Essential Commands

```bash
# Stop everything
docker-compose down

# View logs
docker-compose logs -f api

# Restart API
docker-compose restart api

# Run tests
python test_api.py

# Local development (without Docker)
source venv/bin/activate
uvicorn app.main:app --reload
```

---

## 🌐 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/docs` | GET | Interactive API documentation |
| `/analyze` | POST | Generate astrological predictions |
| `/planetary-transits` | GET | Current planetary positions |
| `/sector-trends` | GET | Latest predictions from DB |
| `/stocks` | GET | Sample stock data |
| `/sectors` | GET | Available sectors |
| `/health` | GET | Health check |

---

## 🧪 Quick Test

```bash
# Test analysis endpoint
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{}'

# Get transits
curl http://localhost:8000/planetary-transits

# Health check
curl http://localhost:8000/health
```

---

## 📁 Key Files

```
app/services/astrology_engine.py  # Core astrology logic
app/services/ai_service.py        # AI integration
app/api/routes/analyze.py         # Main endpoint
app/main.py                       # FastAPI app
docker-compose.yml                # Docker config
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | `lsof -i :8000` then `kill -9 <PID>` |
| DB connection error | `docker-compose restart postgres` |
| Migration failed | `docker-compose down -v` then restart |
| Import errors | `source venv/bin/activate` |

---

## 📚 Documentation

- **Setup**: `QUICKSTART.md`
- **Full Guide**: `README.md`
- **Deploy**: `DEPLOY.md`
- **Status**: `PROJECT_STATUS.md`
- **Complete**: `IMPLEMENTATION_COMPLETE.md`

---

## 🎯 What Works

✅ Vedic Astrology Engine (9 planets, 12 signs, 5 elements)  
✅ AI Service Layer (mock, ready for real LLM)  
✅ 7 API Endpoints (all functional)  
✅ PostgreSQL Database (3 tables)  
✅ Docker Setup (2 services)  
✅ Mock Data (15 stocks, 9 transits)  
✅ Auto-generated Docs  
✅ Database Migrations  

---

## 🔮 What's Next

1. Add real stock API (Yahoo Finance)
2. Integrate OpenAI/Claude
3. Build React frontend
4. Add user authentication
5. Deploy to cloud

---

## 🆘 Emergency Reset

```bash
docker-compose down -v
docker-compose up --build
sleep 10
docker-compose exec api alembic upgrade head
```

---

**Quick Start**: http://localhost:8000/docs

**Built with Vedic Astrology + FastAPI + PostgreSQL**


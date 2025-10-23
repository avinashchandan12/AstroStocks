# Quick Start: Real-Time Market Data System

## 🚀 5-Minute Setup

### Step 1: Get Alpha Vantage API Key (2 minutes)

1. Visit: https://www.alphavantage.co/support/#api-key
2. Enter your email
3. Copy the API key you receive

### Step 2: Configure Environment (1 minute)

Create `.env` file in project root:

```bash
cat > .env << 'EOF'
# Database
DATABASE_URL=postgresql://astrofinance_user:astrofinance_pass@localhost:5432/astrofinance_db

# Alpha Vantage API
ALPHA_VANTAGE_API_KEY=PASTE_YOUR_KEY_HERE

# Market Data
NSE_STOCKS=RELIANCE,TCS,HDFCBANK,INFY,TATASTEEL
USE_REAL_MARKET_DATA=true
MARKET_DATA_CACHE_TTL_HOURS=1

# DeepSeek (Optional)
DEEPSEEK_API_KEY=your_key_here
USE_AI_API=false

# Ephemeris
USE_REAL_EPHEMERIS=true
EOF
```

**Replace `PASTE_YOUR_KEY_HERE` with your actual Alpha Vantage API key!**

### Step 3: Start the System (2 minutes)

```bash
# Rebuild and start Docker containers
docker-compose down
docker-compose up --build -d

# Run database migration
docker-compose exec api alembic upgrade head

# Wait for API to be ready (10-15 seconds)
sleep 15

# Check health
curl http://localhost:8000/health
```

### Step 4: Test It! (instant)

```bash
# Fetch live market data
curl http://localhost:8000/market/stocks/live | jq '.'

# Run complete analysis
curl -X POST http://localhost:8000/analyze/enhanced \
  -H "Content-Type: application/json" \
  -d '{}' | jq '.top_recommendations'
```

---

## 📊 Example Output

### Market Data Response:
```json
{
  "success": true,
  "count": 5,
  "stocks": [
    {
      "symbol": "RELIANCE",
      "current_price": 2456.30,
      "change_percent": 1.25,
      "sector": "Energy",
      "signal": "BUY"
    }
  ]
}
```

### Analysis Response:
```json
{
  "top_recommendations": [
    {
      "rank": 1,
      "stock": {
        "symbol": "TCS",
        "sector": "Technology",
        "current_price": 3567.80,
        "signal": "BUY",
        "confidence": 0.85,
        "astrological_reasoning": "Mercury in favorable position...",
        "technical_summary": "6M Return: 15.2%, Today: +2.1%"
      },
      "score": 89.5
    }
  ]
}
```

---

## 🎯 Key Endpoints

### Get Live Stock Data
```bash
curl http://localhost:8000/market/stocks/live
```

### Get Stock Recommendations
```bash
curl -X POST http://localhost:8000/analyze/enhanced \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Get Specific Stock
```bash
curl http://localhost:8000/market/stocks/RELIANCE
```

### Force Refresh (bypass cache)
```bash
curl "http://localhost:8000/market/stocks/live?force_refresh=true"
```

---

## 📝 Test Script

Run the test script to verify everything works:

```bash
docker-compose exec api python test_alpha_vantage.py
```

Expected output:
```
✅ Quote fetched successfully!
✅ Overview fetched successfully!
✅ Historical data fetched successfully!
✅ Successfully fetched 2 stocks!
```

---

## 🔧 Troubleshooting

### Problem: "No valid Alpha Vantage API key"
**Solution:** Add your API key to `.env` file and restart:
```bash
docker-compose restart api
```

### Problem: "Connection refused"
**Solution:** Wait for PostgreSQL to start:
```bash
docker-compose logs postgres
docker-compose restart api
```

### Problem: "Module not found"
**Solution:** Rebuild container:
```bash
docker-compose up --build
```

---

## 📖 Full Documentation

See `MARKET_DATA_INTEGRATION_COMPLETE.md` for:
- Detailed architecture
- All endpoints
- Configuration options
- Advanced features

---

## ✅ Success Criteria

You're ready when:
- ✅ Health check returns {"status": "healthy"}
- ✅ Test script passes all tests
- ✅ Market endpoint returns stock data
- ✅ Analysis endpoint returns recommendations

**Happy trading with astrology! 🌟**


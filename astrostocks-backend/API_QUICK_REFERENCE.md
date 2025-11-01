# AstroFinanceAI API - Quick Reference

## 🚀 Getting Started

### Import Postman Collection
1. Open Postman
2. Click **Import**
3. Select `AstroFinanceAI.postman_collection.json`
4. Click **Import**

### Base URL
```
http://localhost:8000
```

---

## 📍 Essential Endpoints

### 🔍 Analysis

**Analyze Market (Basic)**
```
POST /analyze
```
Combines stock data with planetary transits for sector predictions.

**Analyze Market (Enhanced)**
```
POST /analyze/enhanced?use_real_data=true
```
Get top stock recommendations with BUY/HOLD/SELL signals.

---

### 🔮 Prediction

**Generate Prediction**
```
POST /predict?analyse_past=false
```
Generate market prediction based on planetary transits.

**Test Prediction**
```
POST /predict/test
```
Quick test with default values.

---

### 📊 Data

**Get Planetary Transits**
```
GET /planetary-transits
```
Current planetary positions from Swiss Ephemeris.

**Get Sector Trends**
```
GET /sector-trends?limit=10
```
Latest sector predictions from database.

**Get Nakshatra**
```
GET /nakshatra
```
Current Moon nakshatra.

---

### 📈 Market Data

**Get Live Stocks**
```
GET /market/stocks/live?force_refresh=false
```
All tracked stock data with caching.

**Get Stock Detail**
```
GET /market/stocks/RELIANCE
```
Specific stock details.

**Cache Management**
```
GET /market/cache/stats
POST /market/cache/clear-expired
```

---

## 📝 Request Examples

### Analyze Market (Basic)
```json
{
  "stocks": [
    {
      "symbol": "RELIANCE",
      "sector": "Oil & Gas",
      "past_6m_return": 15.5,
      "volatility": "Medium",
      "price_trend": "Upward"
    }
  ]
}
```

### Generate Prediction
```json
{
  "date": "2024-02-01",
  "latitude": 19.0760,
  "longitude": 72.8777,
  "timezone": "Asia/Kolkata"
}
```

---

## ⚠️ Common Issues

**503 Service Unavailable**
- Install pyswisseph for ephemeris
- Enable USE_REAL_EPHEMERIS=true

**400 Bad Request**
- Provide required stock data
- Check query parameters

**500 Internal Server Error**
- Check DeepSeek API key
- Verify database connection

---

## 📚 Full Documentation

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete details.

---

## 🔄 Update Documentation

Run the update script:
```bash
./update_api_docs.sh
# or
python3 scripts/generate_postman_collection.py
```

---

**Last Updated:** 2025-11-01 12:39:15


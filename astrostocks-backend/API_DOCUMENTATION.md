# AstroFinanceAI API Documentation

**Version:** 1.0.0  
**Base URL:** `http://localhost:8000`  
**Last Updated:** 2025-11-01 12:39:15

---

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Base Endpoints](#base-endpoints)
- [Analysis Endpoints](#analysis-endpoints)
- [Prediction Endpoints](#prediction-endpoints)
- [Data Endpoints](#data-endpoints)
- [Market Data Endpoints](#market-data-endpoints)
- [Error Handling](#error-handling)
- [Rate Limits](#rate-limits)

---

## Overview

AstroFinanceAI is a FastAPI-based REST API that combines **Vedic Astrology (Jyotish Shastra)** with **Stock Market Analytics** to provide AI-driven market predictions and insights.

### Key Features
- 🌟 Real-time planetary transit calculations using Swiss Ephemeris
- 📊 Stock market data integration via Alpha Vantage
- 🤖 AI-powered analysis using DeepSeek
- 📈 Sector-wise market predictions
- 🔄 Intelligent caching for market data

### Requirements
- Python 3.9+
- PostgreSQL database
- Swiss Ephemeris library (pyswisseph)
- DeepSeek API key
- Alpha Vantage API key

---

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

---

## Base Endpoints

### Root Endpoint

**GET** `/`

Get API information and available endpoints.

**Response:**
```json
{
  "message": "Welcome to AstroFinanceAI API",
  "description": "Combining Vedic Astrology with Stock Market Analytics",
  "version": "1.0.0",
  "docs": "/docs",
  "endpoints": {
    "analyze": "/analyze",
    "predict": "/predict",
    "planetary_transits": "/planetary-transits",
    "sector_trends": "/sector-trends"
  }
}
```

### Health Check

**GET** `/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "AstroFinanceAI Backend"
}
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/health"
```

---

## Analysis Endpoints

### Analyze Market (Basic)

**POST** `/analyze`

Combines stock market data with planetary transits to generate AI-driven astrological predictions for various sectors.

**Request Body:**
```json
{
  "stocks": [
    {
      "symbol": "RELIANCE",
      "sector": "Oil & Gas",
      "past_6m_return": 15.5,
      "volatility": "Medium",
      "pe_ratio": 24.2,
      "price_trend": "Upward",
      "news_sentiment": "Positive"
    }
  ],
  "transits": {
    "transits": [
      {
        "planet": "Jupiter",
        "sign": "Taurus",
        "motion": "Direct",
        "status": "Normal",
        "date": "2024-01-15"
      }
    ]
  }
}
```

**Note:** If `transits` are not provided, real ephemeris data will be automatically fetched.

**Response:**
```json
{
  "sector_predictions": [
    {
      "sector": "Chemicals",
      "planetary_influence": "Jupiter in Cancer, Saturn in Aquarius",
      "trend": "Bullish",
      "reason": "Strong positive momentum expected",
      "top_stocks": ["TATACHEM", "UPL"],
      "confidence": 0.85
    }
  ],
  "overall_market_sentiment": "Positive",
  "accuracy_estimate": "75%",
  "timestamp": "2024-01-15T10:30:00"
}
```

**Error Responses:**
- `400` - Stock data is required
- `503` - Planetary transit data unavailable
- `500` - Analysis failed

---

### Analyze Market (Enhanced)

**POST** `/analyze/enhanced`

Enhanced analysis endpoint with real market data integration. Returns top stock recommendations with buy/hold/sell signals.

**Query Parameters:**
- `use_real_data` (boolean, default: true) - Use real market data from Alpha Vantage

**Request Body:**
```json
{
  "stocks": null
}
```

**Response:**
```json
{
  "top_recommendations": [
    {
      "rank": 1,
      "stock": {
        "symbol": "TCS",
        "sector": "Technology",
        "current_price": 3425.50,
        "change_percent": 2.3,
        "signal": "BUY",
        "confidence": 0.85,
        "astrological_reasoning": "Jupiter's favorable position...",
        "technical_summary": "6M Return: 18.9%, Today: +2.3%, Volatility: Low",
        "past_6m_return": 18.9,
        "volatility": "Low"
      },
      "score": 87.5
    }
  ],
  "sector_analysis": [
    {
      "sector": "Technology",
      "trend": "Bullish",
      "planetary_influence": "Mercury in Virgo",
      "ai_insights": "Strong positive momentum...",
      "stocks_in_sector": [],
      "confidence": 0.85
    }
  ],
  "all_stocks": [],
  "overall_sentiment": "Positive",
  "timestamp": "2024-01-15T10:30:00"
}
```

**Signals:**
- `BUY` - Score ≥ 70
- `HOLD` - Score 40-70
- `SELL` - Score ≤ 40

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/analyze/enhanced?use_real_data=true" \
  -H "Content-Type: application/json" \
  -d '{"stocks": null}'
```

---

### Analysis Health Check

**GET** `/analyze/health`

Health check for analysis service.

**Response:**
```json
{
  "status": "healthy",
  "service": "AstroFinanceAI Analysis Service",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## Prediction Endpoints

### Generate Market Prediction

**POST** `/predict`

Generate market prediction based on planetary transits for a specific date/time/location.

**Query Parameters:**
- `analyse_past` (boolean, default: false) - Include historical market data analysis
- `stream` (boolean, default: false) - Stream the LLM response (future enhancement)

**Request Body:**
```json
{
  "date": "2024-02-01",
  "time": "09:30:00",
  "latitude": 19.0760,
  "longitude": 72.8777,
  "timezone": "Asia/Kolkata"
}
```

**All fields are optional.** If not provided, defaults to current date/time.

**Response:**
```json
{
  "prediction_date": "2024-02-01",
  "location": {
    "latitude": 19.0760,
    "longitude": 72.8777,
    "timezone": "Asia/Kolkata"
  },
  "planetary_transits": [
    {
      "planet": "Jupiter",
      "longitude": 45.5,
      "latitude": 0.0,
      "sign": "Taurus",
      "degree_in_sign": 15.5,
      "dignity": "Own",
      "retrograde": false,
      "motion": "Direct",
      "speed": 0.25
    }
  ],
  "market_prediction": {
    "overall_sentiment": "Bullish",
    "sector_predictions": [],
    "key_influences": [],
    "ai_analysis": "Comprehensive market analysis..."
  },
  "past_market_data": null,
  "confidence": 0.75
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/predict?analyse_past=false" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2024-02-01",
    "latitude": 19.0760,
    "longitude": 72.8777,
    "timezone": "Asia/Kolkata"
  }'
```

---

### Test Prediction

**POST** `/predict/test`

Test endpoint for prediction service with default values.

**Response:**
```json
{
  "message": "Test prediction successful",
  "prediction_date": "2024-01-15",
  "planetary_transits_count": 9,
  "overall_sentiment": "Neutral",
  "confidence": 0.65
}
```

---

### Prediction Health Check

**GET** `/predict/health`

Health check for prediction service.

**Response:**
```json
{
  "status": "healthy",
  "service": "AstroFinanceAI Prediction Service",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## Data Endpoints

### Get Planetary Transits

**GET** `/planetary-transits`

Get current planetary transit data from Swiss Ephemeris.

**Response:**
```json
{
  "transits": [
    {
      "planet": "Sun",
      "sign": "Capricorn",
      "motion": "Direct",
      "status": "Exalted",
      "date": "2024-01-15",
      "longitude": 275.3,
      "nakshatra": "Dhanishta"
    }
  ],
  "timestamp": "2024-01-15T10:30:00",
  "source": "Swiss Ephemeris"
}
```

**Error:**
- `503` - Swiss Ephemeris not available

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/planetary-transits"
```

---

### Get Sector Trends

**GET** `/sector-trends`

Get latest sector predictions from database.

**Query Parameters:**
- `limit` (integer, default: 10, range: 1-100) - Number of recent predictions to return
- `sector` (string, optional) - Filter by specific sector

**Response:**
```json
[
  {
    "id": 1,
    "sector": "Technology",
    "planetary_influence": "Mercury in Virgo",
    "trend": "Bullish",
    "reason": "Strong AI insights...",
    "top_stocks": ["TCS", "INFY", "WIPRO"],
    "accuracy_estimate": 0.85,
    "created_at": "2024-01-15T10:30:00"
  }
]
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/sector-trends?limit=20&sector=Technology"
```

---

### Get Live Planetary Positions

**GET** `/planetary-positions/live`

Get real-time planetary positions using Swiss Ephemeris with detailed astronomical data.

**Query Parameters:**
- `date_str` (string, optional) - Date in YYYY-MM-DD format (defaults to now)

**Response:**
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "calculation_date": "2024-01-15T10:30:00",
  "positions": [
    {
      "planet": "Jupiter",
      "longitude": 45.5,
      "latitude": 0.0,
      "sign": "Taurus",
      "degree_in_sign": 15.5,
      "dignity": "Own",
      "retrograde": false,
      "motion": "Direct",
      "speed": 0.25
    }
  ],
  "moon_nakshatra": {
    "name": "Rohini",
    "pada": 2,
    "ruler": "Venus",
    "moon_position": {
      "longitude": 60.25,
      "sign": "Gemini"
    }
  },
  "count": 9,
  "source": "Swiss Ephemeris"
}
```

**Error:**
- `503` - Swiss Ephemeris not available
- `400` - Invalid date format
- `500` - Error calculating positions

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/planetary-positions/live?date_str=2024-02-01"
```

---

### Get Current Nakshatra

**GET** `/nakshatra`

Get current Moon nakshatra (lunar mansion).

**Response (Success):**
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "nakshatra": "Rohini",
  "pada": 2,
  "moon_longitude": 60.25,
  "moon_sign": "Gemini",
  "source": "Swiss Ephemeris"
}
```

**Response (Error):**
```json
{
  "error": "Swiss Ephemeris not available",
  "message": "Install pyswisseph and set USE_REAL_EPHEMERIS=true"
}
```

---

## Market Data Endpoints

### Get Live Stocks

**GET** `/market/stocks/live`

Get current market data for tracked NSE stocks with caching (1-hour TTL).

**Query Parameters:**
- `force_refresh` (boolean, default: false) - Force refresh from Alpha Vantage

**Response:**
```json
{
  "success": true,
  "count": 15,
  "stocks": [
    {
      "symbol": "RELIANCE",
      "sector": "Oil & Gas",
      "current_price": 2450.50,
      "change_percent": 1.5,
      "past_6m_return": 12.3,
      "volatility": "Medium",
      "timestamp": "2024-01-15T10:30:00"
    }
  ],
  "symbols_requested": ["RELIANCE", "TCS", "INFY"],
  "force_refresh": false
}
```

**Error:**
- `503` - Real market data disabled
- `400` - No stocks configured
- `500` - Error fetching stock data

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/market/stocks/live?force_refresh=false"
```

---

### Get Stock Detail

**GET** `/market/stocks/{symbol}`

Get detailed data for a specific stock.

**Path Parameters:**
- `symbol` (string) - Stock symbol (e.g., RELIANCE, TCS)

**Query Parameters:**
- `force_refresh` (boolean, default: false) - Force refresh from Alpha Vantage

**Response:**
```json
{
  "success": true,
  "stock": {
    "symbol": "RELIANCE",
    "sector": "Oil & Gas",
    "current_price": 2450.50,
    "change_percent": 1.5,
    "past_6m_return": 12.3,
    "volatility": "Medium"
  }
}
```

**Error:**
- `404` - Stock not found
- `503` - Real market data disabled

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/market/stocks/RELIANCE"
```

---

### Get Cache Statistics

**GET** `/market/cache/stats`

Get cache statistics for market data.

**Response:**
```json
{
  "success": true,
  "cache_stats": {
    "total_entries": 15,
    "valid_entries": 15,
    "expired_entries": 0
  }
}
```

---

### Clear Expired Cache

**POST** `/market/cache/clear-expired`

Clear expired cache entries.

**Response:**
```json
{
  "success": true,
  "message": "Expired cache entries cleared",
  "cache_stats": {
    "total_entries": 10,
    "valid_entries": 10,
    "expired_entries": 0
  }
}
```

---

### Get Tracked Symbols

**GET** `/market/tracked-symbols`

Get list of currently tracked stock symbols.

**Response:**
```json
{
  "success": true,
  "count": 3,
  "symbols": ["RELIANCE", "TCS", "INFY"]
}
```

---

## Error Handling

All endpoints return standard HTTP status codes:

- `200 OK` - Request successful
- `400 Bad Request` - Invalid request parameters
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service temporarily unavailable

**Error Response Format:**
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Rate Limits

Currently, there are no rate limits enforced. However, please be respectful of the API resources.

---

## Environment Configuration

The API requires the following environment variables:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/astrofinanceai

# Market Data
USE_REAL_MARKET_DATA=true
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
NSE_STOCKS=RELIANCE,TCS,INFY,HDFCBANK,ICICIBANK,BHARTIARTL,WIPRO,ONGC,SBIN,LT

# Ephemeris
USE_REAL_EPHEMERIS=true
EPHEMERIS_PATH=./ephe
AYANAMSA=lahiri

# AI
USE_AI_API=true
DEEPSEEK_API_KEY=your_deepseek_key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
```

---

## Interactive Documentation

The API provides interactive documentation via Swagger UI and ReDoc:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Contact: support@astrofinanceai.com

---

**Documentation Generated:** 2025-11-01 12:39:15


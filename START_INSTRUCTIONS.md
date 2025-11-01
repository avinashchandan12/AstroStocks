================================================================================
🎯 ASTROSTOCKS - STARTUP INSTRUCTIONS
================================================================================

## Prerequisites Check

✅ Docker running (for PostgreSQL)
✅ Python 3.11+ installed
✅ Node.js 18+ installed

## Database Setup (One-Time)

The database is configured and all tables have been created.
No additional setup needed.

## Starting the Application

### Terminal 1 - Backend:

```bash
cd astrostocks-backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
  INFO:     Uvicorn running on http://0.0.0.0:8000
  ✅ Swiss Ephemeris initialized
  ✅ DeepSeek API client initialized

### Terminal 2 - Frontend:

```bash
cd astrostocks-frontend
npm run dev
```

Expected output:
  ✓ Ready in XXXms
  ○ Local: http://localhost:3000

## Access Points

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs
- Backend ReDoc: http://localhost:8000/redoc

## First Steps

1. Visit http://localhost:3000
2. Click "Sign up" 
3. Enter your details
4. You'll be redirected to the dashboard
5. Click "Generate Predictions" or "Stream Predictions"
6. Explore sector predictions and planetary transits!

## Features to Try

✨ Sector Predictions - View AI-powered sector analysis
🌍 Planetary Transits - See current planetary positions
📅 Date Filtering - Generate predictions for different dates
⚡ Streaming - Watch predictions generate in real-time
📊 Dashboard - Beautiful, responsive UI

================================================================================

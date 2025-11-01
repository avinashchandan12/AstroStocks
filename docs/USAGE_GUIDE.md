# AstroFinanceAI API - Usage Guide

## 📚 Documentation Overview

This project includes comprehensive API documentation in multiple formats:

### Files Created

1. **API_DOCUMENTATION.md** (13KB)
   - Complete API reference
   - All endpoints documented
   - Request/response examples
   - Error handling guide
   - Environment configuration

2. **API_QUICK_REFERENCE.md** (2.3KB)
   - Quick lookup guide
   - Essential endpoints
   - Common examples
   - Troubleshooting tips

3. **AstroFinanceAI.postman_collection.json** (11KB)
   - Postman collection
   - Pre-configured requests
   - All endpoints included
   - Ready to import

4. **scripts/generate_postman_collection.py**
   - Auto-update script
   - Parses routes
   - Updates dates
   - Validates JSON

5. **update_api_docs.sh**
   - Convenience wrapper
   - One-command updates

---

## 🚀 Quick Start

### Import Postman Collection

1. Open Postman app
2. Click **Import** button (top left)
3. Select **File** tab
4. Choose `AstroFinanceAI.postman_collection.json`
5. Click **Import**

### Configure Environment

The collection uses a `base_url` variable:
- Default: `http://localhost:8000`
- Edit in Postman: Click collection → Variables tab

### Test Your API

1. Make sure your FastAPI server is running:
   ```bash
   cd /Users/avinash2/AstroStocks
   python3 -m uvicorn app.main:app --reload
   ```

2. In Postman, navigate to **Base Endpoints**
3. Click **Root - API Info**
4. Click **Send**

---

## 📝 Updating Documentation

### Automatic Updates

Run the update script to refresh dates:
```bash
./update_api_docs.sh
```

Or manually:
```bash
python3 scripts/generate_postman_collection.py
```

### What Gets Updated

- ✅ `API_DOCUMENTATION.md` - Last Updated date
- ✅ `API_QUICK_REFERENCE.md` - Last Updated date
- ✅ Validates `AstroFinanceAI.postman_collection.json`

### Adding New Endpoints

When you add new API endpoints:

1. **Update API_DOCUMENTATION.md**
   - Add endpoint to appropriate section
   - Include request/response examples
   - Document parameters

2. **Update AstroFinanceAI.postman_collection.json**
   - Add new item to appropriate folder
   - Include method, URL, headers, body
   - Add description

3. **Update this guide** (if needed)

---

## 📍 Endpoint Categories

### Base Endpoints
- Root info
- Health checks

### Analysis
- Basic market analysis
- Enhanced analysis with recommendations
- Health checks

### Prediction
- Generate market predictions
- Test predictions
- Health checks

### Data
- Planetary transits
- Sector trends
- Live planetary positions
- Nakshatra data

### Market Data
- Live stock prices
- Stock details
- Cache management
- Tracked symbols

---

## 🔧 Troubleshooting

### Postman Import Fails

**Error:** Invalid JSON
- Run: `python3 -c "import json; json.load(open('AstroFinanceAI.postman_collection.json'))"`
- Check for syntax errors

**Error:** Collection not found
- Verify file exists: `ls -lh AstroFinanceAI.postman_collection.json`
- Check file permissions

### API Requests Fail

**503 Service Unavailable**
- Check if server is running
- Verify Swiss Ephemeris is installed
- Enable USE_REAL_EPHEMERIS=true

**400 Bad Request**
- Review request body format
- Check required parameters
- Validate JSON syntax

**500 Internal Server Error**
- Check server logs
- Verify DeepSeek API key
- Ensure database is connected

---

## 📊 Example Workflow

### 1. Get Planetary Data
```
GET /planetary-transits
→ Returns current planetary positions
```

### 2. Get Live Stock Data
```
GET /market/stocks/live
→ Returns cached stock prices
```

### 3. Generate Analysis
```
POST /analyze/enhanced?use_real_data=true
→ Returns top recommendations with signals
```

### 4. Generate Prediction
```
POST /predict
{
  "date": "2024-02-01",
  "latitude": 19.0760,
  "longitude": 72.8777
}
→ Returns market prediction
```

---

## 📖 Additional Resources

### Interactive Documentation
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Support
- See main README.md for setup instructions
- Check API_DOCUMENTATION.md for detailed specs
- Review API_QUICK_REFERENCE.md for quick lookup

---

## 🎯 Best Practices

### Postman Collection
- Use variables for base_url
- Organize requests in folders
- Add descriptions to requests
- Save examples as tests

### API Testing
- Start with health checks
- Test basic endpoints first
- Verify error handling
- Test edge cases

### Documentation
- Keep examples up-to-date
- Document breaking changes
- Add version notes
- Include migration guides

---

**Last Updated:** 2025-11-01


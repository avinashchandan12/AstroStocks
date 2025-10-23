# 🔑 API Keys Setup Guide for AstroFinanceAI

## 📝 Step-by-Step Setup

### 1. Create Your `.env` File

Create a file called `.env` in the project root directory:

```bash
cd /Users/avinash2/AstroStocks
touch .env
```

### 2. Add Your Configuration

Open the `.env` file in your editor and add:

```env
DATABASE_URL=postgresql://astrofinance_user:astrofinance_pass@localhost:5432/astrofinance_db

# DeepSeek API Configuration
DEEPSEEK_API_KEY=sk-your-actual-deepseek-api-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat

# Enable AI features (set to "true" to use DeepSeek, "false" to use mock)
USE_AI_API=true
```

### 3. Get Your DeepSeek API Key

1. Visit https://platform.deepseek.com
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (it starts with `sk-`)
6. Replace `sk-your-actual-deepseek-api-key-here` in your `.env` file

### 4. Install Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Install OpenAI package (DeepSeek is compatible)
pip install openai

# Or reinstall all dependencies
pip install -r requirements.txt
```

### 5. Restart Your Application

```bash
# If using Docker
docker-compose down
docker-compose up --build

# If running locally
# Press Ctrl+C to stop, then restart:
uvicorn app.main:app --reload
```

## 🎯 Configuration Options

### Use DeepSeek API

```env
USE_AI_API=true
DEEPSEEK_API_KEY=sk-your-key-here
```

### Use Mock AI (No API calls)

```env
USE_AI_API=false
```

### Available DeepSeek Models

```env
# For general chat/reasoning (recommended)
DEEPSEEK_MODEL=deepseek-chat

# For code-focused tasks
DEEPSEEK_MODEL=deepseek-coder
```

## ✅ Verify Setup

After restarting, you should see in the logs:

```
✅ DeepSeek API client initialized
```

If you see this instead:
```
⚠️  DeepSeek API key not configured. Using mock AI responses.
```

Then check your `.env` file configuration.

## 🧪 Test DeepSeek Integration

```bash
# Test the API with DeepSeek enabled
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{}'
```

With DeepSeek enabled, the `ai_insights` field will contain AI-generated content instead of mock responses.

## 🔐 Security Reminders

✅ **DO**:
- Keep `.env` file local (already in `.gitignore`)
- Never share your API keys
- Use different keys for dev/prod
- Rotate keys regularly

❌ **DON'T**:
- Commit `.env` to git
- Share keys in chat/email
- Use production keys in development

## 🆘 Troubleshooting

### "OpenAI package not installed"

```bash
source venv/bin/activate
pip install openai
```

### "DeepSeek API key not configured"

Check that:
1. `.env` file exists in project root
2. `DEEPSEEK_API_KEY` is set correctly
3. Key starts with `sk-`
4. No extra spaces around the key

### "DeepSeek API call failed"

The system automatically falls back to mock responses. Check:
1. Internet connection
2. API key is valid
3. DeepSeek API service status

### Docker not picking up .env changes

```bash
docker-compose down
docker-compose up --build
```

## 📊 Comparison: Mock vs DeepSeek

### Mock Response (USE_AI_API=false)
```json
{
  "ai_insights": "Strong positive momentum expected in Technology sector. Mercury's favorable position supports growth."
}
```

### DeepSeek Response (USE_AI_API=true)
```json
{
  "ai_insights": "The Technology sector shows promising momentum with Mercury's exaltation in Virgo, traditionally linked to analytical prowess and communication—key drivers in tech. However, Rahu's retrograde motion in Pisces suggests potential volatility from foreign markets or innovative disruptions. Investors should watch for breakthrough announcements while maintaining diversification."
}
```

## 🎓 Advanced Configuration

### Use OpenAI Instead of DeepSeek

```env
# OpenAI Configuration (alternative)
DEEPSEEK_API_KEY=your_openai_key_here
DEEPSEEK_BASE_URL=https://api.openai.com/v1
DEEPSEEK_MODEL=gpt-4
USE_AI_API=true
```

### Add Multiple API Providers (Future)

You can extend the code to support multiple providers:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Local LLMs (Ollama, LM Studio)
- Azure OpenAI

## 📞 Support

If you need help:
1. Check this guide
2. Verify logs for error messages
3. Test with `USE_AI_API=false` first
4. Ensure all dependencies are installed

---

**Your `.env` file is safe**: It's already in `.gitignore` and won't be committed to version control! 🔒


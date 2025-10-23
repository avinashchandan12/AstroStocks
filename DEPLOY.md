# 🚀 AstroFinanceAI - Deployment Guide

## Quick Deploy Commands

### 🐳 Docker Deployment (Easiest)

```bash
# 1. Navigate to project
cd /Users/avinash2/AstroStocks

# 2. Start all services
docker-compose up -d

# 3. Wait for PostgreSQL to be ready (10 seconds)
sleep 10

# 4. Run database migrations
docker-compose exec api alembic upgrade head

# 5. Verify it's working
curl http://localhost:8000/health

# 6. Test the analysis endpoint
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 📊 Access the Application

Once running, access:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs ⭐
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 💻 Local Development Setup

### Prerequisites
- Python 3.11+ or Docker
- PostgreSQL 15+ (if not using Docker)

### With Docker (Recommended)

```bash
# Start services
docker-compose up

# The API will be available at http://localhost:8000
# Auto-reloads on code changes
```

### Without Docker

```bash
# 1. Start PostgreSQL (if you have it locally)
brew services start postgresql@15
# OR use Docker just for PostgreSQL
docker-compose up -d postgres

# 2. Activate virtual environment
source venv/bin/activate

# 3. Run migrations
alembic upgrade head

# 4. Start the API
uvicorn app.main:app --reload

# OR use the startup script
./run_local.sh
```

---

## 🧪 Testing the Deployment

### Quick Test Script

Run the comprehensive test suite:

```bash
# Ensure API is running, then:
python test_api.py
```

### Manual Tests

```bash
# Health check
curl http://localhost:8000/health

# Get planetary transits
curl http://localhost:8000/planetary-transits

# Get available sectors
curl http://localhost:8000/sectors

# Get sample stocks
curl http://localhost:8000/stocks

# Run full analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{}'

# Get saved predictions
curl http://localhost:8000/sector-trends?limit=5
```

---

## 🔧 Configuration

### Environment Variables

Edit `.env` file (create from `.env.example`):

```env
DATABASE_URL=postgresql://astrofinance_user:astrofinance_pass@localhost:5432/astrofinance_db
OPENAI_API_KEY=your_openai_api_key_here  # For future AI integration
```

### Changing Ports

Edit `docker-compose.yml`:

```yaml
services:
  postgres:
    ports:
      - "5433:5432"  # Change 5433 to your preferred port
  
  api:
    ports:
      - "8001:8000"  # Change 8001 to your preferred port
```

---

## 📦 Database Management

### View Current Migration Status

```bash
alembic current
```

### Run Migrations

```bash
# Upgrade to latest
alembic upgrade head

# Downgrade one version
alembic downgrade -1

# View migration history
alembic history
```

### Reset Database

```bash
# Docker
docker-compose down -v
docker-compose up -d
docker-compose exec api alembic upgrade head

# Local
dropdb astrofinance_db
createdb astrofinance_db
alembic upgrade head
```

---

## 🐛 Troubleshooting

### API Won't Start

```bash
# Check logs
docker-compose logs api

# Restart services
docker-compose restart
```

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose ps

# Check PostgreSQL logs
docker-compose logs postgres

# Verify connection
docker-compose exec postgres psql -U astrofinance_user -d astrofinance_db -c "SELECT 1;"
```

### Port Already in Use

```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process (replace PID)
kill -9 <PID>

# Or change the port in docker-compose.yml
```

### Clean Start

```bash
# Stop everything
docker-compose down -v

# Remove containers
docker-compose rm -f

# Rebuild and start
docker-compose up --build
```

---

## 🌐 Production Deployment

### Using Docker on Cloud

#### AWS ECS / GCP Cloud Run / Azure Container Instances

1. **Build and push image**:
   ```bash
   docker build -t astrofinance-api .
   docker tag astrofinance-api your-registry/astrofinance-api:latest
   docker push your-registry/astrofinance-api:latest
   ```

2. **Set environment variables**:
   - `DATABASE_URL` - Your PostgreSQL connection string
   - `OPENAI_API_KEY` - Your OpenAI key (when ready)

3. **Deploy**:
   - Follow your cloud provider's container deployment guide

#### Render.com (Easiest)

1. Connect your GitHub repository
2. Select "Docker" as deployment type
3. Set environment variables
4. Deploy!

### Using Regular Server

```bash
# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📊 Monitoring

### Health Check Endpoint

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "AstroFinanceAI Backend"
}
```

### Database Check

```bash
docker-compose exec postgres psql -U astrofinance_user -d astrofinance_db \
  -c "SELECT COUNT(*) FROM sector_predictions;"
```

---

## 🔐 Security Considerations

### For Production

1. **Change default credentials**:
   ```env
   DATABASE_URL=postgresql://your_secure_user:your_secure_pass@...
   ```

2. **Use HTTPS**:
   - Set up SSL/TLS certificates
   - Use nginx or cloud load balancer

3. **Add authentication**:
   - Implement JWT tokens
   - Add API key validation

4. **Rate limiting**:
   - Use slowapi or similar
   - Set up API gateway

5. **Environment variables**:
   - Never commit `.env` file
   - Use secrets management service

---

## 📈 Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml
api:
  deploy:
    replicas: 3
```

### Add Load Balancer

```yaml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
  depends_on:
    - api
```

### Database Connection Pooling

Already configured in SQLAlchemy! Just adjust pool size if needed in `app/database/config.py`.

---

## 🎯 Performance Tips

1. **Use uvicorn workers**:
   ```bash
   uvicorn app.main:app --workers 4
   ```

2. **Add Redis caching** (future):
   ```python
   # Cache planetary transits (they don't change often)
   @cache(expire=3600)
   def get_transits():
       ...
   ```

3. **Database indexing**:
   Already configured on important columns!

4. **Enable compression**:
   ```python
   from fastapi.middleware.gzip import GZIPMiddleware
   app.add_middleware(GZIPMiddleware)
   ```

---

## 📝 Maintenance

### Backup Database

```bash
docker-compose exec postgres pg_dump -U astrofinance_user astrofinance_db > backup.sql
```

### Restore Database

```bash
docker-compose exec -T postgres psql -U astrofinance_user astrofinance_db < backup.sql
```

### View Logs

```bash
# All logs
docker-compose logs -f

# Just API logs
docker-compose logs -f api

# Last 100 lines
docker-compose logs --tail=100 api
```

---

## ✅ Deployment Checklist

- [ ] PostgreSQL is running
- [ ] Environment variables are set
- [ ] Migrations are applied
- [ ] API starts without errors
- [ ] Health check returns 200
- [ ] `/docs` page is accessible
- [ ] Analysis endpoint works
- [ ] Predictions are saved to database
- [ ] All tests pass

---

## 🆘 Support

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Verify database: `docker-compose exec postgres psql -U astrofinance_user -d astrofinance_db`
3. Test endpoints: Use `/docs` interactive interface
4. Run test suite: `python test_api.py`
5. Review [QUICKSTART.md](QUICKSTART.md) and [README.md](README.md)

---

**Ready to deploy!** 🚀

For detailed API documentation, visit http://localhost:8000/docs after deployment.


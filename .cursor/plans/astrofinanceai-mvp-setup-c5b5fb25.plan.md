<!-- c5b5fb25-1f1f-496e-9235-07e17c67b123 c5cfe301-2012-419f-9c8d-1ba30cfd7cb2 -->
# AstroFinanceAI MVP Setup

## Project Structure Setup

- Create FastAPI project with proper directory structure:
- `app/` - main application code
- `app/api/routes/` - API endpoints
- `app/models/` - SQLAlchemy models
- `app/schemas/` - Pydantic schemas
- `app/services/` - business logic (AI service, astrology engine)
- `app/database/` - database configuration
- `alembic/` - migrations
- Add `requirements.txt` with FastAPI, SQLAlchemy, PostgreSQL driver, Alembic, Pydantic

## Docker & Database Configuration

- Create `docker-compose.yml` with PostgreSQL service
- Create `.env` file template with DATABASE_URL and OPENAI_API_KEY
- Set up `app/database/config.py` for SQLAlchemy connection
- Create SQLAlchemy models for `stocks`, `transits`, `sector_predictions` tables

## Database Migrations

- Initialize Alembic
- Create initial migration with all three tables (stocks, transits, sector_predictions)

## Astrology Engine Core

- Create `app/services/astrology_engine.py` with:
- Planet-to-element mapping dictionary
- Element-to-sector mapping dictionary
- Function to analyze planetary influences on sectors
- Basic transit interpretation logic

## Mock Data Layer

- Create `app/services/mock_data.py` with:
- Sample stock data (multiple sectors: Chemicals, Tech, Banking, etc.)
- Sample planetary transit data (Jupiter, Saturn, Mars, Venus, Rahu/Ketu)
- Helper functions to generate realistic mock responses

## AI Service Layer Structure

- Create `app/services/ai_service.py` with:
- Mock LLM response generator (structured JSON output)
- Knowledge base prompt template embedded in code
- Function to combine astrology engine output with "AI reasoning"

## API Endpoints

- Create `app/api/routes/analyze.py`:
- `POST /analyze` - main endpoint combining astrology + AI
- Accept optional stock/transit JSON, use mocks if not provided
- Return structured sector predictions
- Create `app/api/routes/data.py`:
- `GET /planetary-transits` - return current mock transit data
- `GET /sector-trends` - fetch latest predictions from database
- Set up `app/main.py` with FastAPI app initialization and route registration

## Configuration & Documentation

- Create `.env.example` with required variables
- Create `README.md` with:
- Setup instructions (Docker commands)
- API usage examples
- How to access Swagger docs at `/docs`
- Add `.gitignore` for Python projects

## Testing Setup

- Ensure Docker Compose runs successfully
- Verify database migrations apply correctly
- Test `/analyze` endpoint returns proper JSON structure
- Verify Swagger UI is accessible at `http://localhost:8000/docs`

### To-dos

- [ ] Create FastAPI project structure with all necessary directories and requirements.txt
- [ ] Set up Docker Compose, PostgreSQL, and database connection configuration
- [ ] Create SQLAlchemy models for stocks, transits, and sector_predictions tables
- [ ] Initialize Alembic and create initial database migration
- [ ] Build astrology engine with planet/element/sector mappings and transit analysis
- [ ] Create mock data generators for stocks and planetary transits
- [ ] Implement AI service layer with mock responses and knowledge base prompt
- [ ] Build /analyze, /planetary-transits, and /sector-trends endpoints
- [ ] Create README.md, .env.example, and .gitignore files
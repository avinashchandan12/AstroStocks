"""
AstroFinanceAI - Main Application Entry Point
FastAPI backend combining Vedic Astrology with Stock Market Analytics
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import analyze, data, market
from app.database.config import engine, Base

# Initialize FastAPI app
app = FastAPI(
    title="AstroFinanceAI API",
    description="Combining Vedic Astrology with Stock Market Analytics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analyze.router)
app.include_router(data.router)
app.include_router(market.router)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to AstroFinanceAI API",
        "description": "Combining Vedic Astrology with Stock Market Analytics",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "analyze": "/analyze",
            "planetary_transits": "/planetary-transits",
            "sector_trends": "/sector-trends",
            "stocks": "/stocks",
            "sectors": "/sectors"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AstroFinanceAI Backend"
    }


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler
    Note: Table creation is handled by Alembic migrations
    This is just a placeholder for any startup logic
    """
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


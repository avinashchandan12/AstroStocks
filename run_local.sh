#!/bin/bash

# AstroFinanceAI - Local Development Startup Script

echo "🪐 Starting AstroFinanceAI Local Development Environment"
echo "========================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

echo ""
echo "✓ Environment ready!"
echo ""
echo "Note: PostgreSQL must be running for migrations and the API"
echo "You can start it with Docker: docker-compose up -d postgres"
echo ""
echo "To run migrations: alembic upgrade head"
echo "To start the API: uvicorn app.main:app --reload"
echo ""
echo "Starting API server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


#!/bin/bash

# Script to run migrations for AstroStocks
# Works for both Docker and local environments

echo "🔄 Running Database Migrations"
echo "==============================="
echo ""

# Check if running in Docker
if [ -f /.dockerenv ] || [ -n "$DOCKER_CONTAINER" ]; then
    echo "Running migration in Docker container..."
    alembic upgrade head
elif command -v docker &> /dev/null && docker ps | grep -q astrofinance_api; then
    echo "Running migration in Docker container (astrofinance_api)..."
    docker exec astrofinance_api alembic upgrade head
elif [ -f "venv/bin/activate" ]; then
    echo "Running migration locally..."
    source venv/bin/activate
    alembic upgrade head
else
    echo "⚠️  No Docker container or local venv found."
    echo "Please either:"
    echo "  1. Start Docker: docker-compose up -d"
    echo "  2. Activate venv: source venv/bin/activate && alembic upgrade head"
    exit 1
fi

echo ""
echo "✅ Migration completed!"
echo ""


#!/bin/bash

echo "========================================================================"
echo "🚀 AstroStocks Startup Script"
echo "========================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting AstroStocks Application...${NC}"
echo ""

# Check if backend virtual environment exists
if [ -d "astrostocks-backend/venv" ]; then
    echo -e "${GREEN}✓ Backend virtual environment found${NC}"
else
    echo -e "${YELLOW}⚠ Backend virtual environment not found. Creating...${NC}"
    cd astrostocks-backend
    python3 -m venv venv
    cd ..
fi

# Check if frontend node_modules exists
if [ -d "astrostocks-frontend/node_modules" ]; then
    echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠ Frontend dependencies not found. Installing...${NC}"
    cd astrostocks-frontend
    npm install
    cd ..
fi

echo ""
echo "========================================================================"
echo "📋 Instructions:"
echo "========================================================================"
echo ""
echo "To start the application, open TWO terminal windows:"
echo ""
echo -e "${BLUE}Terminal 1 - Backend:${NC}"
echo "  cd astrostocks-backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo -e "${BLUE}Terminal 2 - Frontend:${NC}"
echo "  cd astrostocks-frontend"
echo "  npm run dev"
echo ""
echo "Then visit: http://localhost:3000"
echo ""
echo "========================================================================"
echo -e "${GREEN}Setup complete! Ready to launch.${NC}"
echo "========================================================================"


#!/bin/bash
# Convenience script to update API documentation and Postman collection

echo "🔄 Updating AstroFinanceAI API Documentation..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Run the update script
python3 scripts/generate_postman_collection.py

echo ""
echo "✅ All documentation updated!"
echo ""
echo "📋 Files updated:"
echo "   - API_DOCUMENTATION.md"
echo "   - AstroFinanceAI.postman_collection.json"
echo ""
echo "📦 To import into Postman:"
echo "   1. Open Postman"
echo "   2. Click 'Import'"
echo "   3. Select 'AstroFinanceAI.postman_collection.json'"
echo ""


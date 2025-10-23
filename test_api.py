"""
Simple test script to verify AstroFinanceAI API functionality
Run this after starting the API to test all endpoints
"""
import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_health():
    """Test health endpoint"""
    print_section("Testing Health Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_root():
    """Test root endpoint"""
    print_section("Testing Root Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Message: {result.get('message')}")
        print(f"Available Endpoints: {list(result.get('endpoints', {}).keys())}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_planetary_transits():
    """Test planetary transits endpoint"""
    print_section("Testing Planetary Transits Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/planetary-transits")
        print(f"Status Code: {response.status_code}")
        result = response.json()
        transits = result.get("transits", [])
        print(f"Number of transits: {len(transits)}")
        if transits:
            print("\nSample Transit:")
            print(json.dumps(transits[0], indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_stocks():
    """Test stocks endpoint"""
    print_section("Testing Stocks Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/stocks")
        print(f"Status Code: {response.status_code}")
        result = response.json()
        stocks = result.get("stocks", [])
        print(f"Number of stocks: {result.get('count', 0)}")
        if stocks:
            print("\nSample Stock:")
            print(json.dumps(stocks[0], indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_sectors():
    """Test sectors endpoint"""
    print_section("Testing Sectors Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/sectors")
        print(f"Status Code: {response.status_code}")
        result = response.json()
        sectors = result.get("sectors", [])
        print(f"Number of sectors: {result.get('count', 0)}")
        print(f"Sectors: {', '.join(sectors)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_analyze():
    """Test analyze endpoint"""
    print_section("Testing Analyze Endpoint (Main Feature)")
    try:
        response = requests.post(
            f"{BASE_URL}/analyze",
            json={},  # Empty request uses mock data
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        
        print(f"\nOverall Market Sentiment: {result.get('overall_market_sentiment')}")
        print(f"Accuracy Estimate: {result.get('accuracy_estimate')}")
        
        predictions = result.get("sector_predictions", [])
        print(f"\nNumber of Sector Predictions: {len(predictions)}")
        
        if predictions:
            print("\n📊 Sample Prediction:")
            sample = predictions[0]
            print(f"  Sector: {sample.get('sector')}")
            print(f"  Trend: {sample.get('trend')}")
            print(f"  Confidence: {sample.get('confidence')}")
            print(f"  Planetary Influence: {sample.get('planetary_influence')}")
            print(f"  Top Stocks: {', '.join(sample.get('top_stocks', []))}")
            print(f"  AI Insights: {sample.get('ai_insights')}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_sector_trends():
    """Test sector trends endpoint"""
    print_section("Testing Sector Trends Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/sector-trends?limit=5")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            trends = response.json()
            print(f"Number of trends retrieved: {len(trends)}")
            
            if trends:
                print("\nLatest Prediction:")
                latest = trends[0]
                print(f"  Sector: {latest.get('sector')}")
                print(f"  Trend: {latest.get('trend')}")
                print(f"  Created: {latest.get('created_at')}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n🪐 AstroFinanceAI API Test Suite")
    print(f"Testing API at: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Planetary Transits", test_planetary_transits),
        ("Stocks Data", test_stocks),
        ("Sectors List", test_sectors),
        ("Analyze (Main)", test_analyze),
        ("Sector Trends", test_sector_trends),
    ]
    
    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # Summary
    print_section("Test Summary")
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}  {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! API is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
        exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        exit(1)


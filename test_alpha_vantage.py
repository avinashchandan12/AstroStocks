"""
Test script for Alpha Vantage API integration
Run this to verify your API key and data fetching
"""
import os
from dotenv import load_dotenv
from app.services.alpha_vantage_service import AlphaVantageService

# Load environment variables
load_dotenv()


def test_quote():
    """Test fetching a single stock quote"""
    print("\n" + "="*60)
    print("TEST 1: Fetching Quote for RELIANCE")
    print("="*60)
    
    service = AlphaVantageService()
    quote = service.get_quote("RELIANCE")
    
    if quote:
        print("✅ Quote fetched successfully!")
        print(f"Symbol: {quote['symbol']}")
        print(f"Current Price: ₹{quote['current_price']}")
        print(f"Change: {quote['change_percent']}%")
        print(f"Volume: {quote['volume']:,.0f}")
    else:
        print("❌ Failed to fetch quote")


def test_overview():
    """Test fetching company overview"""
    print("\n" + "="*60)
    print("TEST 2: Fetching Company Overview for TCS")
    print("="*60)
    
    service = AlphaVantageService()
    overview = service.get_company_overview("TCS")
    
    if overview:
        print("✅ Overview fetched successfully!")
        print(f"Symbol: {overview['symbol']}")
        print(f"Sector: {overview['sector']}")
        print(f"P/E Ratio: {overview['pe_ratio']}")
        print(f"Market Cap: ₹{overview['market_cap']:,.0f}" if overview['market_cap'] else "N/A")
    else:
        print("❌ Failed to fetch overview")


def test_daily_adjusted():
    """Test fetching daily adjusted data"""
    print("\n" + "="*60)
    print("TEST 3: Fetching Historical Data for HDFCBANK")
    print("="*60)
    
    service = AlphaVantageService()
    historical = service.get_daily_adjusted("HDFCBANK")
    
    if historical:
        print("✅ Historical data fetched successfully!")
        print(f"Symbol: {historical['symbol']}")
        print(f"6-Month Return: {historical['past_6m_return']:.2f}%")
        print(f"Volatility: {historical['volatility']}")
        print(f"Price Trend: {historical['price_trend']}")
    else:
        print("❌ Failed to fetch historical data")


def test_multiple_stocks():
    """Test fetching multiple stocks"""
    print("\n" + "="*60)
    print("TEST 4: Fetching Multiple Stocks")
    print("="*60)
    
    service = AlphaVantageService()
    symbols = ["RELIANCE", "TCS"]
    
    print(f"Fetching {len(symbols)} stocks: {', '.join(symbols)}")
    stocks = service.fetch_multiple_stocks(symbols)
    
    if stocks:
        print(f"\n✅ Successfully fetched {len(stocks)} stocks!")
        for stock in stocks:
            print(f"\n{stock['symbol']}:")
            print(f"  Price: ₹{stock['current_price']}")
            print(f"  Sector: {stock['sector']}")
            print(f"  Change: {stock['change_percent']:+.2f}%")
    else:
        print("❌ Failed to fetch stocks")


def check_api_key():
    """Check if API key is configured"""
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    
    print("\n" + "="*60)
    print("API KEY CHECK")
    print("="*60)
    
    if not api_key or api_key == "demo" or api_key == "your_alpha_vantage_key_here":
        print("⚠️  WARNING: No valid Alpha Vantage API key configured!")
        print("   Using 'demo' key which has very limited functionality.")
        print("\n   To get a free API key:")
        print("   1. Visit https://www.alphavantage.co/support/#api-key")
        print("   2. Enter your email and get your API key")
        print("   3. Add to .env file: ALPHA_VANTAGE_API_KEY=your_key_here")
        return False
    else:
        print(f"✅ API key configured: {api_key[:8]}...{api_key[-4:]}")
        return True


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("ALPHA VANTAGE API INTEGRATION TEST")
    print("="*60)
    
    has_key = check_api_key()
    
    if not has_key:
        print("\n⚠️  Skipping tests due to missing API key")
        return
    
    try:
        # Run tests
        test_quote()
        test_overview()
        test_daily_adjusted()
        test_multiple_stocks()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED")
        print("="*60)
        print("\n✅ If all tests passed, your Alpha Vantage integration is working!")
        print("   You can now use the /market/stocks/live endpoint.")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


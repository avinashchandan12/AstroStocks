"""
Alpha Vantage API Service
Fetches real-time and historical stock data from Alpha Vantage
"""
import os
import time
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from ratelimit import limits, sleep_and_retry


class RateLimiter:
    """Simple rate limiter for API calls"""
    def __init__(self, calls: int, period: int):
        self.calls = calls
        self.period = period
        self.call_times = []
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        # Remove old calls outside the period
        self.call_times = [t for t in self.call_times if now - t < self.period]
        
        if len(self.call_times) >= self.calls:
            # Need to wait
            sleep_time = self.period - (now - self.call_times[0]) + 1
            if sleep_time > 0:
                print(f"⏳ Rate limit reached, waiting {sleep_time:.1f}s...")
                time.sleep(sleep_time)
                self.call_times = []
        
        self.call_times.append(now)


class AlphaVantageService:
    """
    Service for fetching stock data from Alpha Vantage API
    Supports NSE/BSE Indian stocks with rate limiting and error handling
    """
    
    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
        self.base_url = "https://www.alphavantage.co/query"
        self.rate_limiter = RateLimiter(calls=5, period=60)  # 5 calls per minute
        self.nse_suffix = ".BSE"  # BSE suffix for Indian stocks
        self.daily_call_count = 0
        self.daily_call_limit = 25  # Free tier limit
        
        if self.api_key == "demo":
            print("⚠️  Using Alpha Vantage demo API key. Set ALPHA_VANTAGE_API_KEY for production.")
        else:
            print("✅ Alpha Vantage API initialized")
    
    def _make_request(self, params: Dict[str, str], retries: int = 3) -> Optional[Dict]:
        """
        Make API request with rate limiting and retry logic
        
        Args:
            params: Query parameters for the API
            retries: Number of retry attempts
            
        Returns:
            JSON response or None on failure
        """
        # Check daily limit
        if self.daily_call_count >= self.daily_call_limit:
            print(f"⚠️  Daily API call limit ({self.daily_call_limit}) reached")
            return None
        
        # Wait for rate limit
        self.rate_limiter.wait_if_needed()
        
        params["apikey"] = self.api_key
        
        for attempt in range(retries):
            try:
                response = requests.get(self.base_url, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                # Check for API error messages
                if "Error Message" in data:
                    print(f"❌ Alpha Vantage error: {data['Error Message']}")
                    return None
                
                if "Note" in data:
                    print(f"⚠️  Alpha Vantage note: {data['Note']}")
                    if "call frequency" in data["Note"].lower():
                        time.sleep(60)  # Wait a minute if rate limited
                        continue
                
                self.daily_call_count += 1
                return data
                
            except requests.exceptions.RequestException as e:
                print(f"⚠️  API request failed (attempt {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                return None
        
        return None
    
    def get_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Fetch real-time quote for a stock using GLOBAL_QUOTE endpoint
        
        Args:
            symbol: Stock symbol (e.g., "RELIANCE")
            
        Returns:
            Dictionary with quote data or None on failure
        """
        # Add BSE suffix for Indian stocks
        full_symbol = f"{symbol}{self.nse_suffix}"
        
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": full_symbol
        }
        
        data = self._make_request(params)
        
        if not data or "Global Quote" not in data:
            print(f"⚠️  Failed to fetch quote for {symbol}")
            return None
        
        quote = data["Global Quote"]
        
        # Check if quote is empty
        if not quote or "05. price" not in quote:
            print(f"⚠️  No data available for {symbol}")
            return None
        
        try:
            return {
                "symbol": symbol,
                "current_price": float(quote.get("05. price", 0)),
                "open_price": float(quote.get("02. open", 0)),
                "high": float(quote.get("03. high", 0)),
                "low": float(quote.get("04. low", 0)),
                "volume": float(quote.get("06. volume", 0)),
                "change_percent": float(quote.get("10. change percent", "0%").rstrip("%")),
                "latest_trading_day": quote.get("07. latest trading day", ""),
            }
        except (ValueError, KeyError) as e:
            print(f"⚠️  Error parsing quote for {symbol}: {e}")
            return None
    
    def get_company_overview(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Fetch company fundamentals using OVERVIEW endpoint
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with company data or None
        """
        full_symbol = f"{symbol}{self.nse_suffix}"
        
        params = {
            "function": "OVERVIEW",
            "symbol": full_symbol
        }
        
        data = self._make_request(params)
        
        if not data or "Symbol" not in data:
            print(f"⚠️  Failed to fetch overview for {symbol}")
            return None
        
        try:
            return {
                "symbol": symbol,
                "sector": data.get("Sector", "Unknown"),
                "industry": data.get("Industry", "Unknown"),
                "market_cap": float(data.get("MarketCapitalization", 0)) if data.get("MarketCapitalization") else None,
                "pe_ratio": float(data.get("PERatio", 0)) if data.get("PERatio") and data.get("PERatio") != "None" else None,
                "week_52_high": float(data.get("52WeekHigh", 0)) if data.get("52WeekHigh") else None,
                "week_52_low": float(data.get("52WeekLow", 0)) if data.get("52WeekLow") else None,
            }
        except (ValueError, KeyError) as e:
            print(f"⚠️  Error parsing overview for {symbol}: {e}")
            return None
    
    def get_daily_adjusted(self, symbol: str, months: int = 6) -> Optional[Dict[str, Any]]:
        """
        Fetch daily adjusted time series to calculate historical metrics
        
        Args:
            symbol: Stock symbol
            months: Number of months of history to analyze
            
        Returns:
            Dictionary with calculated metrics or None
        """
        full_symbol = f"{symbol}{self.nse_suffix}"
        
        params = {
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": full_symbol,
            "outputsize": "compact"  # Last 100 data points
        }
        
        data = self._make_request(params)
        
        if not data or "Time Series (Daily)" not in data:
            print(f"⚠️  Failed to fetch daily data for {symbol}")
            return None
        
        time_series = data["Time Series (Daily)"]
        
        if not time_series:
            return None
        
        try:
            # Get dates and prices
            dates = sorted(time_series.keys(), reverse=True)
            
            if len(dates) < 2:
                return None
            
            # Calculate 6-month return
            current_price = float(time_series[dates[0]]["5. adjusted close"])
            
            # Find price from 6 months ago (approximately 126 trading days)
            target_days = min(126, len(dates) - 1)
            past_price = float(time_series[dates[target_days]]["5. adjusted close"])
            
            past_6m_return = ((current_price - past_price) / past_price) * 100
            
            # Calculate volatility (standard deviation of daily returns)
            daily_returns = []
            for i in range(min(30, len(dates) - 1)):  # Last 30 days
                today = float(time_series[dates[i]]["5. adjusted close"])
                yesterday = float(time_series[dates[i + 1]]["5. adjusted close"])
                daily_return = ((today - yesterday) / yesterday) * 100
                daily_returns.append(daily_return)
            
            # Standard deviation of returns
            import statistics
            volatility_value = statistics.stdev(daily_returns) if len(daily_returns) > 1 else 0
            
            # Classify volatility
            if volatility_value < 2:
                volatility = "Low"
            elif volatility_value < 4:
                volatility = "Medium"
            else:
                volatility = "High"
            
            # Determine price trend
            recent_avg = sum([float(time_series[d]["5. adjusted close"]) for d in dates[:5]]) / 5
            older_avg = sum([float(time_series[d]["5. adjusted close"]) for d in dates[20:25]]) / 5
            
            price_trend = "Upward" if recent_avg > older_avg else "Downward"
            
            return {
                "symbol": symbol,
                "past_6m_return": round(past_6m_return, 2),
                "volatility": volatility,
                "volatility_value": round(volatility_value, 2),
                "price_trend": price_trend,
            }
            
        except (ValueError, KeyError, IndexError, ZeroDivisionError) as e:
            print(f"⚠️  Error calculating metrics for {symbol}: {e}")
            return None
    
    def fetch_multiple_stocks(self, symbols: List[str]) -> List[Dict[str, Any]]:
        """
        Fetch comprehensive data for multiple stocks
        Combines quote, overview, and daily data
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            List of dictionaries with complete stock data
        """
        results = []
        
        print(f"📊 Fetching data for {len(symbols)} stocks...")
        
        for i, symbol in enumerate(symbols):
            print(f"  [{i+1}/{len(symbols)}] Fetching {symbol}...")
            
            # Start with quote data
            quote = self.get_quote(symbol)
            if not quote:
                print(f"  ⚠️  Skipping {symbol} - no quote data")
                continue
            
            # Try to get overview for sector and fundamentals
            overview = self.get_company_overview(symbol)
            
            # Try to get historical metrics
            historical = self.get_daily_adjusted(symbol)
            
            # Combine all data
            stock_data = {
                "symbol": symbol,
                "current_price": quote.get("current_price", 0),
                "open_price": quote.get("open_price", 0),
                "high": quote.get("high", 0),
                "low": quote.get("low", 0),
                "volume": quote.get("volume", 0),
                "change_percent": quote.get("change_percent", 0),
                "sector": overview.get("sector", "Unknown") if overview else "Unknown",
                "pe_ratio": overview.get("pe_ratio") if overview else None,
                "market_cap": overview.get("market_cap") if overview else None,
                "week_52_high": overview.get("week_52_high") if overview else None,
                "week_52_low": overview.get("week_52_low") if overview else None,
                "past_6m_return": historical.get("past_6m_return") if historical else None,
                "volatility": historical.get("volatility", "Medium") if historical else "Medium",
                "price_trend": historical.get("price_trend", "Unknown") if historical else "Unknown",
                "news_sentiment": "Neutral",  # Placeholder for future news API integration
            }
            
            results.append(stock_data)
            
            # Small delay between stocks to respect rate limits
            if i < len(symbols) - 1:
                time.sleep(1)
        
        print(f"✅ Successfully fetched data for {len(results)}/{len(symbols)} stocks")
        
        return results


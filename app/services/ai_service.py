"""
AI Service Layer - Integrates Astrology Engine with AI Models
Supports both DeepSeek API and mock responses
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import os
import json

from app.services.astrology_engine import AstrologyEngine
from app.services.mock_data import get_stocks_by_sector

# Try to import OpenAI client, fall back gracefully if not available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None  # Define as None for type hints
    print("⚠️  OpenAI package not installed. Using mock AI responses.")

# Initialize DeepSeek client (OpenAI-compatible) if available
deepseek_client: Optional[OpenAI] = None
USE_AI_API = os.getenv("USE_AI_API", "false").lower() == "true"

if OPENAI_AVAILABLE and USE_AI_API:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if api_key and api_key != "your_deepseek_api_key_here":
        deepseek_client = OpenAI(
            api_key=api_key,
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        )
        print("✅ DeepSeek API client initialized")
    else:
        print("⚠️  DeepSeek API key not configured. Using mock AI responses.")
else:
    if USE_AI_API:
        print("⚠️  AI API disabled or OpenAI package not installed. Using mock AI responses.")

# Knowledge Base Prompt Template
KNOWLEDGE_BASE_PROMPT = """
You are an expert Astro-Financial Analyst AI trained in both Vedic Astrology (Jyotish Shastra) and Financial Market Analysis.

Your task is to combine stock market data, planetary transits, and astrological significations to generate predictive insights about various sectors and companies.

### GOAL:
Generate sector-wise and stock-wise insights based on current planetary transits and their elemental, nakshatra, and sign-based influences.

### HOW TO PROCESS:
1. Match planet → sign → element → sector mapping
2. Evaluate transits (Jupiter, Saturn, Rahu/Ketu, Mars/Venus)
3. Combine with market sentiment
4. Validate with past data patterns

### OUTPUT FORMAT:
Structured JSON with sector predictions, trends, and recommendations.

### BEHAVIOR RULES:
- Base on Vedic Astrology
- Structured, not conversational
- Focus on symbolic correlations
- Provide confidence levels
"""


class AIService:
    """
    AI Service for generating astrology-based market predictions
    Supports both DeepSeek API and mock responses
    """
    
    def __init__(self, use_api: bool = None):
        self.astrology_engine = AstrologyEngine()
        self.knowledge_base = KNOWLEDGE_BASE_PROMPT
        self.use_api = use_api if use_api is not None else (deepseek_client is not None)
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    
    def analyze_market(
        self, 
        stocks: List[Dict[str, Any]], 
        transits: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Main analysis function combining astrology engine and AI reasoning
        """
        # Step 1: Get astrological sector influences
        sector_influences = self.astrology_engine.analyze_sector_influences(transits)
        
        # Step 2: Generate predictions for each sector
        sector_predictions = []
        
        for sector, influences in sector_influences.items():
            prediction = self.astrology_engine.get_sector_prediction(sector, influences)
            
            # Add top stocks for this sector
            top_stocks = get_stocks_by_sector(sector, stocks)
            
            # Enhance with AI reasoning (mock for MVP)
            enhanced_prediction = self._enhance_with_ai_reasoning(
                prediction, 
                influences,
                top_stocks
            )
            
            sector_predictions.append(enhanced_prediction)
        
        # Step 3: Determine overall market sentiment
        overall_sentiment = self._calculate_overall_sentiment(sector_predictions)
        
        # Step 4: Calculate accuracy estimate
        accuracy = self._calculate_accuracy_estimate(transits)
        
        return {
            "sector_predictions": sector_predictions,
            "overall_market_sentiment": overall_sentiment,
            "accuracy_estimate": accuracy,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _enhance_with_ai_reasoning(
        self, 
        prediction: Dict[str, Any],
        influences: List[Dict[str, Any]],
        top_stocks: List[str]
    ) -> Dict[str, Any]:
        """
        Enhance astrological prediction with AI-style reasoning
        In production, this would call OpenAI/Claude API
        """
        sector = prediction["sector"]
        trend = prediction["trend"]
        
        # Mock AI enhancement
        planetary_summary = self._summarize_planetary_influences(influences)
        
        # Build enhanced prediction
        enhanced = {
            "sector": sector,
            "planetary_influence": planetary_summary,
            "trend": trend,
            "reason": prediction["reason"],
            "top_stocks": top_stocks,
            "confidence": prediction["confidence"],
            "ai_insights": self._generate_ai_insights(sector, trend, influences)
        }
        
        return enhanced
    
    def _summarize_planetary_influences(self, influences: List[Dict[str, Any]]) -> str:
        """Create a summary of planetary influences"""
        if not influences:
            return "No significant planetary influences"
        
        summaries = []
        for inf in influences[:3]:  # Top 3
            planet = inf["planet"]
            sign = inf["sign"]
            strength = inf["strength"]
            summaries.append(f"{planet} in {sign} ({strength})")
        
        return ", ".join(summaries)
    
    def _generate_ai_insights(
        self, 
        sector: str, 
        trend: str,
        influences: List[Dict[str, Any]]
    ) -> str:
        """
        Generate AI insights using DeepSeek API or mock responses
        """
        # Try to use DeepSeek API if available
        if self.use_api and deepseek_client:
            try:
                return self._generate_ai_insights_from_api(sector, trend, influences)
            except Exception as e:
                print(f"⚠️  DeepSeek API call failed: {e}. Falling back to mock insights.")
                # Fall through to mock response
        
        # Mock AI insights (fallback)
        return self._generate_mock_insights(sector, trend, influences)
    
    def _generate_ai_insights_from_api(
        self,
        sector: str,
        trend: str,
        influences: List[Dict[str, Any]]
    ) -> str:
        """
        Generate insights using DeepSeek API
        """
        # Format influences for prompt
        influences_text = "\n".join([
            f"- {inf['planet']} in {inf['sign']}: {inf['strength']} ({inf['influence_type']})"
            for inf in influences[:3]
        ])
        
        # Create prompt
        prompt = f"""Based on the following astrological analysis, provide a concise insight (2-3 sentences) about the {sector} sector:

Trend: {trend}
Planetary Influences:
{influences_text}

Provide practical insights combining the astrological symbolism with market outlook. Be specific and actionable."""

        # Call DeepSeek API
        response = deepseek_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.knowledge_base},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_mock_insights(
        self,
        sector: str,
        trend: str,
        influences: List[Dict[str, Any]]
    ) -> str:
        """
        Generate mock AI insights (used when API is not available)
        """
        insights = []
        
        # Trend-based insight
        if trend == "Bullish":
            insights.append(f"Strong positive momentum expected in {sector} sector")
        elif trend == "Bearish":
            insights.append(f"Caution advised for {sector} sector investments")
        else:
            insights.append(f"Mixed signals for {sector} sector, wait-and-watch approach")
        
        # Planet-based insights
        for inf in influences[:2]:
            planet = inf["planet"]
            influence_type = inf["influence_type"]
            
            if "Positive" in influence_type:
                insights.append(f"{planet}'s favorable position supports growth")
            elif "Challenging" in influence_type:
                insights.append(f"{planet}'s placement suggests caution")
        
        return ". ".join(insights) + "."
    
    def _calculate_overall_sentiment(self, predictions: List[Dict[str, Any]]) -> str:
        """Calculate overall market sentiment from sector predictions"""
        if not predictions:
            return "Neutral"
        
        bullish_count = sum(1 for p in predictions if p.get("trend") == "Bullish")
        bearish_count = sum(1 for p in predictions if p.get("trend") == "Bearish")
        
        total = len(predictions)
        bullish_pct = (bullish_count / total) * 100
        
        if bullish_pct >= 60:
            return "Positive"
        elif bullish_pct <= 40:
            return "Negative"
        else:
            return "Neutral"
    
    def _calculate_accuracy_estimate(self, transits: List[Dict[str, Any]]) -> str:
        """
        Calculate accuracy estimate based on transit strength
        More exalted planets = higher confidence
        """
        if not transits:
            return "50%"
        
        exalted_count = sum(1 for t in transits if t.get("status") == "Exalted")
        total = len(transits)
        
        # Base accuracy + bonus for exalted planets
        base_accuracy = 65
        bonus = (exalted_count / total) * 20
        
        final_accuracy = min(base_accuracy + bonus, 85)
        return f"{int(final_accuracy)}%"
    
    def analyze_market_with_stocks(
        self,
        stock_data: List[Dict[str, Any]],
        transits: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Enhanced analysis that combines real stock data with astrological predictions
        
        Steps:
        1. Generate sector predictions from AI based on transits
        2. Match real stocks to sectors
        3. Rank stocks within each sector
        4. Generate buy/hold/sell signals
        5. Return top recommendations + full sector analysis
        
        Args:
            stock_data: List of real stock data from market
            transits: List of planetary transits
            
        Returns:
            Dictionary with top recommendations, sector analysis, and all stocks
        """
        # Step 1: Generate sector predictions with AI
        sector_influences = self.astrology_engine.analyze_sector_influences(transits)
        sector_predictions = self._get_ai_sector_predictions(sector_influences, transits)
        
        # Step 2: Match stocks to sectors and group them
        sector_stocks_map = self._group_stocks_by_sector(stock_data)
        
        # Step 3: Generate signals for all stocks
        all_stock_signals = self._generate_stock_signals(
            stock_data, 
            sector_predictions
        )
        
        # Step 4: Create sector analysis with stocks
        sector_analysis = self._create_sector_analysis(
            sector_predictions,
            sector_stocks_map,
            all_stock_signals
        )
        
        # Step 5: Get top 10 recommendations
        top_recommendations = self._get_top_recommendations(all_stock_signals, limit=10)
        
        # Step 6: Calculate overall sentiment
        overall_sentiment = self._calculate_overall_sentiment(sector_predictions)
        
        return {
            "top_recommendations": top_recommendations,
            "sector_analysis": sector_analysis,
            "all_stocks": all_stock_signals,
            "overall_sentiment": overall_sentiment,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _get_ai_sector_predictions(
        self, 
        sector_influences: Dict[str, List[Dict[str, Any]]], 
        transits: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Use DeepSeek API to generate structured sector predictions
        
        Args:
            sector_influences: Planetary influences by sector
            transits: Full transit data
            
        Returns:
            List of sector predictions with trends and insights
        """
        predictions = []
        
        # Confidence mapping from string to numeric
        confidence_map = {
            "High": 0.85,
            "Medium": 0.65,
            "Low": 0.45
        }
        
        for sector, influences in sector_influences.items():
            # Get base prediction from astrology engine
            base_prediction = self.astrology_engine.get_sector_prediction(sector, influences)
            
            # Enhance with AI insights
            ai_insights = self._generate_ai_insights(sector, base_prediction["trend"], influences)
            
            # Convert string confidence to numeric
            confidence_str = base_prediction["confidence"]
            confidence_numeric = confidence_map.get(confidence_str, 0.5)
            
            prediction = {
                "sector": sector,
                "trend": base_prediction["trend"],
                "planetary_influence": self._summarize_planetary_influences(influences),
                "ai_insights": ai_insights,
                "confidence": confidence_numeric,
                "reason": base_prediction["reason"]
            }
            
            predictions.append(prediction)
        
        return predictions
    
    def _group_stocks_by_sector(
        self, 
        stock_data: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Group stocks by their sector"""
        sector_map = {}
        
        for stock in stock_data:
            sector = stock.get("sector", "Unknown")
            if sector not in sector_map:
                sector_map[sector] = []
            sector_map[sector].append(stock)
        
        return sector_map
    
    def _generate_stock_signals(
        self,
        stock_data: List[Dict[str, Any]],
        sector_predictions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate BUY/HOLD/SELL signals for each stock
        
        Signal Logic:
        - BUY: Bullish sector + positive performance + good technicals
        - SELL: Bearish sector + negative performance
        - HOLD: Everything else
        
        Args:
            stock_data: List of stock data
            sector_predictions: Sector-level predictions
            
        Returns:
            List of stocks with signals and reasoning
        """
        # Create sector trend lookup
        sector_trends = {
            pred["sector"]: pred for pred in sector_predictions
        }
        
        signals = []
        
        for stock in stock_data:
            sector = stock.get("sector", "Unknown")
            sector_pred = sector_trends.get(sector, {
                "trend": "Neutral",
                "confidence": 0.5,
                "ai_insights": "No astrological insights available",
                "planetary_influence": "Unknown"
            })
            
            # Calculate signal
            signal_result = self._calculate_signal(stock, sector_pred)
            
            signals.append(signal_result)
        
        # Sort by score (highest first)
        signals.sort(key=lambda x: x["score"], reverse=True)
        
        return signals
    
    def _calculate_signal(
        self,
        stock: Dict[str, Any],
        sector_pred: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate signal and score for a single stock"""
        
        sector_trend = sector_pred.get("trend", "Neutral")
        confidence = sector_pred.get("confidence", 0.5)
        
        # Get stock metrics
        change_percent = stock.get("change_percent", 0) or 0
        past_6m_return = stock.get("past_6m_return", 0) or 0
        volatility = stock.get("volatility", "Medium")
        
        # Initialize score
        score = 50.0  # Base score
        
        # Sector trend contribution (40 points)
        if sector_trend == "Bullish":
            score += 40 * confidence
        elif sector_trend == "Bearish":
            score -= 40 * confidence
        
        # Stock performance contribution (30 points)
        if past_6m_return > 20:
            score += 30
        elif past_6m_return > 10:
            score += 20
        elif past_6m_return > 0:
            score += 10
        elif past_6m_return < -20:
            score -= 30
        elif past_6m_return < -10:
            score -= 20
        else:
            score -= 10
        
        # Current momentum (20 points)
        if change_percent > 2:
            score += 20
        elif change_percent > 0:
            score += 10
        elif change_percent < -2:
            score -= 20
        elif change_percent < 0:
            score -= 10
        
        # Volatility adjustment (10 points)
        if volatility == "Low":
            score += 10
        elif volatility == "High":
            score -= 10
        
        # Determine signal based on score
        if score >= 70:
            signal = "BUY"
        elif score <= 40:
            signal = "SELL"
        else:
            signal = "HOLD"
        
        # Generate reasoning
        astrological_reasoning = f"{sector_pred.get('ai_insights', 'Sector analysis based on planetary transits.')}"
        
        technical_summary = f"6M Return: {past_6m_return:.1f}%, Today: {change_percent:+.1f}%, Volatility: {volatility}"
        
        return {
            "symbol": stock.get("symbol"),
            "sector": stock.get("sector", "Unknown"),
            "current_price": stock.get("current_price"),
            "change_percent": change_percent,
            "signal": signal,
            "confidence": confidence,
            "astrological_reasoning": astrological_reasoning,
            "technical_summary": technical_summary,
            "past_6m_return": past_6m_return,
            "volatility": volatility,
            "score": score
        }
    
    def _create_sector_analysis(
        self,
        sector_predictions: List[Dict[str, Any]],
        sector_stocks_map: Dict[str, List[Dict[str, Any]]],
        all_stock_signals: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create comprehensive sector analysis with stocks"""
        
        analysis = []
        
        for sector_pred in sector_predictions:
            sector = sector_pred["sector"]
            
            # Get stocks in this sector
            stocks_in_sector = [
                s for s in all_stock_signals 
                if s["sector"] == sector
            ]
            
            sector_analysis = {
                "sector": sector,
                "trend": sector_pred["trend"],
                "planetary_influence": sector_pred["planetary_influence"],
                "ai_insights": sector_pred["ai_insights"],
                "stocks_in_sector": stocks_in_sector,
                "confidence": sector_pred["confidence"]
            }
            
            analysis.append(sector_analysis)
        
        return analysis
    
    def _get_top_recommendations(
        self,
        all_signals: List[Dict[str, Any]],
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get top N stock recommendations sorted by score"""
        
        # Filter for BUY signals primarily, but include top HOLD signals too
        buy_signals = [s for s in all_signals if s["signal"] == "BUY"]
        hold_signals = [s for s in all_signals if s["signal"] == "HOLD"]
        
        # Prioritize BUY signals
        top_stocks = buy_signals[:limit]
        
        # Fill remaining slots with top HOLD signals
        remaining = limit - len(top_stocks)
        if remaining > 0:
            top_stocks.extend(hold_signals[:remaining])
        
        # Create recommendations with rankings
        recommendations = []
        for rank, stock in enumerate(top_stocks, 1):
            recommendation = {
                "rank": rank,
                "stock": {
                    "symbol": stock["symbol"],
                    "sector": stock["sector"],
                    "current_price": stock["current_price"],
                    "change_percent": stock["change_percent"],
                    "signal": stock["signal"],
                    "confidence": stock["confidence"],
                    "astrological_reasoning": stock["astrological_reasoning"],
                    "technical_summary": stock["technical_summary"],
                    "past_6m_return": stock["past_6m_return"],
                    "volatility": stock["volatility"]
                },
                "score": stock["score"]
            }
            recommendations.append(recommendation)
        
        return recommendations


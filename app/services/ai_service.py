"""
AI Service Layer - Integrates Astrology Engine with AI Models
Supports DeepSeek API for market predictions
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import os
import json

from app.services.astrology_engine import AstrologyEngine

# Try to import OpenAI client
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None  # Define as None for type hints
    print("⚠️  OpenAI package not installed. API features will be unavailable.")

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
        print("⚠️  DeepSeek API key not configured. API features will be unavailable.")
else:
    if USE_AI_API:
        print("⚠️  AI API disabled or OpenAI package not installed. API features will be unavailable.")

# Knowledge Base Prompt Template
KNOWLEDGE_BASE_PROMPT = """
You are an **Expert Astro-Financial Analyst AI** trained in **Vedic Astrology (Jyotish Shastra)**, **Planetary Transits (Gochar)**, **Sectoral Market Analysis**, and **Historical Stock Data Interpretation**.

Your task is to analyze **planetary transits**, **sign elements**, **nakshatras**, and **sectoral karakatwas** to generate **predictive insights** about **market sectors and specific companies**.

---

### GOAL:
Produce sector-wise and stock-wise predictions using astrological logic correlated with financial data.  
Focus on how planetary energies, elements, and aspects symbolically influence economic activities and investor sentiment.

---

### HOW TO PROCESS:

#### 1. **Planet → Sign → Element → Sector Mapping**
- Identify each planet’s **current sign** and **element (Fire, Earth, Air, Water)**.
- Determine the **industries** governed by that element and planet’s **karakatwa**.
- Assign influence scores based on:
  - Planet’s dignity (Exalted, Own, Friendly, Neutral, Enemy, Debilitated)
  - Sign lordship and mutual aspects
  - Nakshatra and its ruler’s strength

#### 2. **Evaluate Key Transits**
- **Jupiter (Guru)** → Expansion, macro growth, liquidity
- **Saturn (Shani)** → Structure, industry, consolidation
- **Rahu–Ketu** → Innovation, hype, volatility, or reversal
- **Mars, Mercury, Venus, Sun, Moon** → Short-term trends, emotional sentiment, and momentum
- Measure each planet’s:
  - Transit house position (relative to national chart or base chart)
  - Elemental influence
  - Drishti (aspect-based energy flow)

#### 3. **Combine with Market Sentiment**
- Align planetary positivity/negativity with current **market mood indicators**.
- If benefic planets transit friendly elements → bullish bias.
- If malefics dominate → caution, correction, or sideways consolidation.

#### 4. **Validate with Historical Patterns**
- Compare with **previous similar transits** (e.g., Jupiter in Cancer 2014–2015) to estimate impact duration and magnitude.
- Use backtesting logic for historical sector performance under similar transit configurations.

---

### PLANETARY KARAKATWA REFERENCE:

| Planet | Market Role | Industries / Sectors |
|---------|--------------|----------------------|
| Sun | Power, governance | Oil, Energy, PSU, Defense |
| Moon | Liquidity, sentiment | FMCG, Pharma, Dairy |
| Mars | Action, production | Steel, Automobiles, Infrastructure |
| Mercury | Trade, communication | Banking, IT, Media, Telecom |
| Venus | Luxury, comfort | Real Estate, Fashion, Entertainment |
| Jupiter | Expansion, finance | Chemicals, Education, Pharma |
| Saturn | Industry, discipline | Steel, Infrastructure, Mining |
| Rahu | Innovation, illusion | Technology, AI, Crypto, Foreign Capital |
| Ketu | Detachment, analysis | Research, Biotech, Diagnostics |

---

### ELEMENTAL-BASED INDUSTRY MATRIX:

| Element | Signs | Economic Nature | Favored Industries |
|----------|--------|------------------|--------------------|
| Fire (Agni) | Aries, Leo, Sagittarius | Energy, drive, metals | Power, Oil, Defense, Steel |
| Earth (Prithvi) | Taurus, Virgo, Capricorn | Stability, resources | Real Estate, Banking, Cement |
| Air (Vayu) | Gemini, Libra, Aquarius | Communication, movement | IT, Telecom, Aviation |
| Water (Jal) | Cancer, Scorpio, Pisces | Liquidity, emotion | Chemicals, Pharma, FMCG |

---

### WEIGHTAGE SYSTEM:

| Planet | Influence % | Description |
|---------|--------------|-------------|
| Jupiter | 25% | Long-term expansion, sector growth |
| Saturn | 25% | Industry trends, infrastructure, consolidation |
| Rahu–Ketu | 15% | Innovation, disruption, foreign capital |
| Mars | 10% | Short-term sectoral volatility, industrial energy |
| Mercury | 10% | Speculation, trading sentiment |
| Venus | 8% | Consumer spending, luxury |
| Moon & Sun | 7% | Emotional sentiment, PSU behavior |

---

###OUTPUT STRUCTURE (JSON FORMAT):

{
  "date": "YYYY-MM-DD",
  "planetary_positions": {
    "Jupiter": {"sign": "Cancer", "element": "Water", "nakshatra": "Pushya"},
    "Saturn": {"sign": "Aries", "element": "Fire", "nakshatra": "Bharani"},
    ...
  },
  "sector_predictions": [
    {
      "sector": "Chemicals",
      "primary_planet": "Jupiter",
      "trend": "Bullish",
      "reason": "Jupiter exalted in Cancer (Water sign) expands chemical and pharma sector",
      "confidence": 0.82
    },
    {
      "sector": "Steel",
      "primary_planet": "Saturn",
      "trend": "Gradual uptrend post-consolidation",
      "reason": "Saturn transiting Aries (Fire sign of Mars) supports heavy industry revival",
      "confidence": 0.76
    }
  ],
  "market_sentiment": "Positive liquidity inflow; short-term volatility due to Rahu in Pisces",
  "summary": "Expansionary phase for chemicals, FMCG, and infra sectors. Volatility expected in IT and fintech."
}

---

### BEHAVIOR RULES:
- Strictly adhere to **Vedic Astrology** principles (Parashara, Varahamihira, and Jaimini foundations).
- Use **symbolic, not causal** correlations.
- Keep tone analytical, **non-conversational**.
- Focus on planetary influence, **not personal or individual charts**.
- Always include **confidence levels (0–1)** based on planetary dignity and aspect support.
- Structure the output for machine readability and data integration.

"""



class AIService:
    """
    AI Service for generating astrology-based market predictions
    Uses DeepSeek API for market predictions
    """
    
    def __init__(self, use_api: bool = None):
        self.astrology_engine = AstrologyEngine()
        self.knowledge_base = KNOWLEDGE_BASE_PROMPT
        self.use_api = use_api if use_api is not None else (deepseek_client is not None)
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    
    def _get_top_stocks_by_sector(self, sector: str, stocks: List[Dict[str, Any]]) -> List[str]:
        """Get top stock symbols for a given sector"""
        sector_stocks = [s for s in stocks if s.get("sector") == sector]
        # Sort by 6-month returns
        sector_stocks.sort(key=lambda x: x.get("past_6m_return", 0), reverse=True)
        return [s["symbol"] for s in sector_stocks[:3]]
    
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
            top_stocks = self._get_top_stocks_by_sector(sector, stocks)
            
            # Enhance with AI reasoning
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
        
        # AI enhancement
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
        Generate AI insights using DeepSeek API
        """
        # Use DeepSeek API
        if self.use_api and deepseek_client:
            try:
                return self._generate_ai_insights_from_api(sector, trend, influences)
            except Exception as e:
                print(f"⚠️  DeepSeek API call failed: {e}")
                raise e
        
        # If API is not available, raise error
        raise Exception("DeepSeek API not available")
    
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
        prompt = f"""Based on the following astrological analysis, provide a concise insight about the {sector} sector:

Trend: {trend}
Planetary Influences:
{influences_text}

Provide practical insights combining the astrological symbolism with market outlook. Be specific and actionable.

Return your response as a JSON object with the following structure:
{{
  "sector": "{sector}",
  "trend": "{trend}",
  "reason": "Brief explanation of the astrological reasoning",
  "confidence": 0.75,
  "actionable_insight": "Specific investment recommendation or insight"
}}"""

        # Check if debug logging is enabled
        debug_logging = os.getenv("DEBUG_DEEPSEEK_REQUESTS", "true").lower() == "true"
        
        if debug_logging:
            # Log the request
            print("=" * 60)
            print(f"🌟 DEEPSEEK SECTOR INSIGHTS REQUEST FOR {sector.upper()}:")
            print("=" * 60)
            print(f"Prompt: {prompt}")
            print("=" * 60)

        try:
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
            
            if debug_logging:
                # Log the response
                print("=" * 60)
                print(f"📥 DEEPSEEK SECTOR RESPONSE FOR {sector.upper()}:")
                print("=" * 60)
                print(f"Response: {response.choices[0].message.content}")
                print("=" * 60)
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse JSON response
            try:
                import json
                parsed_content = json.loads(content)
                return parsed_content
            except json.JSONDecodeError:
                # If not valid JSON, return as string
                return content
            
        except Exception as e:
            if debug_logging:
                print("=" * 60)
                print(f"❌ DEEPSEEK SECTOR API ERROR FOR {sector.upper()}:")
                print("=" * 60)
                print(f"Error: {e}")
                print("=" * 60)
            raise e
    
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
    
    def generate_market_prediction_from_transits(
        self,
        transits: List[Dict[str, Any]],
        prediction_date: datetime,
        include_past_data: bool = False
    ) -> Dict[str, Any]:
        """
        Generate market prediction from planetary transits
        
        Args:
            transits: List of planetary transit data
            prediction_date: Date for prediction
            include_past_data: Whether to include historical market data
            
        Returns:
            Dictionary with market prediction results
        """
        try:
            # Get sector influences from astrology engine
            sector_influences = self.astrology_engine.analyze_sector_influences(transits)
            
            # Generate sector predictions (limit to top 5 sectors to avoid timeout)
            sector_predictions = []
            sector_items = list(sector_influences.items())
            
            # Sort sectors by number of influences (most influenced first)
            sector_items.sort(key=lambda x: len(x[1]), reverse=True)
            
            # Limit to top 5 sectors
            for sector, influences in sector_items[:5]:
                prediction = self.astrology_engine.get_sector_prediction(sector, influences)
                
                # Enhance with AI insights
                ai_insights = self._generate_ai_insights(sector, prediction["trend"], influences)
                
                sector_prediction = {
                    "sector": sector,
                    "trend": prediction["trend"],
                    "planetary_influence": self._summarize_planetary_influences(influences),
                    "ai_insights": ai_insights,
                    "confidence": prediction["confidence"],
                    "reason": prediction["reason"]
                }
                sector_predictions.append(sector_prediction)
            
            # Generate overall AI analysis
            ai_analysis = self._generate_overall_analysis(transits, sector_predictions, prediction_date)
            
            # Calculate overall sentiment
            overall_sentiment = self._calculate_overall_sentiment(sector_predictions)
            
            return {
                "overall_sentiment": overall_sentiment,
                "sector_predictions": sector_predictions,
                "ai_analysis": ai_analysis,
                "prediction_date": prediction_date.isoformat()
            }
            
        except Exception as e:
            print(f"Error generating market prediction: {e}")
            raise Exception(f"Market prediction failed: {str(e)}")
    
    def _generate_overall_analysis(
        self,
        transits: List[Dict[str, Any]],
        sector_predictions: List[Dict[str, Any]],
        prediction_date: datetime
    ) -> str:
        """Generate comprehensive AI analysis of market outlook"""
        
        # Use DeepSeek API
        if self.use_api and deepseek_client:
            try:
                return self._generate_overall_analysis_from_api(transits, sector_predictions, prediction_date)
            except Exception as e:
                print(f"⚠️  DeepSeek API call failed: {e}")
                raise e
        
        # If API is not available, raise error
        raise Exception("DeepSeek API not available")
    
    def _generate_overall_analysis_from_api(
        self,
        transits: List[Dict[str, Any]],
        sector_predictions: List[Dict[str, Any]],
        prediction_date: datetime
    ) -> str:
        """Generate overall analysis using DeepSeek API"""
        
        # Format transit summary
        transit_summary = "\n".join([
            f"- {t['planet']} in {t['sign']}: {t['dignity']} ({t['motion']})"
            for t in transits[:5]
        ])
        
        # Format sector trends
        sector_trends = "\n".join([
            f"- {sp['sector']}: {sp['trend']} ({sp['confidence']})"
            for sp in sector_predictions[:3]
        ])
        
        # Create comprehensive prompt
        prompt = f"""Based on the planetary transits for {prediction_date.strftime('%Y-%m-%d')}, provide a comprehensive market outlook analysis:

PLANETARY TRANSITS:
{transit_summary}

SECTOR TRENDS:
{sector_trends}

Provide a detailed analysis covering:
1. Overall market sentiment and key astrological influences
2. Sector-specific insights and opportunities
3. Risk factors and cautionary notes
4. Investment recommendations based on planetary positions

Be specific, actionable, and combine astrological wisdom with practical market insights.

Return your response as a JSON object with the following structure:
{{
  "date": "{prediction_date.strftime('%Y-%m-%d')}",
  "market_sentiment": "Overall market sentiment (Bullish/Bearish/Neutral)",
  "key_influences": [
    {{
      "planet": "Planet name",
      "sign": "Sign name",
      "influence": "Description of influence"
    }}
  ],
  "sector_highlights": [
    {{
      "sector": "Sector name",
      "trend": "Trend direction",
      "confidence": 0.75,
      "reason": "Brief explanation"
    }}
  ],
  "investment_recommendations": "Specific actionable recommendations",
  "risk_factors": "Key risks to watch",
  "summary": "Overall market outlook summary"
}}"""

        # Check if debug logging is enabled
        debug_logging = os.getenv("DEBUG_DEEPSEEK_REQUESTS", "true").lower() == "true"
        
        if debug_logging:
            # Log the request being sent to DeepSeek
            print("=" * 80)
            print("🚀 DEEPSEEK OVERALL ANALYSIS REQUEST:")
            print("=" * 80)
            print(f"Model: {self.model}")
            print(f"Temperature: 0.7")
            print(f"Max Tokens: 500")
            print("\n📝 PROMPT:")
            print(prompt)
            print("=" * 80)

        try:
            # Call DeepSeek API
            response = deepseek_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.knowledge_base},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            if debug_logging:
                # Log the response from DeepSeek
                print("=" * 80)
                print("📥 DEEPSEEK OVERALL ANALYSIS RESPONSE:")
                print("=" * 80)
                print(f"Response Object: {response}")
                print(f"Response Content: {response.choices[0].message.content}")
                print("=" * 80)
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse JSON response
            try:
                import json
                parsed_content = json.loads(content)
                return parsed_content
            except json.JSONDecodeError:
                # If not valid JSON, return as string
                return content
            
        except Exception as e:
            if debug_logging:
                print("=" * 80)
                print("❌ DEEPSEEK OVERALL ANALYSIS API ERROR:")
                print("=" * 80)
                print(f"Error: {e}")
                print("=" * 80)
            raise e


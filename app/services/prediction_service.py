"""
Prediction Service - Core logic for market predictions based on planetary transits
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, date
import os
import pytz

from app.services.ephemeris_service import ephemeris_service
from app.services.ai_service import AIService
from app.services.astrology_engine import AstrologyEngine
from app.services.alpha_vantage_service import AlphaVantageService
from app.schemas.schemas import (
    PredictRequest, PredictResponse, LocationInfo, 
    PlanetaryTransit, MarketPrediction, KeyInfluence
)


class PredictionService:
    """Service for generating market predictions based on planetary transits"""
    
    def __init__(self):
        self.ai_service = AIService()
        self.astrology_engine = AstrologyEngine()
        self.alpha_vantage_service = AlphaVantageService()
        
        # Default values from environment
        self.default_lat = float(os.getenv("DEFAULT_LOCATION_LAT", "28.6139"))
        self.default_lon = float(os.getenv("DEFAULT_LOCATION_LON", "77.2090"))
        self.default_timezone = os.getenv("DEFAULT_TIMEZONE", "Asia/Kolkata")
    
    def generate_prediction(
        self,
        request: PredictRequest,
        include_past_data: bool = False
    ) -> PredictResponse:
        """
        Generate market prediction based on planetary transits
        
        Args:
            request: Prediction request with date/time/location parameters
            include_past_data: Whether to include historical market data
            
        Returns:
            PredictResponse with prediction results
        """
        try:
            # Parse and validate inputs with defaults
            prediction_datetime, location = self._parse_inputs(request)
            
            # Calculate planetary transits for the given date/time
            planetary_positions = ephemeris_service.get_all_planetary_positions(prediction_datetime)
            
            # Format planetary transits
            planetary_transits = self._format_planetary_transits(planetary_positions)
            
            # Generate AI-powered market prediction
            market_prediction = self._generate_market_prediction(
                planetary_transits, 
                prediction_datetime,
                include_past_data
            )
            
            # Calculate overall confidence
            confidence = self._calculate_confidence(planetary_transits)
            
            # Get past market data if requested
            past_market_data = None
            if include_past_data:
                past_market_data = self._get_past_market_data(prediction_datetime)
            
            # Format response
            response = PredictResponse(
                prediction_date=prediction_datetime.isoformat(),
                location=LocationInfo(
                    latitude=location["latitude"],
                    longitude=location["longitude"],
                    timezone=location["timezone"]
                ),
                planetary_transits=planetary_transits,
                market_prediction=market_prediction,
                past_market_data=past_market_data,
                confidence=confidence
            )
            
            return response
            
        except Exception as e:
            raise Exception(f"Prediction generation failed: {str(e)}")
    
    def _parse_inputs(self, request: PredictRequest) -> tuple[datetime, Dict[str, Any]]:
        """Parse and validate input parameters with defaults"""
        
        # Get date (default to today)
        if request.date:
            prediction_date = datetime.fromisoformat(request.date).date()
        else:
            prediction_date = date.today()
        
        # Get time (default to current time)
        if request.time:
            time_parts = request.time.split(":")
            hour = int(time_parts[0])
            minute = int(time_parts[1]) if len(time_parts) > 1 else 0
            second = int(time_parts[2]) if len(time_parts) > 2 else 0
        else:
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            second = now.second
        
        # Create datetime object
        prediction_datetime = datetime.combine(prediction_date, datetime.min.time().replace(hour=hour, minute=minute, second=second))
        
        # Get timezone
        timezone_str = request.timezone or self.default_timezone
        timezone = pytz.timezone(timezone_str)
        
        # Localize datetime to timezone
        localized_datetime = timezone.localize(prediction_datetime)
        
        # Convert to UTC for ephemeris calculations
        utc_datetime = localized_datetime.astimezone(pytz.UTC)
        
        # Get location
        location = {
            "latitude": request.latitude or self.default_lat,
            "longitude": request.longitude or self.default_lon,
            "timezone": timezone_str
        }
        
        return utc_datetime, location
    
    def _format_planetary_transits(self, planetary_positions: List[Dict[str, Any]]) -> List[PlanetaryTransit]:
        """Format planetary positions into transit objects"""
        transits = []
        
        for position in planetary_positions:
            transit = PlanetaryTransit(
                planet=position["planet"],
                longitude=position["longitude"],
                latitude=position["latitude"],
                sign=position["sign"],
                degree_in_sign=position["degree_in_sign"],
                dignity=position["dignity"],
                retrograde=position["retrograde"],
                motion=position["motion"],
                speed=position["speed"]
            )
            transits.append(transit)
        
        return transits
    
    def _generate_market_prediction(
        self, 
        planetary_transits: List[PlanetaryTransit],
        prediction_datetime: datetime,
        include_past_data: bool
    ) -> MarketPrediction:
        """Generate AI-powered market prediction"""
        
        # Convert transits to format expected by astrology engine
        transits_data = []
        for transit in planetary_transits:
            transits_data.append({
                "planet": transit.planet,
                "sign": transit.sign,
                "longitude": transit.longitude,
                "dignity": transit.dignity,
                "retrograde": transit.retrograde,
                "motion": transit.motion
            })
        
        # Get sector influences from astrology engine
        sector_influences = self.astrology_engine.analyze_sector_influences(transits_data)
        
        # Generate AI prediction
        prediction_result = self.ai_service.generate_market_prediction_from_transits(
            transits_data, 
            prediction_datetime,
            include_past_data
        )
        
        # Extract key influences
        key_influences = []
        for sector, influences in sector_influences.items():
            for influence in influences[:2]:  # Top 2 influences per sector
                key_influence = KeyInfluence(
                    planet=influence["planet"],
                    sign=influence["sign"],
                    influence_type=influence["influence_type"],
                    strength=influence["strength"],
                    description=f"{influence['planet']} in {influence['sign']} affects {sector} sector"
                )
                key_influences.append(key_influence)
        
        # Limit to top 5 influences
        key_influences = key_influences[:5]
        
        return MarketPrediction(
            overall_sentiment=prediction_result["overall_sentiment"],
            sector_predictions=prediction_result["sector_predictions"],
            key_influences=key_influences,
            ai_analysis=prediction_result["ai_analysis"]
        )
    
    def _calculate_confidence(self, planetary_transits: List[PlanetaryTransit]) -> float:
        """Calculate prediction confidence based on planetary strength"""
        if not planetary_transits:
            return 0.5
        
        # Base confidence
        confidence = 0.6
        
        # Bonus for exalted planets
        exalted_count = sum(1 for t in planetary_transits if t.dignity == "Exalted")
        exalted_bonus = (exalted_count / len(planetary_transits)) * 0.2
        
        # Bonus for direct motion planets
        direct_count = sum(1 for t in planetary_transits if not t.retrograde)
        direct_bonus = (direct_count / len(planetary_transits)) * 0.1
        
        # Bonus for multiple planets in same signs (conjunctions)
        sign_counts = {}
        for transit in planetary_transits:
            sign_counts[transit.sign] = sign_counts.get(transit.sign, 0) + 1
        
        conjunction_bonus = 0
        for count in sign_counts.values():
            if count >= 2:
                conjunction_bonus += 0.05 * (count - 1)
        
        final_confidence = min(confidence + exalted_bonus + direct_bonus + conjunction_bonus, 0.95)
        return round(final_confidence, 2)
    
    def _get_past_market_data(self, prediction_datetime: datetime) -> Optional[List[Dict[str, Any]]]:
        """Get historical market data if requested"""
        try:
            # Get tracked stocks from config
            from app.config.stock_config import get_tracked_stocks
            tracked_symbols = get_tracked_stocks()
            
            if not tracked_symbols:
                return None
            
            # Get historical data (last 30 days)
            historical_data = []
            for symbol in tracked_symbols[:5]:  # Limit to 5 stocks to avoid rate limits
                try:
                    data = self.alpha_vantage_service.get_historical_data(symbol, days=30)
                    if data:
                        historical_data.append({
                            "symbol": symbol,
                            "data": data
                        })
                except Exception as e:
                    print(f"Error fetching data for {symbol}: {e}")
                    continue
            
            return historical_data
            
        except Exception as e:
            print(f"Error fetching historical market data: {e}")
            return None

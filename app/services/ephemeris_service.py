"""
Ephemeris Service - Real Astrological Calculations using Swiss Ephemeris
Provides accurate planetary positions, nakshatras, and Vedic astrology data
"""
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, date
import os

# Try to import swisseph, fall back gracefully if not available
try:
    import swisseph as swe
    SWISSEPH_AVAILABLE = True
except ImportError:
    SWISSEPH_AVAILABLE = False
    print("⚠️  pyswisseph not installed. Using mock ephemeris data.")


# Planet constants from Swiss Ephemeris
PLANETS = {
    'Sun': swe.SUN if SWISSEPH_AVAILABLE else 0,
    'Moon': swe.MOON if SWISSEPH_AVAILABLE else 1,
    'Mars': swe.MARS if SWISSEPH_AVAILABLE else 4,
    'Mercury': swe.MERCURY if SWISSEPH_AVAILABLE else 2,
    'Jupiter': swe.JUPITER if SWISSEPH_AVAILABLE else 5,
    'Venus': swe.VENUS if SWISSEPH_AVAILABLE else 3,
    'Saturn': swe.SATURN if SWISSEPH_AVAILABLE else 6,
    'Rahu': swe.TRUE_NODE if SWISSEPH_AVAILABLE else 10,  # True Node
    'Ketu': -1,  # Calculated as opposite of Rahu
}

# Zodiac signs
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Nakshatras (27 lunar mansions)
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# Exaltation and Debilitation
EXALTATION_SIGNS = {
    "Sun": "Aries",
    "Moon": "Taurus",
    "Mars": "Capricorn",
    "Mercury": "Virgo",
    "Jupiter": "Cancer",
    "Venus": "Pisces",
    "Saturn": "Libra",
    "Rahu": "Taurus",
    "Ketu": "Scorpio"
}

DEBILITATION_SIGNS = {
    "Sun": "Libra",
    "Moon": "Scorpio",
    "Mars": "Cancer",
    "Mercury": "Pisces",
    "Jupiter": "Capricorn",
    "Venus": "Virgo",
    "Saturn": "Aries",
    "Rahu": "Scorpio",
    "Ketu": "Taurus"
}


class EphemerisService:
    """Service for calculating real planetary positions using Swiss Ephemeris"""
    
    def __init__(self):
        self.use_real_ephemeris = SWISSEPH_AVAILABLE and os.getenv("USE_REAL_EPHEMERIS", "true").lower() == "true"
        if self.use_real_ephemeris:
            # Set ephemeris path if provided
            ephe_path = os.getenv("EPHEMERIS_PATH", "")
            if ephe_path:
                swe.set_ephe_path(ephe_path)
            
            # Configure Ayanamsa for Vedic (Sidereal) astrology
            ayanamsa_type = os.getenv("AYANAMSA", "lahiri").lower()
            
            if ayanamsa_type == "raman":
                swe.set_sid_mode(swe.SIDM_RAMAN)
                ayanamsa_name = "Raman"
            elif ayanamsa_type == "krishnamurti":
                swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
                ayanamsa_name = "Krishnamurti"
            else:
                swe.set_sid_mode(swe.SIDM_LAHIRI)
                ayanamsa_name = "Lahiri"
            
            print(f"✅ Swiss Ephemeris initialized with {ayanamsa_name} Ayanamsa (Sidereal mode)")
    
    def datetime_to_julian_day(self, dt: datetime) -> float:
        """Convert datetime to Julian Day Number"""
        if not SWISSEPH_AVAILABLE:
            return 0.0
        
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
        
        return swe.julday(year, month, day, hour)
    
    def get_zodiac_sign(self, longitude: float) -> str:
        """Get zodiac sign from longitude (0-360 degrees)"""
        # Normalize longitude to 0-360 range
        longitude = longitude % 360
        sign_index = int(longitude / 30)
        return ZODIAC_SIGNS[sign_index]
    
    def get_nakshatra(self, longitude: float) -> Dict[str, Any]:
        """Get nakshatra (lunar mansion) from longitude"""
        # Normalize longitude to 0-360 range
        longitude = longitude % 360
        
        # Each nakshatra is 13°20' (13.333 degrees)
        nakshatra_span = 360 / 27
        nakshatra_index = int(longitude / nakshatra_span)
        
        # Pada (quarter) within nakshatra
        position_in_nakshatra = (longitude % nakshatra_span) / nakshatra_span
        pada = int(position_in_nakshatra * 4) + 1
        
        return {
            "name": NAKSHATRAS[nakshatra_index],
            "pada": pada,
            "degree_in_nakshatra": position_in_nakshatra * nakshatra_span
        }
    
    def get_planetary_dignity(self, planet: str, sign: str) -> str:
        """Determine if planet is exalted, debilitated, or neutral"""
        if planet in EXALTATION_SIGNS and EXALTATION_SIGNS[planet] == sign:
            return "Exalted"
        elif planet in DEBILITATION_SIGNS and DEBILITATION_SIGNS[planet] == sign:
            return "Debilitated"
        else:
            return "Normal"
    
    def is_retrograde(self, planet: str, jd: float) -> bool:
        """Check if a planet is in retrograde motion"""
        if not SWISSEPH_AVAILABLE or planet in ["Sun", "Moon", "Rahu", "Ketu"]:
            return False
        
        try:
            planet_id = PLANETS.get(planet)
            if planet_id is None:
                return False
            
            # Calculate position with speed
            result = swe.calc_ut(jd, planet_id)
            speed = result[0][3]  # Daily speed in longitude
            
            # Negative speed means retrograde
            return speed < 0
        except Exception as e:
            print(f"Error checking retrograde for {planet}: {e}")
            return False
    
    def calculate_planet_position(self, planet: str, dt: datetime) -> Optional[Dict[str, Any]]:
        """Calculate position for a single planet"""
        if not SWISSEPH_AVAILABLE:
            return None
        
        try:
            jd = self.datetime_to_julian_day(dt)
            planet_id = PLANETS.get(planet)
            
            if planet_id is None:
                return None
            
            # Special handling for Ketu (opposite of Rahu)
            if planet == "Ketu":
                rahu_result = swe.calc_ut(jd, PLANETS['Rahu'])
                rahu_long = rahu_result[0][0]
                
                # Apply sidereal correction to Rahu first
                ayanamsa = swe.get_ayanamsa_ut(jd)
                rahu_long = (rahu_long - ayanamsa) % 360
                
                # Ketu is opposite of Rahu
                longitude = (rahu_long + 180) % 360
                latitude = -rahu_result[0][1]
                speed = rahu_result[0][3]
            else:
                result = swe.calc_ut(jd, planet_id)
                longitude = result[0][0]
                latitude = result[0][1]
                speed = result[0][3]
                
                # Apply sidereal correction for Vedic astrology (including Rahu)
                ayanamsa = swe.get_ayanamsa_ut(jd)
                longitude = (longitude - ayanamsa) % 360
            
            sign = self.get_zodiac_sign(longitude)
            dignity = self.get_planetary_dignity(planet, sign)
            retrograde = self.is_retrograde(planet, jd)
            
            # Calculate degree within sign
            degree_in_sign = longitude % 30
            
            return {
                "planet": planet,
                "longitude": round(longitude, 4),
                "latitude": round(latitude, 4),
                "sign": sign,
                "degree_in_sign": round(degree_in_sign, 4),
                "dignity": dignity,
                "retrograde": retrograde,
                "motion": "Retrograde" if retrograde else "Direct",
                "speed": round(speed, 4)
            }
        
        except Exception as e:
            print(f"Error calculating position for {planet}: {e}")
            return None
    
    def get_all_planetary_positions(self, dt: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Calculate positions for all planets
        
        Args:
            dt: DateTime to calculate for (defaults to now)
        
        Returns:
            List of planetary position dictionaries
        """
        if dt is None:
            dt = datetime.utcnow()
        
        if not self.use_real_ephemeris:
            return []
        
        positions = []
        for planet_name in PLANETS.keys():
            position = self.calculate_planet_position(planet_name, dt)
            if position:
                positions.append(position)
        
        return positions
    
    def get_moon_nakshatra(self, dt: Optional[datetime] = None) -> Optional[Dict[str, Any]]:
        """Get current nakshatra of the Moon"""
        if dt is None:
            dt = datetime.utcnow()
        
        moon_position = self.calculate_planet_position("Moon", dt)
        if not moon_position:
            return None
        
        nakshatra = self.get_nakshatra(moon_position["longitude"])
        return {
            **nakshatra,
            "moon_position": moon_position
        }
    
    def format_for_api(self, positions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format planetary positions for API compatibility
        Matches the format expected by astrology_engine
        """
        formatted = []
        for pos in positions:
            formatted.append({
                "planet": pos["planet"],
                "sign": pos["sign"],
                "motion": pos["motion"],
                "status": pos["dignity"],
                "date": datetime.utcnow().date().isoformat(),
                "longitude": pos["longitude"],
                "nakshatra": self.get_nakshatra(pos["longitude"])["name"] if pos["planet"] == "Moon" else None
            })
        
        return formatted
    
    def get_planetary_transits(self, dt: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Get planetary transits in the format expected by the application
        
        This is the main function to replace mock data
        """
        positions = self.get_all_planetary_positions(dt)
        return self.format_for_api(positions)


# Global instance
ephemeris_service = EphemerisService()


# Convenience functions
def get_current_planetary_positions() -> List[Dict[str, Any]]:
    """Get current planetary positions"""
    return ephemeris_service.get_all_planetary_positions()


def get_planetary_transits(dt: Optional[datetime] = None) -> List[Dict[str, Any]]:
    """Get planetary transits for API use"""
    return ephemeris_service.get_planetary_transits(dt)


def get_moon_nakshatra() -> Optional[Dict[str, Any]]:
    """Get current Moon nakshatra"""
    return ephemeris_service.get_moon_nakshatra()


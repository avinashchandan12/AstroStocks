"""
Astrology Engine - Core Vedic Astrology Logic
Maps planets, signs, elements to market sectors
"""
from typing import Dict, List, Any


# Planet to Element Mapping (Vedic Astrology)
PLANET_ELEMENT_MAP = {
    "Sun": "Fire",
    "Moon": "Water",
    "Mars": "Fire",
    "Mercury": "Earth",
    "Jupiter": "Ether",
    "Venus": "Water",
    "Saturn": "Air",
    "Rahu": "Air",
    "Ketu": "Fire"
}

# Sign to Element Mapping
SIGN_ELEMENT_MAP = {
    "Aries": "Fire",
    "Taurus": "Earth",
    "Gemini": "Air",
    "Cancer": "Water",
    "Leo": "Fire",
    "Virgo": "Earth",
    "Libra": "Air",
    "Scorpio": "Water",
    "Sagittarius": "Fire",
    "Capricorn": "Earth",
    "Aquarius": "Air",
    "Pisces": "Water"
}

# Element to Sector Mapping
ELEMENT_SECTOR_MAP = {
    "Fire": ["Energy", "Oil & Gas", "Power", "Automotive"],
    "Earth": ["Real Estate", "Agriculture", "Mining", "Construction", "FMCG"],
    "Water": ["Chemicals", "Pharmaceuticals", "Beverages", "Marine"],
    "Air": ["Technology", "Telecom", "Aviation", "Media"],
    "Ether": ["Banking", "Finance", "Insurance", "Education"]
}

# Planet Significations for Markets
PLANET_MARKET_SIGNIFICATIONS = {
    "Jupiter": {
        "sectors": ["Banking", "Finance", "Education", "Pharma"],
        "qualities": ["Expansion", "Growth", "Wisdom", "Prosperity"],
        "exalted_in": "Cancer",
        "debilitated_in": "Capricorn"
    },
    "Saturn": {
        "sectors": ["Iron & Steel", "Oil", "Mining", "Real Estate"],
        "qualities": ["Discipline", "Restriction", "Delay", "Stability"],
        "exalted_in": "Libra",
        "debilitated_in": "Aries"
    },
    "Mars": {
        "sectors": ["Defense", "Real Estate", "Energy", "Machinery"],
        "qualities": ["Action", "Energy", "Aggression", "Speed"],
        "exalted_in": "Capricorn",
        "debilitated_in": "Cancer"
    },
    "Venus": {
        "sectors": ["Luxury Goods", "Entertainment", "Hospitality", "Fashion"],
        "qualities": ["Beauty", "Harmony", "Pleasure", "Wealth"],
        "exalted_in": "Pisces",
        "debilitated_in": "Virgo"
    },
    "Mercury": {
        "sectors": ["IT", "Communication", "Trading", "Commerce"],
        "qualities": ["Intelligence", "Communication", "Analysis", "Trade"],
        "exalted_in": "Virgo",
        "debilitated_in": "Pisces"
    },
    "Moon": {
        "sectors": ["FMCG", "Dairy", "Public Services", "Hospitality"],
        "qualities": ["Emotions", "Public", "Fluctuation", "Nourishment"],
        "exalted_in": "Taurus",
        "debilitated_in": "Scorpio"
    },
    "Sun": {
        "sectors": ["Government", "Pharmaceuticals", "Gold", "Power"],
        "qualities": ["Authority", "Leadership", "Vitality", "Government"],
        "exalted_in": "Aries",
        "debilitated_in": "Libra"
    },
    "Rahu": {
        "sectors": ["Technology", "Foreign Trade", "Aviation", "Speculation"],
        "qualities": ["Innovation", "Foreign", "Unconventional", "Sudden Changes"],
        "exalted_in": "Taurus",
        "debilitated_in": "Scorpio"
    },
    "Ketu": {
        "sectors": ["Spirituality", "Research", "Occult", "Electronics"],
        "qualities": ["Detachment", "Liberation", "Research", "Mysticism"],
        "exalted_in": "Scorpio",
        "debilitated_in": "Taurus"
    }
}


class AstrologyEngine:
    """Core engine for astrological analysis of markets"""
    
    def __init__(self):
        self.planet_element_map = PLANET_ELEMENT_MAP
        self.sign_element_map = SIGN_ELEMENT_MAP
        self.element_sector_map = ELEMENT_SECTOR_MAP
        self.planet_significations = PLANET_MARKET_SIGNIFICATIONS
    
    def analyze_transit(self, planet: str, sign: str, motion: str = "Direct", status: str = "Normal") -> Dict[str, Any]:
        """
        Analyze a single planetary transit and return its market implications
        """
        if planet not in self.planet_significations:
            return {"error": f"Unknown planet: {planet}"}
        
        planet_data = self.planet_significations[planet]
        sign_element = self.sign_element_map.get(sign, "Unknown")
        planet_element = self.planet_element_map.get(planet, "Unknown")
        
        # Determine strength of transit
        strength = "Neutral"
        if sign == planet_data.get("exalted_in"):
            strength = "Exalted (Very Strong)"
        elif sign == planet_data.get("debilitated_in"):
            strength = "Debilitated (Weak)"
        
        # Retrograde consideration
        if motion == "Retrograde":
            strength += " + Retrograde (Introspective/Delayed)"
        
        # Affected sectors
        affected_sectors = []
        
        # Direct planet sectors
        affected_sectors.extend(planet_data["sectors"])
        
        # Element-based sectors
        if sign_element in self.element_sector_map:
            affected_sectors.extend(self.element_sector_map[sign_element])
        
        # Remove duplicates
        affected_sectors = list(set(affected_sectors))
        
        return {
            "planet": planet,
            "sign": sign,
            "element": sign_element,
            "strength": strength,
            "motion": motion,
            "affected_sectors": affected_sectors,
            "qualities": planet_data["qualities"],
            "influence_type": self._determine_influence_type(strength, motion)
        }
    
    def _determine_influence_type(self, strength: str, motion: str) -> str:
        """Determine if influence is positive, negative, or mixed"""
        if "Exalted" in strength and motion == "Direct":
            return "Highly Positive"
        elif "Debilitated" in strength:
            return "Challenging"
        elif "Retrograde" in motion:
            return "Mixed (Delays/Review)"
        else:
            return "Positive"
    
    def analyze_sector_influences(self, transits: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Aggregate all transits and determine sector-wise influences
        """
        sector_influences = {}
        
        for transit_data in transits:
            planet = transit_data.get("planet")
            sign = transit_data.get("sign")
            motion = transit_data.get("motion", "Direct")
            status = transit_data.get("status", "Normal")
            
            analysis = self.analyze_transit(planet, sign, motion, status)
            
            for sector in analysis.get("affected_sectors", []):
                if sector not in sector_influences:
                    sector_influences[sector] = []
                
                sector_influences[sector].append({
                    "planet": planet,
                    "sign": sign,
                    "strength": analysis["strength"],
                    "influence_type": analysis["influence_type"],
                    "qualities": analysis["qualities"]
                })
        
        return sector_influences
    
    def get_sector_prediction(self, sector: str, influences: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a prediction for a specific sector based on its planetary influences
        """
        if not influences:
            return {
                "sector": sector,
                "trend": "Neutral",
                "confidence": "Low",
                "reason": "No significant planetary influences detected"
            }
        
        # Count positive vs challenging influences
        positive_count = sum(1 for inf in influences if "Positive" in inf.get("influence_type", ""))
        challenging_count = sum(1 for inf in influences if "Challenging" in inf.get("influence_type", ""))
        
        # Determine overall trend
        if positive_count > challenging_count:
            trend = "Bullish"
            confidence = "Medium" if positive_count > challenging_count + 1 else "Low"
        elif challenging_count > positive_count:
            trend = "Bearish"
            confidence = "Medium" if challenging_count > positive_count + 1 else "Low"
        else:
            trend = "Neutral"
            confidence = "Low"
        
        # Build reason
        planet_list = [inf["planet"] for inf in influences]
        reason = f"Influenced by {', '.join(planet_list[:3])}. "
        
        # Add specific reasons
        for inf in influences[:2]:  # Top 2 influences
            reason += f"{inf['planet']} in {inf['sign']} ({inf['strength']}). "
        
        return {
            "sector": sector,
            "trend": trend,
            "confidence": confidence,
            "reason": reason.strip(),
            "planetary_influences": influences
        }


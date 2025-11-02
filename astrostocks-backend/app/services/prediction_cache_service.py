"""
Prediction Cache Service
Handles caching of prediction and analysis results to save API resources
"""
from typing import Dict, Any, Optional
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from app.models.models import PredictionCache, AnalyzeCache


class PredictionCacheService:
    """Service for managing prediction and analysis cache"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _serialize_datetime(self, obj: Any) -> Any:
        """
        Recursively serialize datetime objects to ISO format strings
        
        Args:
            obj: Object to serialize
            
        Returns:
            Serialized object with datetime as ISO strings
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {key: self._serialize_datetime(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_datetime(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self._serialize_datetime(item) for item in obj)
        else:
            return obj
    
    def get_prediction_cache(self, prediction_date: date) -> Optional[Dict[str, Any]]:
        """
        Get cached prediction for a specific date
        
        Args:
            prediction_date: Date to lookup
            
        Returns:
            Cached prediction data or None if not found
        """
        cached = self.db.query(PredictionCache).filter(
            PredictionCache.prediction_date == prediction_date
        ).first()
        
        if cached:
            print(f"✅ Cache HIT for prediction date: {prediction_date}")
            return cached.response_data
        else:
            print(f"❌ Cache MISS for prediction date: {prediction_date}")
            return None
    
    def save_prediction_cache(self, prediction_date: date, response_data: Dict[str, Any]) -> PredictionCache:
        """
        Save prediction to cache
        
        Args:
            prediction_date: Date of prediction
            response_data: Full response data to cache
            
        Returns:
            Saved cache record
        """
        # Serialize datetime objects to ISO format strings
        serialized_data = self._serialize_datetime(response_data)
        
        # Check if cache exists
        existing = self.db.query(PredictionCache).filter(
            PredictionCache.prediction_date == prediction_date
        ).first()
        
        if existing:
            # Update existing cache
            existing.response_data = serialized_data
            existing.updated_at = datetime.utcnow()
            print(f"✅ Updated cache for prediction date: {prediction_date}")
            return existing
        else:
            # Create new cache
            cache = PredictionCache(
                prediction_date=prediction_date,
                response_data=serialized_data
            )
            self.db.add(cache)
            print(f"✅ Created new cache for prediction date: {prediction_date}")
            return cache
    
    def get_analyze_cache(self, analysis_date: date, endpoint_type: str) -> Optional[Dict[str, Any]]:
        """
        Get cached analysis for a specific date and endpoint type
        
        Args:
            analysis_date: Date to lookup
            endpoint_type: 'basic' or 'enhanced'
            
        Returns:
            Cached analysis data or None if not found
        """
        cached = self.db.query(AnalyzeCache).filter(
            AnalyzeCache.analysis_date == analysis_date,
            AnalyzeCache.endpoint_type == endpoint_type
        ).first()
        
        if cached:
            print(f"✅ Cache HIT for {endpoint_type} analysis date: {analysis_date}")
            return cached.response_data
        else:
            print(f"❌ Cache MISS for {endpoint_type} analysis date: {analysis_date}")
            return None
    
    def save_analyze_cache(self, analysis_date: date, endpoint_type: str, response_data: Dict[str, Any]) -> AnalyzeCache:
        """
        Save analysis to cache
        
        Args:
            analysis_date: Date of analysis
            endpoint_type: 'basic' or 'enhanced'
            response_data: Full response data to cache
            
        Returns:
            Saved cache record
        """
        # Serialize datetime objects to ISO format strings
        serialized_data = self._serialize_datetime(response_data)
        
        # Check if cache exists
        existing = self.db.query(AnalyzeCache).filter(
            AnalyzeCache.analysis_date == analysis_date,
            AnalyzeCache.endpoint_type == endpoint_type
        ).first()
        
        if existing:
            # Update existing cache
            existing.response_data = serialized_data
            existing.updated_at = datetime.utcnow()
            print(f"✅ Updated cache for {endpoint_type} analysis date: {analysis_date}")
            return existing
        else:
            # Create new cache
            cache = AnalyzeCache(
                analysis_date=analysis_date,
                endpoint_type=endpoint_type,
                response_data=serialized_data
            )
            self.db.add(cache)
            print(f"✅ Created new cache for {endpoint_type} analysis date: {analysis_date}")
            return cache
    
    def clear_expired_cache(self, days: int = 30):
        """
        Clear cache older than specified days
        
        Args:
            days: Number of days to keep cache
        """
        cutoff_date = date.today() - timedelta(days=days)
        
        # Clear prediction cache
        prediction_count = self.db.query(PredictionCache).filter(
            PredictionCache.prediction_date < cutoff_date
        ).delete()
        
        # Clear analyze cache
        analyze_count = self.db.query(AnalyzeCache).filter(
            AnalyzeCache.analysis_date < cutoff_date
        ).delete()
        
        self.db.commit()
        
        print(f"🗑️  Cleared {prediction_count} prediction caches and {analyze_count} analysis caches older than {days} days")
    
    def delete_analyze_cache(self, analysis_date: date, endpoint_type: str) -> bool:
        """
        Delete cached analysis for a specific date and endpoint type
        
        Args:
            analysis_date: Date to delete cache for
            endpoint_type: 'basic' or 'enhanced'
            
        Returns:
            True if deleted, False if not found
        """
        cached = self.db.query(AnalyzeCache).filter(
            AnalyzeCache.analysis_date == analysis_date,
            AnalyzeCache.endpoint_type == endpoint_type
        ).first()
        
        if cached:
            self.db.delete(cached)
            print(f"🗑️  Deleted cache for {endpoint_type} analysis date: {analysis_date}")
            return True
        else:
            print(f"⚠️  No cache found to delete for {endpoint_type} analysis date: {analysis_date}")
            return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache statistics
        """
        total_predictions = self.db.query(PredictionCache).count()
        total_analyzes = self.db.query(AnalyzeCache).count()
        
        return {
            "prediction_cache_count": total_predictions,
            "analyze_cache_count": total_analyzes,
            "total_caches": total_predictions + total_analyzes
        }

        


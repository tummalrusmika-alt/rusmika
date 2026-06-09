from geopy.geocoders import Nominatim
import logging

logger = logging.getLogger(__name__)

class GeolocationService:
    """
    Handle geolocation and reverse geocoding
    """
    
    def __init__(self):
        """Initialize geolocation service"""
        try:
            self.geocoder = Nominatim(user_agent="local_problem_reporter")
        except Exception as e:
            logger.error(f"Failed to initialize geocoder: {str(e)}")
            self.geocoder = None
    
    async def get_location_name(
        self,
        latitude: float,
        longitude: float
    ) -> str:
        """
        Get location name from coordinates (reverse geocoding)
        """
        try:
            if not self.geocoder:
                return f"{latitude}, {longitude}"
            
            location = self.geocoder.reverse(f"{latitude}, {longitude}")
            return location.address if location else f"{latitude}, {longitude}"
            
        except Exception as e:
            logger.error(f"Error getting location name: {str(e)}")
            return f"{latitude}, {longitude}"
    
    async def get_coordinates(
        self,
        location_name: str
    ) -> tuple:
        """
        Get coordinates from location name (geocoding)
        
        Returns:
            (latitude, longitude) tuple or (None, None) if not found
        """
        try:
            if not self.geocoder:
                return None, None
            
            location = self.geocoder.geocode(location_name)
            if location:
                return location.latitude, location.longitude
            return None, None
            
        except Exception as e:
            logger.error(f"Error getting coordinates: {str(e)}")
            return None, None
    
    @staticmethod
    def calculate_distance(
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:
        """
        Calculate distance between two coordinates (in km)
        Using Haversine formula
        """
        from math import radians, cos, sin, asin, sqrt
        
        try:
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
            
            # Haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * asin(sqrt(a))
            r = 6371  # Radius of earth in kilometers
            
            return c * r
            
        except Exception as e:
            logger.error(f"Error calculating distance: {str(e)}")
            return 0.0

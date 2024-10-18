from typing import List, Dict, Any
import os, requests
from . import config
from pydantic import BaseModel

class AnalyticsRequest(BaseModel):
    site_id: str
    metrics: List[str]
    date_range: str
    dimensions: List[str]

    class Config:
        schema_extra = {
            "example": {
                "site_id": "nerdidads.com",
                "metrics": ["visitors", "pageviews", "bounce_rate"],
                "date_range": "7d",
                "dimensions": [
                    "visit:country_name",
                    "visit:city_name",
                    "visit:source",
                    "visit:device",
                    "visit:browser",
                    "visit:os"
                ]
            }
        }

class AnalyticsClient:
    def __init__(self):
        self.base_url = os.getenv('API_BASE_URL')
        self.api_key = os.getenv('API_KEY')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })

    def get_analytics(self, 
                     site_id: str,
                     metrics: List[str],
                     date_range: str,
                     dimensions: List[str]) -> dict:
        """
        Fetch analytics data based on specified parameters.
        
        Args:
            site_id (str): The website identifier
            metrics (List[str]): List of metrics to fetch
            date_range (str): Time range for the data
            dimensions (List[str]): List of dimensions to include
        
        Returns:
            dict: The analytics data
        """
        request_data = AnalyticsRequest(
            site_id=site_id,
            metrics=metrics,
            date_range=date_range,
            dimensions=dimensions
        )
        
        response = self.session.post(
            f"{self.base_url}",
            json=request_data.dict()
        )
        response.raise_for_status()
        return response.json()
        
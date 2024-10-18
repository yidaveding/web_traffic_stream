from typing import Dict, List, Any
from datetime import datetime, timezone
import json
import uuid

def transform_for_eventhub(analytics_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Transform analytics response into a list of events suitable for Azure Event Hub.
    
    Args:
        analytics_response (Dict[str, Any]): The original analytics response
        
    Returns:
        List[Dict[str, Any]]: A list of events ready for Event Hub
    """
    events = []
    
    # Extract common metadata
    site_id = analytics_response['query']['site_id']
    date_range = analytics_response['query']['date_range']
    metric_names = analytics_response['query']['metrics']
    dimension_names = analytics_response['query']['dimensions']
    
    for result in analytics_response['results']:
        event = {
            # Required Event Hub metadata
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'type': 'web_analytics_event',
            
            # Analytics data
            'data': {
                'site_id': site_id,
                'date_range': {
                    'start': date_range[0],
                    'end': date_range[1]
                },
                'metrics': {
                    metric_names[i]: result['metrics'][i]
                    for i in range(len(metric_names))
                },
                'dimensions': {
                    dimension_names[i].split(':')[1]: result['dimensions'][i]
                    for i in range(len(dimension_names))
                }
            }
        }
        events.append(event)
    
    return events
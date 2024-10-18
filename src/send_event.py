from azure.eventhub import EventHubProducerClient, EventData
from typing import List, Dict, Any
import os
import json
from dotenv import load_dotenv

class EventHubSender:
    def __init__(self):
        load_dotenv()
        self.connection_string = os.getenv("EVENTHUB_CONNECTION_STRING")
        self.eventhub_name = os.getenv("EVENTHUB_NAME")
        self.producer = None

    def __enter__(self):
        self.producer = EventHubProducerClient.from_connection_string(
            conn_str=self.connection_string,
            eventhub_name=self.eventhub_name
        )
        return self
    
    async def __aenter__(self):
        self.producer = EventHubProducerClient.from_connection_string(
            conn_str=self.connection_string,
            eventhub_name=self.eventhub_name
        )
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self.producer.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.producer.close()

    async def send_events(self, events: List[Dict[str, Any]]):
        event_data_batch = self.producer.create_batch()
        
        for event in events:
            event_data = EventData(json.dumps(event))
            try:
                event_data_batch.add(event_data)
            except ValueError:
                # If the batch is full, send it and create a new one
                self.producer.send_batch(event_data_batch)
                event_data_batch = self.producer.create_batch()
                event_data_batch.add(event_data)
            
        # Send the final batch of events
        if len(event_data_batch) > 0:
            self.producer.send_batch(event_data_batch)

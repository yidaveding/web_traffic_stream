import pytest
from src.api_client import APIClient

def test_api_client_get(requests_mock):
    client = APIClient()
    requests_mock.get(f"{client.base_url}/test", json={"status": "ok"})
    
    response = client.get("test")
    assert response == {"status": "ok"}
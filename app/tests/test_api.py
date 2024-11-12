import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app
from flask import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_resort(client):
    """Test adding a new resort to all_resorts collection."""
    new_resort = {
        "resort_name": "Test Resort",
        "snow_forecast_name": "Test Snow Forecast",
        "infonieve_name": "Test Infonieve"
    }
    response = client.post('/api/resorts/add', data=json.dumps(new_resort), content_type='application/json')
    assert response.status_code in [200, 201]
    data = response.get_json()
    assert 'message' in data

def test_delete_resort(client):
    """Test deleting an existing resort from all_resorts collection."""
    # Add resort first for delete testing
    new_resort = {
        "resort_name": "Test Resort",
        "snow_forecast_name": "Test Snow Forecast",
        "infonieve_name": "Test Infonieve"
    }
    client.post('/api/resorts/add', data=json.dumps(new_resort), content_type='application/json')

    # Now delete the resort
    response = client.delete('/api/resorts/delete', data=json.dumps({"resort_name": "Test Resort"}), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "Resort deleted successfully."

    # Verify that the resort no longer exists
    response = client.delete('/api/resorts/delete', data=json.dumps({"resort_name": "Test Resort"}), content_type='application/json')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == "Resort not found."
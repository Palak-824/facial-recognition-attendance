import os
import tempfile
import pandas as pd
import pytest
from api.attendance_api import app
import sys


# Add project root (Initial_Phase) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.attendance_api import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    """Test the base home route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Flask API running" in response.data

def test_get_attendance_no_date(client):
    """Test /get-attendance with missing date."""
    response = client.get('/get-attendance')
    assert response.status_code == 400
    assert response.json['error'] == "Date not provided"

def test_get_attendance_file_not_found(client):
    """Test /get-attendance when file does not exist."""
    response = client.get('/get-attendance?date=2099-01-01')
    assert response.status_code == 404
    assert "not found" in response.json['error']

def test_get_attendance_success(client):
    """Test /get-attendance when file exists."""
    # Create a temporary CSV file
    with tempfile.TemporaryDirectory() as tempdir:
        test_date = "2025-01-01"
        test_file_path = os.path.join(
            tempdir, f"Attendance_{test_date}.csv"
        )

        # Add dummy data
        df = pd.DataFrame({
            "Id": [1, 2],
            "Name": ["Alice", "Bob"]
        })
        df.to_csv(test_file_path, index=False)

        # Monkeypatch os.path.exists to return True for this path
        original_exists = os.path.exists
        os.path.exists = lambda path: path == test_file_path or original_exists(path)

        # Monkeypatch the file path inside the route
        from api import attendance_api
        attendance_api.os.path.exists = lambda path: path == test_file_path
        attendance_api.pd.read_csv = lambda path, usecols=None: df

        # Make the GET request
        response = client.get(f'/get-attendance?date={test_date}')
        assert response.status_code == 200
        assert response.json == [{'Id': 1, 'Name': 'Alice'}, {'Id': 2, 'Name': 'Bob'}]

        # Restore original functions
        os.path.exists = original_exists

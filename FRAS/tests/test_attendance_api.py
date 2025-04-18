import pytest
import os
import pandas as pd
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.attendance_api import app, FlaskServer

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Flask API running" in response.data

def test_get_attendance_valid_file(client, tmp_path):
    # Create mock CSV file for today's date
    test_date = "01-01-2023"
    file_path = tmp_path / f"Attendance_{test_date}.csv"
    df = pd.DataFrame({"Id": [1], "Name": ["John Doe"]})
    df.to_csv(file_path, index=False)

    # Use patch to mock os.path.exists and pd.read_csv in the Flask app context
    with patch("api.attendance_api.os.path.exists") as mock_exists, \
         patch("api.attendance_api.pd.read_csv") as mock_read_csv:
        
        # Mock the file existence and CSV reading behavior
        mock_exists.return_value = True
        mock_read_csv.return_value = df
        
        # Send GET request to the API with the date parameter
        response = client.get(f"/get-attendance?date={test_date}")

        # Assert the response status code is 200 OK
        assert response.status_code == 200

        # Assert that the response JSON contains the correct data
        response_json = response.get_json()
        assert len(response_json) == 1  # One student in the mock file
        assert response_json[0]['Id'] == 1
        assert response_json[0]['Name'] == "John Doe"

def test_get_attendance_file_not_found(client):
    response = client.get("/get-attendance?date=02-02-2023")
    assert response.status_code == 404
    assert response.is_json
    assert "error" in response.json

def test_get_attendance_missing_date(client):
    response = client.get("/get-attendance")
    assert response.status_code == 400
    assert response.is_json
    assert response.json["error"] == "Date not provided"

def test_flask_server_start_shutdown():
    server = FlaskServer(app)
    server.start()
    assert server.thread.is_alive()
    server.shutdown()
    assert not server.thread.is_alive()

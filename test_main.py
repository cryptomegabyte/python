import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Unit test for prediction logic (mocking the generator)
@patch('main.generator')
def test_predict_text(mock_generator):
    mock_generator.return_value = [{'generated_text': 'Hello world, this is a test'}]

    response = client.post("/predict", json={"text": "Hello world"})
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert response.json()["prediction"] == "Hello world, this is a test"

# Test root endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Text Prediction API"}

# Test with max_length parameter
@patch('main.generator')
def test_predict_with_max_length(mock_generator):
    mock_generator.return_value = [{'generated_text': 'Short text'}]

    response = client.post("/predict", json={"text": "Test", "max_length": 10})
    assert response.status_code == 200
    mock_generator.assert_called_once_with("Test", max_length=10, num_return_sequences=1)

# Test invalid input
def test_predict_invalid_input():
    response = client.post("/predict", json={})
    assert response.status_code == 422  # Unprocessable Entity for missing required field

# Test with empty text
@patch('main.generator')
def test_predict_empty_text(mock_generator):
    mock_generator.return_value = [{'generated_text': 'Generated text'}]

    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 200
    assert "prediction" in response.json()
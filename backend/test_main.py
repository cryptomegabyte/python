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
    data = response.json()
    assert "prediction" in data
    assert data["prediction"] == "Hello world, this is a test"
    assert data["input_length"] == 11
    assert data["generated_length"] == 16

# Test root endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Text Prediction API", "version": "1.0"}

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

# Test empty text
def test_predict_empty_text():
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422

# Test text too long
def test_predict_text_too_long():
    long_text = "a" * 501
    response = client.post("/predict", json={"text": long_text})
    assert response.status_code == 422

# Test max_length out of range
def test_predict_max_length_too_low():
    response = client.post("/predict", json={"text": "Test", "max_length": 5})
    assert response.status_code == 422

def test_predict_max_length_too_high():
    response = client.post("/predict", json={"text": "Test", "max_length": 250})
    assert response.status_code == 422

# Test whitespace-only text
def test_predict_whitespace_text():
    response = client.post("/predict", json={"text": "   "})
    assert response.status_code == 422
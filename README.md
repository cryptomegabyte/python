# Text Prediction API

A FastAPI demo app that uses machine learning to predict text continuations.

## Setup

1. Create a virtual environment: `python -m venv .venv`
2. Activate: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`

## Run

`uvicorn main:app --reload`

## Usage

- GET `/`: Welcome message
- POST `/predict`: Send JSON with `text` and optional `max_length` to get text prediction.

Example: `curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"text": "Hello world", "max_length": 20}'`

## Testing

Run unit and integration tests: `pytest`

## Demo

Visit http://localhost:8000/docs for interactive API docs.

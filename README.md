# Text Prediction Demo

A full-stack demo showcasing FastAPI backend with ML text prediction and Preact frontend.

## Project Structure

```
├── backend/          # FastAPI application
│   ├── main.py       # Main API code
│   ├── test_main.py  # Unit and integration tests
│   └── requirements.txt
├── frontend/         # Preact application
│   └── src/
└── README.md
```

## Setup

1. **Backend Setup:**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

1. **Start Backend:**
   ```bash
   cd backend
   source .venv/bin/activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. Open http://localhost:5173 in your browser for the frontend, or http://localhost:8000/docs for API docs.

## API Usage

- GET `/`: Welcome message
- POST `/predict`: Send JSON with `text` and optional `max_length` to get text prediction.

Example:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "max_length": 50}'
```

## Testing

Run backend tests:
```bash
cd backend
source .venv/bin/activate
pytest
```

## Features

- **Backend:** FastAPI with ML text generation, input validation, error handling, CORS
- **Frontend:** Preact app with modern UI for text prediction
- **Testing:** Comprehensive unit and integration tests
- **ML:** Uses Hugging Face transformers with distilgpt2 model

# Text Prediction Demo

A full-stack demo showcasing FastAPI backend with ML text prediction and Preact frontend.

## Quick Start

1. **Setup dependencies:**
   ```bash
   make setup
   ```

2. **Run the application:**
   ```bash
   make run
   ```
   This starts both backend (http://localhost:8000) and frontend (http://localhost:5173)

## Project Structure

```
├── backend/          # FastAPI application
│   ├── main.py       # Main API code
│   ├── test_main.py  # Unit and integration tests
│   └── requirements.txt
├── frontend/         # Preact application
│   └── src/
├── Makefile          # Build and run commands
└── README.md
```

## Manual Commands

- **Start backend only:** `make backend`
- **Start frontend only:** `make frontend`
- **Run all tests:** `make test`
- **Run backend tests:** `make test-backend`
- **Run frontend tests:** `make test-frontend`
- **Clean up:** `make clean`
- **View API docs:** `make docs` (opens in browser)

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

Run frontend tests:
```bash
cd frontend
npm test
```

## Features

- **Backend:** FastAPI with ML text generation, input validation, error handling, CORS
- **Frontend:** Preact app with modern UI for text prediction
- **Testing:** Comprehensive unit and integration tests
- **ML:** Uses Hugging Face transformers with distilgpt2 model

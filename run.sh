#!/bin/bash

# Start both backend and frontend for development

echo "Starting Text Prediction Demo..."

# Start backend in background
echo "Starting backend..."
cd backend
source .venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "Backend running on http://localhost:8000"
echo "Frontend running on http://localhost:5173"
echo "Press Ctrl+C to stop both services"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
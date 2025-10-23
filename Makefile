.PHONY: help setup backend frontend run test test-backend test-frontend clean

# Default target
help:
	@echo "Available commands:"
	@echo "  setup         - Install dependencies for both backend and frontend"
	@echo "  backend       - Start the FastAPI backend server"
	@echo "  frontend      - Start the Preact frontend dev server"
	@echo "  run           - Start both backend and frontend servers"
	@echo "  test          - Run all tests (backend and frontend)"
	@echo "  test-backend  - Run backend tests only"
	@echo "  test-frontend - Run frontend tests only"
	@echo "  clean         - Clean up cache files and virtual environments"
	@echo "  docs          - Open API documentation in browser"

# Setup dependencies
setup:
	@echo "Setting up backend..."
	cd backend && python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
	@echo "Setting up frontend..."
	cd frontend && npm install

# Start backend server
backend:
	@echo "Starting FastAPI backend on http://localhost:8000"
	cd backend && . .venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start frontend dev server
frontend:
	@echo "Starting Preact frontend on http://localhost:5173"
	cd frontend && npm run dev

# Start both servers
run:
	@echo "Starting both backend and frontend..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@echo "API Docs: http://localhost:8000/docs"
	@echo "Press Ctrl+C to stop both servers"
	@make -j2 backend frontend

# Run all tests
test: test-backend test-frontend

# Run backend tests
test-backend:
	@echo "Running backend tests..."
	cd backend && . .venv/bin/activate && python -m pytest -v

# Run frontend tests
test-frontend:
	@echo "Running frontend tests..."
	cd frontend && npm test -- --run

# Clean up
clean:
	@echo "Cleaning up..."
	rm -rf backend/.venv
	rm -rf backend/__pycache__
	rm -rf backend/*.pyc
	rm -rf frontend/node_modules
	rm -rf frontend/dist

# Open API documentation
docs:
	@echo "Opening API documentation..."
	@if command -v xdg-open > /dev/null; then \
		xdg-open http://localhost:8000/docs; \
	elif command -v open > /dev/null; then \
		open http://localhost:8000/docs; \
	else \
		echo "Please open http://localhost:8000/docs in your browser"; \
	fi
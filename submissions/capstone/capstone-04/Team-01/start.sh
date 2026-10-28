#!/bin/bash

# Root-level startup script for production structure

echo ""
echo "========================================"
echo "Agile Solutions Control Tower"
echo "Production Startup Script"
echo "========================================"
echo ""

# Start backend
echo "[1/2] Starting Django Backend..."
cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
pip install -q -r requirements.txt

# Run migrations
python manage.py migrate --noinput

# Start Django in background
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

cd ..

sleep 3

# Start frontend
echo "[2/2] Starting React Frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install -q
fi

npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "========================================"
echo "Services Starting..."
echo "========================================"
echo ""
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""

sleep 5

# Try to open in browser
if command -v open &> /dev/null; then
    open http://localhost:5173
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5173
fi

echo "Backend PID: $DJANGO_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

wait

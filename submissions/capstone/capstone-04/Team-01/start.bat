@echo off
REM Root-level startup script for production structure

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Agile Solutions Control Tower
echo Production Startup Script
echo ========================================
echo.

REM Navigate to backend and start Django
echo [1/2] Starting Django Backend...
cd backend

REM Check if venv exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install dependencies
pip install -q -r requirements.txt

REM Run migrations
python manage.py migrate --noinput

REM Start Django in new window
start "Django Backend" cmd /k python manage.py runserver 0.0.0.0:8000

cd ..

timeout /t 3 /nobreak

REM Start React frontend
echo [2/2] Starting React Frontend...
cd frontend

if not exist "node_modules" (
    echo Installing npm dependencies...
    call npm install -q
)

start "React Frontend" cmd /k npm run dev

cd ..

echo.
echo ========================================
echo Services Starting...
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.

timeout /t 5 /nobreak
start "" http://localhost:5173

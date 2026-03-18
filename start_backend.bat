@echo off
REM Backend startup script for Windows

echo.
echo ======================================================
echo BI Dashboard - Backend Startup
echo ======================================================
echo.

REM Check if backend folder exists
if not exist "backend\" (
    echo Error: backend folder not found!
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

REM Check if venv exists
if not exist ".venv\" (
    echo Virtual environment not found. Creating one...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if requirements are installed
echo Checking dependencies...
pip install -q -r backend\requirements.txt

REM Check for .env file
if not exist "backend\.env" (
    echo.
    echo WARNING: backend\.env not found!
    echo Please create it with your GEMINI_API_KEY
    echo Run: copy backend\.env.example backend\.env
    echo Then edit and add your API key
    echo.
)

REM Start the backend
echo.
echo ======================================================
echo Starting Backend API server...
echo ======================================================
echo.
echo API will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause

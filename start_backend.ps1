# Backend startup script for Windows PowerShell

Write-Host "`n======================================================" -ForegroundColor Cyan
Write-Host " BI Dashboard - Backend Startup (PowerShell)" -ForegroundColor Cyan
Write-Host "======================================================`n" -ForegroundColor Cyan

# Check if backend folder exists
if (-not (Test-Path "backend")) {
    Write-Host "Error: backend folder not found!" -ForegroundColor Red
    Write-Host "Please run this script from the project root directory" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if venv exists
if (-not (Test-Path ".venv")) {
    Write-Host "Virtual environment not found. Creating one..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Check if requirements are installed
Write-Host "Checking dependencies..." -ForegroundColor Green
pip install -q -r backend\requirements.txt

# Check for .env file
if (-not (Test-Path "backend\.env")) {
    Write-Host "`nWARNING: backend\.env not found!" -ForegroundColor Yellow
    Write-Host "Please create it with your GEMINI_API_KEY" -ForegroundColor Yellow
    Write-Host "Run: copy backend\.env.example backend\.env" -ForegroundColor Yellow
    Write-Host "Then edit and add your API key`n" -ForegroundColor Yellow
}

# Start the backend
Write-Host "`n======================================================" -ForegroundColor Cyan
Write-Host "Starting Backend API server..." -ForegroundColor Cyan
Write-Host "======================================================`n" -ForegroundColor Cyan

Write-Host "API will be available at: http://localhost:8000" -ForegroundColor Green
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "Database: E-commerce sales data (55 transactions)" -ForegroundColor Green
Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Yellow

Push-Location backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
Pop-Location

Read-Host "Press Enter to exit"

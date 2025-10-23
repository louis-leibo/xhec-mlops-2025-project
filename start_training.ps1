# PowerShell script to start Prefect server and model retraining deployment
# Usage: .\start_training.ps1

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Prefect Model Training Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".\.venv")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: uv sync --all-extras" -ForegroundColor Yellow
    exit 1
}

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
}

# Check if uv is installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: uv is not installed!" -ForegroundColor Red
    Write-Host "Install from: https://github.com/astral-sh/uv" -ForegroundColor Yellow
    exit 1
}

# Check if Prefect is installed
Write-Host "Checking Prefect installation..." -ForegroundColor Yellow
$prefectCheck = & uv run python -c "import prefect; print(prefect.__version__)" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Prefect not found. Installing dependencies..." -ForegroundColor Yellow
    uv sync --all-extras
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install dependencies!" -ForegroundColor Red
        exit 1
    }
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "Prefect version: $prefectCheck" -ForegroundColor Green
}

# Check SQLite availability (Prefect requirement)
Write-Host "Checking SQLite..." -ForegroundColor Yellow
$sqliteCheck = & uv run python -c "import sqlite3; print(f'SQLite {sqlite3.sqlite_version}')" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "$sqliteCheck" -ForegroundColor Green
} else {
    Write-Host "WARNING: SQLite check failed, but it's usually built-in with Python" -ForegroundColor Yellow
}

Write-Host ""

Write-Host "Starting Prefect server in background..." -ForegroundColor Green

# Start Prefect server in a new PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\.venv\Scripts\Activate.ps1; Write-Host 'Starting Prefect Server...' -ForegroundColor Cyan; uv run prefect server start --host localhost"

# Wait for server to start
Write-Host "Waiting for Prefect server to initialize (15 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  Prefect UI available at:" -ForegroundColor Green
Write-Host "  http://127.0.0.1:4200" -ForegroundColor White
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Host "Starting model retraining deployment..." -ForegroundColor Green
Write-Host ""

# Run the deployment script
uv run python src/deployment.py

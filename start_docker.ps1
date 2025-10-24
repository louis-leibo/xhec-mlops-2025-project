# PowerShell script to start all services with Docker Compose
# Usage: .\start_docker.ps1

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Starting Abalone MLOps Platform" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    docker info | Out-Null
    Write-Host "Docker is running!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Docker is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
    exit 1
}

# Check if docker-compose is available
Write-Host "Checking docker-compose..." -ForegroundColor Yellow
if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
    Write-Host "docker-compose found!" -ForegroundColor Green
    $COMPOSE_CMD = "docker-compose"
} elseif (docker compose version 2>$null) {
    Write-Host "docker compose (plugin) found!" -ForegroundColor Green
    $COMPOSE_CMD = "docker compose"
} else {
    Write-Host "ERROR: docker-compose not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Building and starting services..." -ForegroundColor Green
Write-Host ""

# Build and start all services
& $COMPOSE_CMD up --build -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "  Services Started Successfully!" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Access the services at:" -ForegroundColor Cyan
    Write-Host "  API:           http://localhost:8001" -ForegroundColor White
    Write-Host "  API Docs:      http://localhost:8001/docs" -ForegroundColor White
    Write-Host "  Prefect UI:    http://localhost:4200" -ForegroundColor White
    Write-Host "  MLflow UI:     http://localhost:5000" -ForegroundColor White
    Write-Host ""
    Write-Host "Useful commands:" -ForegroundColor Cyan
    Write-Host "  View logs:     $COMPOSE_CMD logs -f" -ForegroundColor White
    Write-Host "  Stop all:      $COMPOSE_CMD down" -ForegroundColor White
    Write-Host "  Restart:       $COMPOSE_CMD restart" -ForegroundColor White
    Write-Host "  View status:   $COMPOSE_CMD ps" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "ERROR: Failed to start services!" -ForegroundColor Red
    Write-Host "Check logs with: $COMPOSE_CMD logs" -ForegroundColor Yellow
    exit 1
}

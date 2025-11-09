# PowerShell script to fix cq-agent installation
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "cq-agent Installation Fix Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the Code-Quality-Agent directory
if (-not (Test-Path "setup.py") -and -not (Test-Path "pyproject.toml")) {
    Write-Host "ERROR: This script must be run from the Code-Quality-Agent directory!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please:" -ForegroundColor Yellow
    Write-Host "  1. Navigate to: E:\Code-Quality-Agent" -ForegroundColor Yellow
    Write-Host "  2. Run this script again" -ForegroundColor Yellow
    exit 1
}

Write-Host "Step 1: Uninstalling existing cq-agent (if any)..." -ForegroundColor Yellow
python -m pip uninstall cq-agent -y 2>$null

Write-Host ""
Write-Host "Step 2: Installing cq-agent..." -ForegroundColor Yellow
python -m pip install --upgrade --force-reinstall .

Write-Host ""
Write-Host "Step 3: Verifying installation..." -ForegroundColor Yellow
python -m pip show cq-agent

Write-Host ""
Write-Host "Step 4: Testing the command..." -ForegroundColor Yellow
cq-agent --help

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✓ Installation successful!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now use 'cq-agent' from any directory:" -ForegroundColor Cyan
    Write-Host "  cq-agent analyze ." -ForegroundColor White
    Write-Host "  cq-agent qa ." -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "✗ Installation verification failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please check:" -ForegroundColor Yellow
    Write-Host "  1. Python version: python --version (needs 3.11+)" -ForegroundColor Yellow
    Write-Host "  2. Pip version: pip --version" -ForegroundColor Yellow
    Write-Host "  3. Try: python -m pip install --upgrade pip" -ForegroundColor Yellow
}


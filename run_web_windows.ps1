# PowerShell script to run Streamlit web interface on Windows
# This ensures proper localhost configuration for Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Code Quality Agent Web Interface" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if streamlit is installed
try {
    $streamlitCheck = python -c "import streamlit; print('OK')" 2>$null
    if (-not $streamlitCheck) {
        Write-Host "Streamlit not found. Installing..." -ForegroundColor Yellow
        python -m pip install streamlit
    }
} catch {
    Write-Host "Installing Streamlit..." -ForegroundColor Yellow
    python -m pip install streamlit
}

Write-Host ""
Write-Host "🚀 Launching web interface..." -ForegroundColor Green
Write-Host ""
Write-Host "📍 Access at: http://localhost:8501" -ForegroundColor Cyan
Write-Host "   Or:        http://127.0.0.1:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Run Streamlit with Windows-compatible settings
$appPath = Join-Path $PSScriptRoot "src\cq_agent\web\app.py"

if (Test-Path $appPath) {
    python -m streamlit run $appPath --server.address localhost --server.port 8501
} else {
    Write-Host "ERROR: Could not find app.py at: $appPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run this script from the Code-Quality-Agent directory" -ForegroundColor Yellow
    exit 1
}


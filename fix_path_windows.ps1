# PowerShell script to fix PATH for cq-agent on Windows
# This script helps add Python Scripts directory to PATH

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "cq-agent PATH Fix for Windows" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get Python Scripts directory
Write-Host "Finding Python Scripts directory..." -ForegroundColor Yellow
try {
    $scriptsDir = python -c "import site; from pathlib import Path; print(Path(site.getuserbase()) / 'Scripts')" 2>$null
    if (-not $scriptsDir) {
        $scriptsDir = python -c "import site; import os; from pathlib import Path; print(Path(site.getuserbase()) / 'Scripts')" 2>$null
    }
    
    if (-not $scriptsDir -or -not (Test-Path $scriptsDir)) {
        Write-Host "ERROR: Could not find Python Scripts directory!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please check:" -ForegroundColor Yellow
        Write-Host "  1. Python is installed correctly" -ForegroundColor Yellow
        Write-Host "  2. You're using the correct Python version (3.11+)" -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host "Found Scripts directory: $scriptsDir" -ForegroundColor Green
    Write-Host ""
    
    # Check if already in PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $pathEntries = $currentPath -split ';'
    
    if ($pathEntries -contains $scriptsDir -or $pathEntries -contains "$scriptsDir\") {
        Write-Host "✓ Scripts directory is already in PATH!" -ForegroundColor Green
        Write-Host ""
        Write-Host "If 'cq-agent' still doesn't work, try:" -ForegroundColor Yellow
        Write-Host "  1. Close and reopen your terminal/PowerShell" -ForegroundColor Yellow
        Write-Host "  2. Use: python -m cq_agent.cli.main analyze ." -ForegroundColor Yellow
        exit 0
    }
    
    # Ask user if they want to add to PATH
    Write-Host "The Scripts directory is NOT in your PATH." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Would you like to add it to your PATH? (Y/N)" -ForegroundColor Cyan
    $response = Read-Host
    
    if ($response -eq 'Y' -or $response -eq 'y' -or $response -eq 'Yes' -or $response -eq 'yes') {
        # Add to PATH
        $newPath = $currentPath
        if ($newPath -and -not $newPath.EndsWith(';')) {
            $newPath += ';'
        }
        $newPath += $scriptsDir
        
        try {
            [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
            Write-Host ""
            Write-Host "✓ Successfully added to PATH!" -ForegroundColor Green
            Write-Host ""
            Write-Host "IMPORTANT: You must restart your terminal/PowerShell for changes to take effect!" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "After restarting, you can use:" -ForegroundColor Cyan
            Write-Host "  cq-agent analyze ." -ForegroundColor White
            Write-Host ""
            Write-Host "Or use immediately (no restart needed):" -ForegroundColor Cyan
            Write-Host "  python -m cq_agent.cli.main analyze ." -ForegroundColor White
        } catch {
            Write-Host ""
            Write-Host "ERROR: Could not update PATH automatically!" -ForegroundColor Red
            Write-Host "Error: $_" -ForegroundColor Red
            Write-Host ""
            Write-Host "Please add manually:" -ForegroundColor Yellow
            Write-Host "  1. Press Win + X, select 'System'" -ForegroundColor Yellow
            Write-Host "  2. Click 'Advanced system settings'" -ForegroundColor Yellow
            Write-Host "  3. Click 'Environment Variables'" -ForegroundColor Yellow
            Write-Host "  4. Edit 'Path' under 'User variables'" -ForegroundColor Yellow
            Write-Host "  5. Add: $scriptsDir" -ForegroundColor Yellow
        }
    } else {
        Write-Host ""
        Write-Host "PATH not modified." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "You can still use cq-agent with:" -ForegroundColor Cyan
        Write-Host "  python -m cq_agent.cli.main analyze ." -ForegroundColor White
        Write-Host ""
        Write-Host "Or add to PATH manually:" -ForegroundColor Yellow
        Write-Host "  Add this directory: $scriptsDir" -ForegroundColor White
    }
    
} catch {
    Write-Host ""
    Write-Host "ERROR: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternative: Use Python module syntax (no PATH needed):" -ForegroundColor Yellow
    Write-Host "  python -m cq_agent.cli.main analyze ." -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan


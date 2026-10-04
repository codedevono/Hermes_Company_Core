
Write-Host "Initializing Hermes Company Infrastructure (PowerShell Mode)..." -ForegroundColor Cyan

# Setup paths
$SERVER_DIR = "C:\Users\USER-0\Hermes_Server"
$ENV_PATH = "C:\Users\USER-0\jarvis_env\Scripts\Activate.ps1"

# 1. Activate Environment
if (Test-Path $ENV_PATH) {
    Write-Host "Activating Environment..."
    & $ENV_PATH
} else {
    Write-Host "ERROR: Virtual Environment not found at $ENV_PATH" -ForegroundColor Red
    exit
}

# 2. Prepare Server Environment
if (!(Test-Path "$SERVER_DIR\logs")) {
    New-Item -ItemType Directory -Path "$SERVER_DIR\logs" | Out-Null
}
Set-Location $SERVER_DIR

# 3. Kill existing server instances
Write-Host "Stopping previous server instances..."
$process = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($process) {
    Write-Host "Killing process $($process.OwningProcess)..."
    Stop-Process -Id $process.OwningProcess -Force
}

# 4. Start Server in background
Write-Host "Starting Hermes-Core Server on port 8000..."
Start-Process python -ArgumentList "main.py" -WindowStyle Hidden -RedirectStandardOutput "logs\server_stdout.log" -RedirectStandardError "logs\server_stderr.log"

# 5. Verification
Write-Host "Verifying server status..."
Start-Sleep -Seconds 5
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing
    Write-Host "SUCCESS: Server is UP and running." -ForegroundColor Green
} catch {
    Write-Host "ERROR: Server failed to start. Check logs\server_stdout.log" -ForegroundColor Red
    exit
}

Write-Host "Android Connectivity: Server is listening on 0.0.0.0:8000"
Write-Host "System Ready." -ForegroundColor Green

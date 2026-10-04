
function Show-Menu {
    Clear-Host
    Write-Host "===========================================" -ForegroundColor Cyan
    Write-Host "       HERMES LIFE-CYCLE MANAGER           " -ForegroundColor Cyan
    Write-Host "===========================================" -ForegroundColor Cyan
    Write-Host " 1. 🚀 WAKE UP (Start Server & Mic)        "
    Write-Host " 2. 💤 SLEEP (Stop Everything)             "
    Write-Host " 3. 🛠️  REBUILD ENVIRONMENT (Clean Setup)  "
    Write-Host " 4. ❌ EXIT                                "
    Write-Host "===========================================" -ForegroundColor Cyan
}

function Start-Hermes {
    Write-Host "`n🚀 Waking up Hermes..." -ForegroundColor Cyan
    # 1. Start Server
    powershell -ExecutionPolicy Bypass -File "C:\Users\USER-0\init_hermes.ps1"
    
    # 2. Start Mic Bridge in a new window so you can see the responses
    Write-Host "🎤 Opening Microphone Bridge..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy Bypass", "-Command", "& 'C:\Users\USER-0\jarvis_env\Scripts\Activate.ps1'; python C:\Users\USER-0\hermes_mic_manual.py"
    
    Write-Host "`n✨ System is LIVE. Hermes is on your lap." -ForegroundColor Green
}

function Stop-Hermes {
    Write-Host "`n💤 Putting Hermes to sleep..." -ForegroundColor Yellow
    # Kill all python processes related to the server and mic
    $procs = Get-Process -Name "python" -ErrorAction SilentlyContinue
    if ($procs) {
        Stop-Process -Name "python" -Force
        Write-Host "Stopped all background processes." -ForegroundColor Green
    } else {
        Write-Host "No active processes found."
    }
    Write-Host "`n🌙 System is now silent. Peace restored." -ForegroundColor Cyan
}

function Rebuild-Env {
    Write-Host "`n🛠️ Rebuilding environment..." -ForegroundColor Yellow
    powershell -ExecutionPolicy Bypass -File "C:\Users\USER-0\setup_jarvis_env.ps1"
}

do {
    Show-Menu
    $choice = Read-Host "Select an option"
    switch ($choice) {
        "1" { Start-Hermes; Read-Host "`nPress Enter to return to menu" }
        "2" { Stop-Hermes; Read-Host "`nPress Enter to return to menu" }
        "3" { Rebuild-Env; Read-Host "`nPress Enter to return to menu" }
        "4" { exit }
    }
} while ($true)

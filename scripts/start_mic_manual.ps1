
Write-Host "🚀 Launching Manual Mic Bridge..." -ForegroundColor Cyan
$ENV_PATH = "C:\Users\USER-0\jarvis_env\Scripts\Activate.ps1"
$SCRIPT_PATH = "C:\Users\USER-0\hermes_mic_manual.py"
powershell -ExecutionPolicy Bypass -Command "& '$ENV_PATH'; python '$SCRIPT_PATH'"

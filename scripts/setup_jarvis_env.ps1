
Write-Host "🛠️ Rebuilding Jarvis Virtual Environment..." -ForegroundColor Cyan

$ENV_PATH = "C:\Users\USER-0\jarvis_env"
$PIP_PACKAGES = "fastapi uvicorn openai-whisper requests sounddevice scipy edge-tts numpy"

# 1. Clean up old environment if it exists
if (Test-Path $ENV_PATH) {
    Write-Host "Removing old environment..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $ENV_PATH
}

# 2. Create new virtual environment
Write-Host "Creating VENV at $ENV_PATH..."
python -m venv $ENV_PATH

# 3. Install packages using the venv's python executable directly
Write-Host "Installing core dependencies... (This may take a few minutes)" -ForegroundColor Yellow
$PYTHON_EXE = "$ENV_PATH\Scripts\python.exe"
& $PYTHON_EXE -m pip install --upgrade pip
& $PYTHON_EXE -m pip install $PIP_PACKAGES

Write-Host "✅ Virtual Environment successfully established!" -ForegroundColor Green
Write-Host "You can now run your init_hermes.ps1 script." -ForegroundColor Cyan

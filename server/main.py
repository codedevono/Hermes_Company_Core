
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
import uvicorn
import whisper
import subprocess
import os
import glob
from datetime import datetime

app = FastAPI()

# CONFIGURATION
DEVICE = "cpu" 
MODEL_SIZE = "small"
AUDIO_INPUT_PATH = "temp_input.wav"
LOG_FILE = "logs/system.log"
VOICE = "en-IN-NeerjaNeural"

print("Initializing Hermes-Core Server (Stabilized Mode)...")
os.makedirs("logs", exist_ok=True)
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] System Initialized.\n")
model = whisper.load_model(MODEL_SIZE, device=DEVICE)

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def get_html_content():
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return "<h1>Error loading UI</h1>"

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return get_html_content()

@app.post("/voice")
async def process_voice(request: Request, file: UploadFile = File(...)):
    log_event(f"Received voice input from {request.client.host}")
    
    # Save audio
    with open(AUDIO_INPUT_PATH, "wb") as buffer:
        buffer.write(await file.read())
    
    # Transcribe
    result = model.transcribe(AUDIO_INPUT_PATH)
    user_text = result['text']
    log_event(f"User said: {user_text}")
    
    # Call Hermes CLI
    try:
        process = subprocess.Popen(["hermes", "-z", user_text], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        stdout, stderr = process.communicate(timeout=15)
        response_text = stdout.strip()
        if not response_text:
            # If stdout is empty, check stderr
            response_text = stderr.strip() if stderr else "I heard you, but I couldn't generate a response."
    except Exception as e:
        response_text = f"Error calling Hermes CLI: {str(e)}"
        
    log_event(f"Hermes responded: {response_text}")
    
    # Trigger TTS
    try:
        # BILINGUAL LOGIC: Determine voice based on response content
        # Simple check: if response contains common Hindi characters/words, use Hindi voice
        # Otherwise, use the Indian English voice.
        
        # Hindi Unicode range: \u0900-\u097F
        import re
        if re.search(r'[\u0900-\u097F]', response_text):
            voice_id = "hi-IN-SwararaNeural"
        else:
            voice_id = "en-IN-NeerjaNeural"
            
        tmp_audio = r"C:\Users\USER-0\AppData\Local\hermes\cache\audio\tmp_res.mp3"
        subprocess.run(["edge-tts", "--voice", voice_id, "--text", response_text, "--write-file", tmp_audio], shell=True, check=True)
        
        # Move to the final location
        if os.path.exists(tmp_audio):
            if os.path.exists(AUDIO_CACHE_FILE):
                os.remove(AUDIO_CACHE_FILE)
            os.rename(tmp_audio, AUDIO_CACHE_FILE)
    except Exception as e:
        log_event(f"TTS Error: {str(e)}")
    
    # Find latest audio file
    cache_dir = os.path.expanduser("~") + r"\AppData\Local\hermes\cache\audio"
    list_of_files = glob.glob(f"{cache_dir}/*.mp3")
    if not list_of_files:
        return {"text": response_text, "audio": None}
    
    latest_audio = max(list_of_files, key=os.path.getctime)
    return {"text": response_text, "audio": latest_audio}

@app.get("/logs")
async def get_logs():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

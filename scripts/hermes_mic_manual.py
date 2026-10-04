
import os
import requests
import time
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import sys

# Fix terminal encoding for "gibberish" characters
if sys.platform == "win32":
    import codecs
    try:
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    except:
        pass

# --- CONFIGURATION ---
SERVER_URL = "http://localhost:8000/voice"
TEMP_AUDIO_FILE = "pc_mic_input.wav"
FS = 16000 
AUDIO_CACHE_FILE = r"C:\Users\USER-0\AppData\Local\hermes\cache\audio\response.mp3"
# ---------------------

def record_manual():
    input("\n[PRESS ENTER TO START RECORDING]")
    print("🔴 RECORDING... (Press Enter again to stop)")
    
    audio_data = []
    def callback(indata, frames, time, status):
        if status: print(status)
        audio_data.append(indata.copy())

    with sd.InputStream(samplerate=FS, channels=1, callback=callback):
        input() 
    
    print("🛑 Stopped. Processing...")
    if not audio_data:
        print("❌ No audio captured.")
        return

    full_audio = np.concatenate(audio_data, axis=0)
    write(TEMP_AUDIO_FILE, FS, full_audio)
    
    try:
        print("📤 Sending to Hermes...")
        with open(TEMP_AUDIO_FILE, "rb") as f:
            files = {"file": ("voice.wav", f, "audio/wav")}
            response = requests.post(SERVER_URL, files=files)
            
        if response.status_code == 200:
            res_json = response.json()
            text = res_json.get('text', 'No text returned')
            print(f"🤖 Hermes: {text}")
            
            # --- PLAY AUDIO ---
            if os.path.exists(AUDIO_CACHE_FILE):
                print("🔊 Playing response...")
                os.startfile(AUDIO_CACHE_FILE)
            else:
                print("⚠️ Audio file not found in cache.")
        else:
            print(f"❌ Server Error: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Request Error: {e}")

if __name__ == "__main__":
    print("--- Hermes Manual Mic Bridge ---")
    print("Control: [Enter] to Start | [Enter] to Stop")
    print("Press Ctrl+C to exit completely")
    try:
        while True:
            record_manual()
            print("\n--- Ready for next command ---")
    except KeyboardInterrupt:
        print("\nStopping Mic Bridge...")

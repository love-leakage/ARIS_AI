# File: core/speech_input.py
import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wav

model = whisper.load_model("base")

# Record voice from mic

def record_audio(duration=5, fs=16000):
    print("🎙️ Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    return audio.flatten(), fs

# Convert and transcribe voice to text

def get_user_input():
    audio, fs = record_audio()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as f:
        wav.write(f.name, fs, audio)
        try:
            result = model.transcribe(f.name)
            print("🗣️ You said:", result["text"])
            return result["text"]
        except Exception as e:
            print("Error in speech recognition:", e)
            return ""

# File: core/tts_output.py
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 160)  # speaking speed
engine.setProperty('volume', 1.0)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)

def speak(text):
    print("🤖 ARIS:", text)
    engine.say(text)
    engine.runAndWait()

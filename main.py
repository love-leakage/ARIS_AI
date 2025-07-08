# File: main.py

import time
from core.speech_input import get_user_input
from core.tts_output import speak
from core.nlp_engine import process_command

WAKE_WORD = "aris"


def main():
    speak("ARIS is online and ready.")
    while True:
        print("Listening...")
        command = get_user_input()
        if command:
            print(f"Heard: {command}")
            if WAKE_WORD in command.lower():
                speak("Yes?")
                command = command.lower().replace(WAKE_WORD, "").strip()
                if command:
                    response = process_command(command)
                    if response:
                        speak(response)
        time.sleep(1)


if __name__ == "__main__":
    main()


# --- File: core/speech_input.py ---
import speech_recognition as sr

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source, phrase_time_limit=5)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""


# --- File: core/tts_output.py ---
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    engine.say(text)
    engine.runAndWait()


# --- File: core/nlp_engine.py ---
import openai
import json
from core.task_executor import execute_command

with open("config/settings.json") as f:
    config = json.load(f)

openai.api_key = config["openai_api_key"]

def process_command(command):
    if command.startswith("open") or "search" in command:
        return execute_command(command)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are ARIS, a smart assistant."},
                {"role": "user", "content": command}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return "I'm having trouble connecting to my brain right now."


# --- File: core/task_executor.py ---
import webbrowser
import os

def execute_command(command):
    if "open youtube" in command:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube."
    elif "open google" in command:
        webbrowser.open("https://google.com")
        return "Opening Google."
    elif "shutdown" in command:
        os.system("shutdown /s /t 1")
        return "Shutting down."
    elif "search" in command:
        search_term = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search_term}")
        return f"Searching for {search_term}."
    else:
        return "Sorry, I don't recognize that action."


# --- File: core/memory_manager.py ---
import json
import os

MEMORY_FILE = "memory.json"

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({}, f)

def remember(key, value):
    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)
    data[key] = value
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)

def recall(key):
    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)
    return data.get(key, "I don't remember that.")

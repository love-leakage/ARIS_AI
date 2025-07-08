# File: core/task_executor.py
import os
import webbrowser
import datetime
from core.tts_output import speak

def execute_command(cmd):
    if cmd == "time":
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}.")

    elif cmd.startswith("http"):
        speak("Opening browser.")
        webbrowser.open(cmd)

    elif cmd.endswith(".exe"):
        speak(f"Launching application: {cmd}")
        os.startfile(cmd)

    else:
        speak(f"Sorry, I don't understand how to execute: {cmd}")

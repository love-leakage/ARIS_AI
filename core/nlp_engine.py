# File: core/nlp_engine.py
from openai import OpenAI
import json
import os
from core.tts_output import speak
from core.task_executor import execute_command

# Load API key
with open("config/settings.json") as f:
    config = json.load(f)
client = OpenAI(api_key=config["openai_api_key"])

# Define basic keyword command map
COMMANDS = {
    "open youtube": lambda: execute_command("https://www.youtube.com"),
    "open google": lambda: execute_command("https://www.google.com"),
    "what is your name": lambda: speak("My name is Aris, your personal assistant."),
    "what time is it": lambda: execute_command("time"),
}

def process_command(command):
    command = command.lower().strip()

    for key in COMMANDS:
        if key in command:
            COMMANDS[key]()
            return f"Executed command: {key}"

    # Fallback to GPT if not in command list
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are ARIS, a helpful and polite AI assistant."},
                {"role": "user", "content": command},
            ]
        )
        reply = response.choices[0].message.content
        speak(reply)
        return reply
    except Exception as e:
        speak("Sorry, I couldn't reach the smart engine.")
        print("GPT error:", e)
        return "Sorry, I couldn't reach the smart engine."

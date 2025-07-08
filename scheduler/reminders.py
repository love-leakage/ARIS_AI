# File: scheduler/reminders.py
import datetime
import json
import os
from core.tts_output import speak

REMINDER_FILE = "config/reminders.json"

# Load reminders from file
def load_reminders():
    if not os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, 'w') as f:
            json.dump([], f)
    with open(REMINDER_FILE, 'r') as f:
        return json.load(f)

# Save reminders to file
def save_reminders(reminders):
    with open(REMINDER_FILE, 'w') as f:
        json.dump(reminders, f, indent=4)

# Check and announce due reminders
def check_reminders():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    reminders = load_reminders()
    remaining = []
    for r in reminders:
        if r['time'] == now:
            speak(f"Reminder: {r['note']}")
        else:
            remaining.append(r)
    save_reminders(remaining)

# Add new reminder (called from NLP or API)
def add_reminder(note, time_str):
    reminders = load_reminders()
    reminders.append({"note": note, "time": time_str})
    save_reminders(reminders)
    speak(f"Reminder added for {time_str}: {note}")

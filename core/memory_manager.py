# File: core/memory_manager.py
import json
import os
from datetime import datetime
from core.tts_output import speak

MEMORY_FILE = "config/memory.json"

# Load memory

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'w') as f:
            json.dump([], f)
    with open(MEMORY_FILE, 'r') as f:
        return json.load(f)

# Save memory

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=4)

# Add memory entry

def add_memory(note):
    memory = load_memory()
    entry = {
        "note": note,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    memory.append(entry)
    save_memory(memory)
    speak("Memory saved.")

# Retrieve recent memories

def list_memories(limit=5):
    memory = load_memory()
    latest = memory[-limit:]
    for entry in latest:
        speak(f"On {entry['timestamp']}, you saved: {entry['note']}")

# File: interfaces/android_api.py
from flask import Flask, request, jsonify
from core.nlp_engine import process_command
from scheduler.reminders import add_reminder
from core.memory_manager import add_memory, list_memories

app = Flask(__name__)

@app.route("/command", methods=["POST"])
def handle_command():
    data = request.json
    command = data.get("command")
    if not command:
        return jsonify({"error": "No command received"}), 400
    process_command(command)
    return jsonify({"status": "Processed"})

@app.route("/add_reminder", methods=["POST"])
def handle_add_reminder():
    data = request.json
    note = data.get("note")
    time_str = data.get("time")
    if not note or not time_str:
        return jsonify({"error": "Missing note or time"}), 400
    add_reminder(note, time_str)
    return jsonify({"status": "Reminder added"})

@app.route("/add_memory", methods=["POST"])
def handle_add_memory():
    data = request.json
    note = data.get("note")
    if not note:
        return jsonify({"error": "Missing note"}), 400
    add_memory(note)
    return jsonify({"status": "Memory added"})

@app.route("/get_memories", methods=["GET"])
def handle_get_memories():
    from core.memory_manager import load_memory
    memory = load_memory()
    return jsonify(memory)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
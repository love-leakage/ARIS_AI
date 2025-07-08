# File: server/api.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, render_template, jsonify, request
from core.memory_manager import load_memory
from scheduler.reminders import load_reminders, add_reminder
import datetime

app = Flask(__name__, template_folder=".")

@app.route("/")
def dashboard():
    memories = load_memory()[-5:]
    reminders = load_reminders()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return render_template("dashboard.html", memories=memories, reminders=reminders, now=now)

@app.route("/add_reminder", methods=["POST"])
def web_add_reminder():
    note = request.form.get("note")
    time = request.form.get("time")
    add_reminder(note, time)
    return jsonify({"status": "Reminder added"})

if __name__ == "__main__":
    app.run(port=5002)

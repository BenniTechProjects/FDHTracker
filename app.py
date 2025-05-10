from flask import Flask, render_template
import csv
import os
import sys
import webbrowser

app = Flask(__name__)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp dir
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

LOG_DIR = resource_path("results")
LOG_FILE = os.path.join(LOG_DIR, "health_log.csv")

def read_latest_status():
    status_map = {}

    # Ensure folder exists
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Ensure file exists with header
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
            f.write("Timestamp,DeviceName,IP,Type,Location,Status,Latency_ms\n")
        return []

    with open(LOG_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            status_map[row['DeviceName']] = row
    return list(status_map.values())

@app.route("/")
def dashboard():
    devices = read_latest_status()
    return render_template("dashboard.html", devices=devices)

if __name__ == "__main__":
    webbrowser.open("http://localhost:5000")
    app.run(debug=False, port=5000)
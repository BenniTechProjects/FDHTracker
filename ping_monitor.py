import csv
import time
import os
from ping3 import ping
from datetime import datetime

DEVICES_FILE = "devices.csv"
LOG_FILE = "results/health_log.csv"

def load_devices(file_path):
    devices = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            devices.append(row)
    return devices

def check_device(ip):
    try:
        latency = ping(ip, timeout=1)
        if latency is None:
            return ("Offline", None)
        return ("Online", round(latency * 1000, 2))  # ms
    except Exception:
        return ("Error", None)


def write_log(entries):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, 'a', newline='') as logfile:
        writer = csv.writer(logfile)
        if not file_exists:
            writer.writerow(["Timestamp", "DeviceName", "IP", "Type", "Location", "Status", "Latency_ms"])
        for entry in entries:
            writer.writerow(entry)

def run_health_check():
    devices = load_devices(DEVICES_FILE)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entries = []

    print(f"\n[{timestamp}] Device Health Check\n")
    for device in devices:
        status, latency = check_device(device['IP'])
        line = f"{device['DeviceName']:10} | {device['IP']:15} | {status:7}"
        if latency is not None:
            line += f" | {latency:6} ms"
        else:
            line += " |    ---"
        print(line)

        log_entries.append([
            timestamp,
            device['DeviceName'],
            device['IP'],
            device['Type'],
            device['Location'],
            status,
            latency if latency is not None else ''
        ])

    write_log(log_entries)

if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    while True:
        run_health_check()
        time.sleep(60)  # Run every 60 seconds

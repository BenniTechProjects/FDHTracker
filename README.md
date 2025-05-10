# Field Device Health Ping Tracker

Monitors hospital mobile carts and label printers via ping, logs health, and serves a live web dashboard.

## Features
- Real-time ping checks
- Health status color-coded
- Filter/search by status, name, date
- Export filtered results to CSV
- One-click `.exe` packaging with PyInstaller

## Setup

```bash
pip install -r requirements.txt
python ping_monitor.py  # Background logging
python app.py           # View dashboard at http://localhost:5000

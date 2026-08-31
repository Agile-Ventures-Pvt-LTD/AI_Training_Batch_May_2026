# -*- coding: utf-8 -*-
import os
import time
import subprocess
import sys

# Force UTF-8 stdout encoding on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CSV_FILE = os.path.join("data", "daily_executive_metrics.csv")
BUILD_SCRIPT = "build_executive_hub.py"

print("==================================================")
print("Sleepsia Live CSV Watcher & Auto-Sync Engine")
print(f"Watching '{CSV_FILE}' for live updates...")
print("==================================================")

last_mtime = 0
if os.path.exists(CSV_FILE):
    last_mtime = os.path.getmtime(CSV_FILE)

while True:
    try:
        if os.path.exists(CSV_FILE):
            current_mtime = os.path.getmtime(CSV_FILE)
            if current_mtime != last_mtime:
                last_mtime = current_mtime
                print(f"\n[DETECTED CSV CHANGE] Rebuilding index.html & dashboard.html...")
                subprocess.run([sys.executable, BUILD_SCRIPT], check=True)
                print("SUCCESS: Live sync complete! Refresh index.html in your browser.")
        time.sleep(1)
    except KeyboardInterrupt:
        print("\nWatcher stopped.")
        break
    except Exception as e:
        print("Watcher error:", e)
        time.sleep(1)

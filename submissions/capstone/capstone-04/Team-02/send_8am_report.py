import urllib.request
import datetime
import json
import os

# ========================================================
# 8:00 AM DAILY SCHEDULED UNIVERSAL REPORT DISPATCH
# Reads email_config.json & sends to configured recipient(s)
# ========================================================

CONFIG_FILE = r"c:\Users\Taniya Gupta\Desktop\report\email_config.json"

def trigger_8am_direct_report():
    print(f"[{datetime.datetime.now()}] 8:00 AM Scheduled Task Fired -> Requesting universal email dispatch...")
    url = "http://localhost:5000/send-report"
    try:
        req = urllib.request.Request(url, data=b"{}", headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            print("Universal Report Successfully Dispatched!", res_data)
    except Exception as e:
        print(f"Universal dispatch standby ping: {e}")

if __name__ == "__main__":
    trigger_8am_direct_report()

import json
from datetime import datetime

from config import LOG_FILE

def log_query(payload):
    with open(LOG_FILE,"a",encoding="utf-8") as f:
       f.write(json.dumps(payload)+ "\n")


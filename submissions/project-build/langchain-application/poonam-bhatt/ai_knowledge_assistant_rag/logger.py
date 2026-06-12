import json
from datetime import datetime

#For query log creation...

def log_query(
    query,
    answer,
    sources
):

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "response": answer,
        "sources": sources
    }

    with open(
        "logs/query_logs.json",
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(log_entry)
            + "\n"
        )

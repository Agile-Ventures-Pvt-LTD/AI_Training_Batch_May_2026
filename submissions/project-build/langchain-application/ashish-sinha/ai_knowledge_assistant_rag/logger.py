import json
import os
from datetime import datetime

from config import LOG_FILE


def log_query(question, query_type,retrieved_sources,answer,answerability,confidence):

    os.makedirs(os.path.dirname(LOG_FILE),exist_ok=True)

    log_record = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "query_type": query_type,
        "retrieved_sources": retrieved_sources,
        "answer": answer,
        "answerability": answerability,
        "confidence": confidence
    }

    with open(LOG_FILE,"a",encoding="utf-8") as f:

        f.write( json.dumps(log_record)+ "\n")
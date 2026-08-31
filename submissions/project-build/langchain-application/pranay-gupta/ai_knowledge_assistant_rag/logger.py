import json
import os

from datetime import datetime

from config import LOG_PATH


def log_query(question, query_type, retrieved_sources, answer, confidence, answerability):

    os.makedirs(
        os.path.dirname(LOG_PATH),
        exist_ok=True
    )

    log_record = {

        "timestamp":
        datetime.utcnow().isoformat(),

        "question": question,

        "query_type": query_type,

        "retrieved_sources": retrieved_sources,

        "answer": answer,

        "confidence": confidence,

        "answerability": answerability
    }

    with open(LOG_PATH,"a",encoding="utf-8") as file:

        file.write(json.dumps(log_record,ensure_ascii=False)+ "\n")
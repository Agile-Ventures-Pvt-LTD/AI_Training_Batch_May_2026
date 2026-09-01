import json
import os
from datetime import datetime

class QueryLogger:
    def __init__(self, log_file):
        self.log_file=log_file
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def log_query(self, question, classification, answer, retrieved_sources):
        log_entry={
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "query_type": classification.get("query_type"),
            "retrieved_sources": retrieved_sources,
            "answer": answer.get("answer"),
            "answerability": answer.get("answerability"),
            "confidence": answer.get("confidence")
        }

        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry)+"\n")
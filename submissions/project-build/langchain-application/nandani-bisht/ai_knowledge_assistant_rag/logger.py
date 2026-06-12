import json
from datetime import datetime
from config import settings


LOG_FILE = (
    settings.LOG_DIR
    / "query_logs.jsonl"
)


def save_log(data):

    record = {
        "timestamp": str(
            datetime.now()
        ),
        **data
    }

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(
                record,
                ensure_ascii=False
            )
            + "\n"
        )
import json
from pathlib import Path


def append_to_json_log(
    record: dict,
    filepath: str
):
    '''general logger utility'''
    path = Path(filepath)

    if path.exists():

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

    else:
        data = []

    data.append(record)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )
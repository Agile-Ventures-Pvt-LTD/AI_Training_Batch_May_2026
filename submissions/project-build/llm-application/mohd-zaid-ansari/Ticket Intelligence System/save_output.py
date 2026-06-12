import json
from pathlib import Path

def save_output(
    data,
    filename="sample_blog_output.json"
):

    Path("outputs").mkdir(
        exist_ok=True
    )

    filepath = f"outputs/{filename}"

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

    return filepath
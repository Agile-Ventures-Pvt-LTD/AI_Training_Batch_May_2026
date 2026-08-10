from pathlib import Path
from datetime import datetime


OUTPUT_FOLDER = Path("outputs")

OUTPUT_FOLDER.mkdir(
    exist_ok=True
)


def save_output(
    query: str,
    response: str
):
    """
    Save every run.
    """

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    file_path = (
        OUTPUT_FOLDER /
        f"run_{timestamp}.md"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            f"# User Query\n\n{query}\n\n"
        )

        file.write(
            f"# Agent Response\n\n{response}"
        )

    return str(file_path)
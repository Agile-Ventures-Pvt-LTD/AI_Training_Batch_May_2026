from datetime import datetime


LOG_FILE = "logs/query_logs.txt"


def log_query(
    sql_query: str,
    result: str
):

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write("\n")
        file.write("=" * 100)
        file.write("\n")

        file.write(
            f"Timestamp: {datetime.now()}\n\n"
        )

        file.write(
            f"SQL Query:\n{sql_query}\n\n"
        )

        file.write(
            f"Result:\n{result}\n"
        )

        file.write("\n")
        file.write("=" * 100)
        file.write("\n")
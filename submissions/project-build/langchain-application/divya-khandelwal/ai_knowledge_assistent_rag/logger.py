import json
from datetime import datetime


def save_log(query, documents, response):

    sources = []

    for doc in documents:
        sources.append(
            {
                "file_name": doc.metadata.get("file_name"),
                "page_number": doc.metadata.get("page_number"),
                "chunk_id": doc.metadata.get("chunk_id")
            }
        )


    log = {
        "timestamp": str(datetime.now()),
        "query": query,
        "sources": sources,
        "answer": response
    }


    with open(
        "outputs/benchmark_result.json",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(log, indent=4)
        )

        file.write("\n")


    print("Log saved")
from chain import answer_question
from logger import log_query

while True:

    question = input(
        "\nAsk Question (type exit to quit): "
    )

    result = answer_question(question)

    print("\nANSWER")
    print(result["answer"])

    print("\nCONFIDENCE")
    print(result["confidence"])

    print("\nANSWERABILITY")
    print(result["answerability"])

    print("\nSOURCES")

    for source in result["sources"]:

        print(
            f"""
File: {source['source_file']}
Page: {source['page_number']}
Chunk: {source['chunk_id']}
Snippet: {source['snippet']}
"""
        )

    print("\nDEBUG VIEW")

    for chunk in result["retrieved_chunks"]:

        print(chunk)

    log_query(result)


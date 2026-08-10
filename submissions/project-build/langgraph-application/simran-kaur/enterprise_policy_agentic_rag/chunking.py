from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from loaders import load_documents

documents=load_documents()


def split_documents():

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=120
    )

    chunks = splitter.split_documents(documents)

# for idx, chunk in enumerate(chunks):

#     chunk.metadata["chunk_id"] = f"chunk_{idx}"

    for idx, chunk in enumerate(chunks):

            policy = chunk.metadata["policy_domain"]

            chunk.metadata = {
                "chunk_id": f"{policy.lower().replace(' ', '_')}_{idx}",
                "source_file": chunk.metadata["source_file"],
                "policy_domain": policy,
                "text": chunk.page_content
            }

    return chunks



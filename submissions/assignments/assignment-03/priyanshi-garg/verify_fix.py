from langchain_core.documents import Document

docs = [Document(page_content="alpha"), Document(page_content="beta")]
chunk_batches = [docs[:1], docs[1:]]
ok = []
for batch_num, batch in enumerate(chunk_batches, start=1):
    batch_text = "\\n\\n".join([f"Chunk {idx}: {chunk.page_content}" for idx, chunk in enumerate(batch, start=1)])
    ok.append((batch_num, len(batch), batch_text))
print("verified", ok)

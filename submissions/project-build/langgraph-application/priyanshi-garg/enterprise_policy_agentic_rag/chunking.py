from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain.schema import Document
from loaders import markdown_files

header_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "H1"), ("##", "H2")]
)

fallback_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

chunks = []

for file_name, text in markdown_files:
    sections = header_splitter.split_text(text)

    for section in sections:
        small_chunks = fallback_splitter.split_text(section.page_content)

        for index, ch in enumerate(small_chunks):
            chunks.append(
                Document(
                    page_content=ch,
                    metadata={"file": file_name, "chunk": index}
                )
            )

print("Chunks created:", len(chunks))
print(chunks[0].page_content)
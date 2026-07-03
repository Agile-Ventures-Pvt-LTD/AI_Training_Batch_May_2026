from typing import List, Union
from pdf_load import data

def recursive_character_splitter(data: Union[str, List[str]],
    chunk_size: int = 200,chunk_overlap: int = 20,
    separators: List[str] = None) -> List[str]:

    if separators is None:
        separators = ["\n", " ", ""] 

    if isinstance(data, list):
        chunks = []
        for item in data:
            chunks.extend(recursive_character_splitter(item, chunk_size, chunk_overlap, separators))
        return chunks

    text = data.strip()
    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    for sep in separators:
        if sep and sep in text:
            parts = text.split(sep)
        else:
            parts = list(text) 

        chunks = []
        current_chunk = ""

        for part in parts:
            candidate = (current_chunk + sep + part) if current_chunk else part

            if len(candidate) <= chunk_size:
                current_chunk = candidate
            else:
                if current_chunk:
                    chunks.append(current_chunk)

                if len(part) > chunk_size:
                    chunks.extend(
                        recursive_character_splitter(
                            part, chunk_size, chunk_overlap, separators[separators.index(sep)+1:]
                        )
                    )
                    current_chunk = ""
                else:
                    current_chunk = part

        if current_chunk:
            chunks.append(current_chunk)

        if chunk_overlap > 0 and len(chunks) > 1:
            overlapped_chunks = []
            for i, chunk in enumerate(chunks):
                if i == 0:
                    overlapped_chunks.append(chunk)
                else:
                    prev_chunk = overlapped_chunks[-1]
                    overlap_text = prev_chunk[-chunk_overlap:]
                    overlapped_chunks.append(overlap_text + chunk)
            chunks = overlapped_chunks

        return chunks

    return [text]  

if __name__ == "__main__":
    chunks = recursive_character_splitter(data, chunk_size=80, chunk_overlap=10)
    for i, c in enumerate(chunks, 1):
        print(f"Chunk {i}: {repr(c)}")
        
print(len(chunks))
print(chunks)

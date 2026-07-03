from langchain_pymupdf4llm import PyMuPDF4LLMLoader

def load_file(file_path):
    try:
        loader = PyMuPDF4LLMLoader(file_path=file_path, pages_delimiter="\n\f")
        return loader.load()
    except Exception as e:
        print(f"Error: {e}")
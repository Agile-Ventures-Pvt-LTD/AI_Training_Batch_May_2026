from langchain.document_loaders import UnstructuredMarkdownLoader

def load_markdown(path: str):
    """Load Markdown documents with strict error handling."""
    try:
        loader = UnstructuredMarkdownLoader(path)
        docs = loader.load()
        if not docs:
            raise ValueError("No content extracted from markdown file.")
        return docs
    except ModuleNotFoundError as e:
        raise RuntimeError(
            f"Markdown loader requires the 'unstructured' package. "
            f"Install with: `pip install unstructured`. Original error: {e}"
        )
    except Exception as e:
        raise RuntimeError(f"Markdown loading failed for {path}: {e}")

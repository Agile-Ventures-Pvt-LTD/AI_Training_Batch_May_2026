from langchain.document_loaders import UnstructuredHTMLLoader

def load_html(path: str):
    """Load HTML documents with strict error handling."""
    try:
        loader = UnstructuredHTMLLoader(path)
        docs = loader.load()
        if not docs:
            raise ValueError("No content extracted from HTML file.")
        return docs
    except ModuleNotFoundError as e:
        raise RuntimeError(
            f"HTML loader requires the 'unstructured' package. "
            f"Install with: pip install 'unstructured[html]'. Original error: {e}"
        )
    except Exception as e:
        raise RuntimeError(f"HTML loading failed for {path}: {e}")
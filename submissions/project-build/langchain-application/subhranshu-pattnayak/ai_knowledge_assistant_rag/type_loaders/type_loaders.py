import os
from .PdfLoader import load_pdf
from .TextLoader import load_text
from .MarkdownLoader import load_markdown
from .HTMLLoader import load_html

def load_documents(file_paths):
    """Load documents of multiple types into LangChain format."""
    loader_map = {
        ".pdf": load_pdf,
        ".txt": load_text,
        ".md": load_markdown,
        ".html": load_html,
        ".htm": load_html,
    }

    documents = []
    errors = []

    for path in file_paths:
        if not os.path.exists(path):
            errors.append(f"File not found: {path}")
            continue

        extension = os.path.splitext(path)[1].lower()
        loader_fn = loader_map.get(extension)

        if not loader_fn:
            errors.append(f"Unsupported file type: {path}")
            continue

        try:
            docs = loader_fn(path)
            documents.extend(docs)
        except Exception as e:
            errors.append(str(e))

    if not documents:
        errors.append("No documents loaded. Please check file paths and formats.")

    # Report errors clearly
    if errors:
        print("Loader Errors:")
        for err in errors:
            print(f" - {err}")

    return documents

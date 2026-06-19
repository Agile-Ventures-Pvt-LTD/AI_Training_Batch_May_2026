from langchain_community.document_loaders import TextLoader

def load_file(file_path):
    try:
        loader = TextLoader(file_path)
        return loader.load()
    except Exception as e:
        print(f"Error: {e}")
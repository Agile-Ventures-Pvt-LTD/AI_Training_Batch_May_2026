from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader

load_dotenv()


def load_data():
    base_path = Path(__file__).resolve().parent
    data_path = base_path / "data" / "policies"

    if not data_path.exists():
        raise FileNotFoundError(f"Data folder not found: {data_path}")

    loader = DirectoryLoader(
        str(data_path),
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )

    documents = loader.load()
    print("Number of pages loaded:", len(documents))
    return documents


if __name__ == "__main__":
    load_data()
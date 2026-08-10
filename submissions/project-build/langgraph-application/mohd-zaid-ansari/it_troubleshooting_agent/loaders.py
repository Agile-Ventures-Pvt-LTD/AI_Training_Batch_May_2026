import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from config import KB_PATH


def load_raw_documents(KB_PATH=KB_PATH):
    loader = DirectoryLoader(KB_PATH, glob="**/*.md", loader_cls=TextLoader)
    return loader.load()


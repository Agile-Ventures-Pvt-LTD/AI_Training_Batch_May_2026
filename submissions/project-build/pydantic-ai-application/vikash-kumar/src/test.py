from config import HF_TOKEN
from pydantic_ai import Embedder
embedder = Embedder('sentence-transformers:google/embeddinggemma-300m')


async def main():
    result = await embedder.embed_query('Hello world')
    print(result)
    #> 768
    await main()

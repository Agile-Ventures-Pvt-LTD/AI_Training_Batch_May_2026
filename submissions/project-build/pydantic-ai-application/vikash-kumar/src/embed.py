from dotenv import load_dotenv
load_dotenv()
import os
os.environ['HF_TOKEN'] = os.getenv('HF_TOKEN')
from pydantic_ai import Agent
from pydantic_ai import Agent
from pydantic_ai.capabilities import Capability

from pydantic_ai import Embedder

# Model is downloaded from Hugging Face on first use
embedder = Embedder('sentence-transformers:google/embeddinggemma-300m')

from pydantic_ai import Embedder

# Model is downloaded from Hugging Face on first use
embedder = Embedder('sentence-transformers:lightonai/DenseOn')


async def main():
    result = await embedder.embed_query('Hello world')
    print(result)
    #> 768
    await main()
    
async def main():
    result = await embedder.embed_query('Hello world')
    return result
    #> 768

    await main()
from config import Config

def retrieving_chunks(db, query: str):
    """Fetch top K chunks for the query."""
    if db is None:
        return []
    similar = db.similarity_search(
        query,
        k=Config.TOP_K
        )
    return similar
import sqlite3
import chromadb
from config import DB_PATH, KB_PATH

class DatabaseManager:
    def __init__(self):
        self.sql_db_path = DB_PATH
        self.chroma_client = chromadb.PersistentClient(path=KB_PATH)

    def get_sql_connection(self):
        conn = sqlite3.connect(self.sql_db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def execute_sql_query(self, query, params=()):
        conn = self.get_sql_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def query_knowledge_base(self, collection_name, query_text, n_results=3):
        collection = self.chroma_client.get_collection(name=collection_name)
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results
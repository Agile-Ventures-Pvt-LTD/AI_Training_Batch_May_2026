import sqlite3
import pandas as pd
from config import DB_PATH

def run(query, params):
    """Function to run sql query"""
    try:
        conn=sqlite3.connect(DB_PATH)
        df=pd.read_sql_query(query,conn,params=params)
        conn.close()
        return df
    except Exception as e:
        return {"error": str(e)}
    
from db_utils.db_connection import get_conn
from langchain_core.prompts import ChatPromptTemplate
from utils.gClient import get_client
from utils.paths import service_names
import sqlite3
from langchain.tools import tool

@tool
def get_known_incident_tool(query):
    try:
        incident_system_message = f"""
            You are an expert query classifier. Analyze the customer query and classify it into one of the following categories:
            {service_names}
            Respond ONLY with the classification type.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", incident_system_message),
            ("human", "Customer Query: {query}")
        ])
        
        llm = get_client()
        
        classifier_chain = prompt | llm
        
        classification_result: str = classifier_chain.invoke({"query": query})
        
        conn=get_conn()
        conn.row_factory=sqlite3.Row
        cursor=conn.cursor()

        if classification_result.content:
            query = "SELECT * FROM known_incidents WHERE service_name=?"
            params = [classification_result.content]
        else:
            conn.close()
            return None

        cursor.execute(query,params)
        row = cursor.fetchall()
        conn.close()
        return row
    
    except Exception as e:
        print(F"Error: {e}")
        return None
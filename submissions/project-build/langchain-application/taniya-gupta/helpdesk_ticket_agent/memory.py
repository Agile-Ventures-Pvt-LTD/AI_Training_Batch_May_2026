import json

class Memory:
    def __init__(self, db):
        self.db=db

    def save_conversation(self, session_id, user_message, agent_response, tools_used):
        query="""
        INSERT INTO conversation_logs (session_id, user_message, agent_response, tools_used) 
        VALUES (?,?,?,?) """
        params = (session_id, user_message, agent_response, json.dumps(tools_used))
        self.db.execute_update(query,params)

    def recall_conversation(self, keyword):
        query="SELECT * from conversation_logs WHERE user_message LIKE ? OR agent_response LIKE ? ORDER by created_at DESC"
        params=(f"%{keyword}%", f"%{keyword}%")
        return self.db.execute_query(query, params)

    def save_archival_memory(self, key, value, mem_type="preference", importance=3):
        query = """
        INSERT INTO archival_memory (memory_key, memory_value, memory_type, importance)
        VALUES (?, ?, ?, ?)
        """
        params = (key, value, mem_type, importance)
        self.db.execute_update(query, params)

    def recall_archival_memory(self, keyword):
        query = "SELECT * FROM archival_memory WHERE memory_key LIKE ? OR memory_value LIKE ? ORDER BY importance DESC"
        params = (f"%{keyword}%", f"%{keyword}%")
        return self.db.execute_query(query, params)
    
    def save_summary(self, session_id, summary, key_decisions, open_items):
        query = """
        INSERT INTO conversation_summaries (session_id, summary, key_decisions, open_items)
        VALUES (?, ?, ?, ?)
        """
        params = (session_id, summary, json.dumps(key_decisions), json.dumps(open_items))
        self.db.execute_update(query, params)
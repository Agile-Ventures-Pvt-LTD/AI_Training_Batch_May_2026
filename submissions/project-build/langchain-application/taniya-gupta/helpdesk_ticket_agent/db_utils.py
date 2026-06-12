import sqlite3

class DB:
    def __init__(self, db_path):
        self.db_path=db_path
    
    def get_connection(self):
        conn=sqlite3.connect(self.db_path)
        conn.row_factory=sqlite3.Row
        return conn
    
    def execute_query(self, query, params=()):
        with self.get_connection() as conn:
            cursor=conn.cursor()
            cursor.execute(query, params)
            rows=cursor.fetchall()
            return [dict(row) for row in rows]
        

    def execute_update(self, query, params=()):
        with self.get_connection() as conn:
            cursor=conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
    
    def get_ticket_by_id(self,ticket_id):
        query="SELECT * from tickets WHERE ticket_id=?"
        results=self.execute_query(query,(ticket_id,))
        return results[0] if results else None
    
    def get_open_tickets(self):
        query="SELECT * from open_tickets"
        return self.execute_query(query)
    
    def search_tickets(self, filters, limit=5):
        columns="ticket_id, subject, priority, status, customer_tier, category, due_at"
        query=f"SELECT {columns} from tickets WHERE 1=1"
        params=[]
        if 'status' in filters and filters['status']:
            query += " AND status = ?"
            params.append(filters['status'])
        if 'priority' in filters and filters['priority']:
            query += " AND priority = ?"
            params.append(filters['priority'])
        if 'customer_tier' in filters and filters['customer_tier']:
            query += " AND customer_tier = ?"
            params.append(filters['customer_tier'])
        if 'category' in filters and filters['category']:
            query += " AND category = ?"
            params.append(filters['category'])

        final_limit=min(int(limit),5)
        query+=" LIMIT ?"
        params.append(final_limit)

        return self.execute_query(query, tuple(params))
import sqlite3
import config

def connection():
    return sqlite3.connect(config.DB_PATH)

def user_profile(user_id,full_name,email):
    conn=connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()

    if user_id:
        query="select * from users where user_id=?"
        params=[user_id]
    elif email:
        query="select * from users where email=?"
        params=[email]
    elif full_name:
        query="select * from users where full_name LIKE ?"
        params=[f"%{full_name}%"]
    else:
        conn.close()
        return None
    cursor.execute(query,params)
    row=cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def device_status(user_id=None,device_id=None):
    conn=connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()

    if user_id:
        query="select * from devices where user_id=?"
        params=[user_id]
    elif device_id:
        query="select * from devices where device_id=?"
        params=[device_id]
    else:
        conn.close()
        return None
    cursor.execute(query,params)
    row=cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def known_incidents(service_name=None, region=None, status="Active"):
    conn = connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = "SELECT * FROM known_incidents WHERE status = ?"
    params = [status]
    
    if service_name:
        query += " AND LOWER(service_name) LIKE LOWER(?)"
        params.append(f"%{service_name}%")
    if region:
        query += " AND LOWER(region) = LOWER(?)"
        params.append(region)     
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def diagnostic_snapshot(user_id=None, device_id=None):
    conn = connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if user_id and device_id:
        query = "SELECT * FROM diagnostic_snapshots WHERE user_id = ? AND device_id = ? ORDER BY created_at DESC LIMIT 1"
        params = [user_id, device_id]
    elif user_id:
        query = "SELECT * FROM diagnostic_snapshots WHERE user_id = ? ORDER BY created_at DESC LIMIT 1"
        params = [user_id]
    elif device_id:
        query = "SELECT * FROM diagnostic_snapshots WHERE device_id = ? ORDER BY created_at DESC LIMIT 1"
        params = [device_id]
    else:
        conn.close()
        return None
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    res = dict(row)
    keys = ['vpn_reachable', 'internet_reachable', 'webmail_reachable', 'internal_apps_reachable', 'account_locked', 'mfa_push_success']
    for k in keys:
        if res.get(k) is not None:
            res[k] = bool(res[k])
    return res

def ticket_details(ticket_id=None, user_id=None):
    conn = connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if ticket_id:
        query = "SELECT * FROM tickets WHERE ticket_id = ?"
        params = [ticket_id]
    elif user_id:
        query = "SELECT * FROM tickets WHERE user_id = ? ORDER BY created_at DESC LIMIT 1"
        params = [user_id]
    else:
        conn.close()
        return None
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None

def search_tickets(query_term):
    conn = connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE subject LIKE ? OR description LIKE ?", (f"%{query_term}%", f"%{query_term}%"))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
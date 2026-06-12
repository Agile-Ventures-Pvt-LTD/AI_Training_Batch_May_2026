import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv


Row = dict


def get_db_path(db_path=None):
    load_dotenv()
    path = db_path or os.getenv("DB_PATH") or "data/helpdesk_agent_db/helpdesk_agent.db"
    path = Path(path)

    if not path.is_absolute():
        path = Path(__file__).parent / path

    if not path.exists():
        raise FileNotFoundError(f"Database not found: {path}")

    return path


def connect(db_path=None):
    conn = sqlite3.connect(get_db_path(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all(sql, params=(), db_path=None):
    with connect(db_path) as conn:
        rows = conn.execute(sql, params).fetchall()
        return [dict(row) for row in rows]


def fetch_one(sql, params=(), db_path=None):
    rows = fetch_all(sql, params, db_path)
    if rows:
        return rows[0]
    return None


def count_tickets_by_status(db_path=None):
    return fetch_all(
        """
        SELECT status, COUNT(*) AS total
        FROM tickets
        GROUP BY status
        ORDER BY total DESC
        """,
        db_path=db_path,
    )


def search_tickets(keyword=None, status=None, priority=None, limit=20, db_path=None):
    where = []
    params = []

    if keyword:
        where.append("(subject LIKE ? OR description LIKE ? OR customer_name LIKE ?)")
        keyword = f"%{keyword}%"
        params += [keyword, keyword, keyword]

    if status:
        where.append("status = ?")
        params.append(status)

    if priority:
        where.append("priority = ?")
        params.append(priority)

    where_sql = ""
    if where:
        where_sql = "WHERE " + " AND ".join(where)

    params.append(limit)

    return fetch_all(
        f"""
        SELECT ticket_id, customer_name, customer_tier, category, priority,
               status, assigned_to, subject, description, due_at
        FROM tickets
        {where_sql}
        ORDER BY due_at ASC
        LIMIT ?
        """,
        params,
        db_path,
    )


def get_ticket_details(ticket_id, db_path=None):
    return fetch_one(
        "SELECT * FROM tickets WHERE ticket_id = ?",
        (ticket_id,),
        db_path,
    )


def get_ticket_comments(ticket_id, db_path=None):
    return fetch_all(
        """
        SELECT comment_id, author, comment_type, comment, created_at
        FROM ticket_comments
        WHERE ticket_id = ?
        ORDER BY created_at ASC
        """,
        (ticket_id,),
        db_path,
    )


def get_overdue_tickets(limit=20, db_path=None):
    return fetch_all(
        """
        SELECT ticket_id, customer_name, customer_tier, category, priority,
               status, assigned_to, subject, due_at, sla_status
        FROM overdue_tickets
        ORDER BY due_at ASC
        LIMIT ?
        """,
        (limit,),
        db_path,
    )


def get_work_queue(limit=20, db_path=None):
    return fetch_all(
        """
        SELECT ticket_id, customer_name, customer_tier, category, priority,
               status, subject, sla_status, priority_score
        FROM ticket_work_queue
        ORDER BY priority_score DESC, due_at ASC
        LIMIT ?
        """,
        (limit,),
        db_path,
    )


def update_ticket_status(ticket_id, status, db_path=None):
    with connect(db_path) as conn:
        cursor = conn.execute(
            """
            UPDATE tickets
            SET status = ?, last_updated_at = CURRENT_TIMESTAMP
            WHERE ticket_id = ?
            """,
            (status, ticket_id),
        )
        conn.commit()
        return cursor.rowcount > 0

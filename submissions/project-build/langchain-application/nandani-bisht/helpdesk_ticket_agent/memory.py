from datetime import datetime
from db_utils import db


class MemoryManager:
    """
    SQLite backed memory manager.
    """

    def save_conversation(
        self,
        session_id,
        user_message,
        agent_response,
        tools_used=""
    ):

        db.execute(
            """
            INSERT INTO conversation_logs
            (
                session_id,
                user_message,
                agent_response,
                tools_used,
                created_at
            )
            VALUES
            (?, ?, ?, ?, ?)
            """,
            (
                session_id,
                user_message,
                agent_response,
                tools_used,
                datetime.now().isoformat()
            )
        )

        return {
            "stored": True
        }

    def recall_conversation(
        self,
        keyword=None,
        session_id=None,
        limit=10
    ):

        query = """
        SELECT *
        FROM conversation_logs
        WHERE 1=1
        """

        params = []

        if keyword:

            query += """
            AND
            (
                user_message LIKE ?
                OR
                agent_response LIKE ?
            )
            """

            params.extend(
                [
                    f"%{keyword}%",
                    f"%{keyword}%"
                ]
            )

        if session_id:

            query += """
            AND session_id=?
            """

            params.append(
                session_id
            )

        query += """
        ORDER BY created_at DESC
        LIMIT ?
        """

        params.append(
            limit
        )

        return db.fetch_all(
            query,
            tuple(params)
        )

    def save_archival_memory(
        self,
        memory_key,
        memory_value,
        memory_type="preference",
        importance=5
    ):

        db.execute(
            """
            INSERT INTO archival_memory
            (
                memory_key,
                memory_value,
                memory_type,
                importance
            )
            VALUES
            (?, ?, ?, ?)
            """,
            (
                memory_key,
                memory_value,
                memory_type,
                importance
            )
        )

        return {
            "stored": True
        }

    def recall_archival_memory(
        self,
        keyword
    ):

        return db.fetch_all(
            """
            SELECT *
            FROM archival_memory
            WHERE
            memory_key LIKE ?
            OR
            memory_value LIKE ?
            ORDER BY importance DESC
            """,
            (
                f"%{keyword}%",
                f"%{keyword}%"
            )
        )

    def summarize_conversation(
        self,
        session_id,
        summary,
        key_decisions="",
        open_items=""
    ):

        db.execute(
            """
            INSERT INTO
            conversation_summaries
            (
                session_id,
                summary,
                key_decisions,
                open_items
            )
            VALUES
            (?, ?, ?, ?)
            """,
            (
                session_id,
                summary,
                key_decisions,
                open_items
            )
        )

        return {
            "stored": True,
            "summary": summary
        }


memory = MemoryManager()

import sqlite3
from contextlib import contextmanager
from config import DB_PATH
class DatabaseError(Exception):
    pass


class HelpdeskDB:

    def __init__(self):

        self.db_path = str(DB_PATH)

    @contextmanager
    def connect(self):

        connection = None

        try:

            connection = sqlite3.connect(
                self.db_path
            )

            connection.row_factory = (
                sqlite3.Row
            )

            yield connection

            connection.commit()

        except Exception as exc:

            if connection:
                connection.rollback()

            raise DatabaseError(
                str(exc)
            )

        finally:

            if connection:
                connection.close()

    def fetch_all(
        self,
        query,
        params=()
    ):

        with self.connect() as conn:

            rows = conn.execute(
                query,
                params
            ).fetchall()

            return [
                dict(r)
                for r in rows
            ]

    def fetch_one(
        self,
        query,
        params=()
    ):

        with self.connect() as conn:

            row = conn.execute(
                query,
                params
            ).fetchone()

            if row:
                return dict(row)

            return None

    def fetch_scalar(
        self,
        query,
        params=()
    ):

        row = self.fetch_one(
            query,
            params
        )

        if not row:
            return None

        return next(
            iter(row.values())
        )

    def execute(
        self,
        query,
        params=()
    ):

        with self.connect() as conn:

            cursor = conn.execute(
                query,
                params
            )

            return {
                "rows_affected":
                cursor.rowcount
            }

    def exists(
        self,
        table,
        field,
        value
    ):

        query = f"""
        SELECT 1
        FROM {table}
        WHERE {field}=?
        LIMIT 1
        """

        row = self.fetch_one(
            query,
            (value,)
        )

        return bool(row)


db = HelpdeskDB()
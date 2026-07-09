import sqlite3
from pathlib import Path
from typing import Optional, Union, List
from src.config import TICKET_DB
from fastmcp import FastMCP
from src.mcp_logger import log_tool

mcp = FastMCP("support-ticket")

def get_connection(db_path: Path) -> sqlite3.Connection:
    """
    Create and return a SQLite connection.
    """

    if not db_path.exists():
        raise FileNotFoundError(f"{db_path} not found.")

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row

    return connection


class TicketService:
    """
    Business logic for Support Ticket operations.
    """

    def __init__(self) -> None:
        self.db_path = TICKET_DB

    def search_tickets(
        self,
        service_name: Optional[Union[str,List[str]]] = None,
        priority: str | None = None,
        status: str | None = None,
    ) -> list[dict]:
        """
        Search tickets using optional filters.
        """

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM tickets WHERE 1=1"
        params = []
        

        if service_name:

            if isinstance(service_name,list):
                placeholder = ",".join(["?"]*len(service_name))
                query += (f" AND service_name IN ({placeholder})")
                params.extend(service_name)

            else:
                query += " AND service_name = ?"
                params.append(service_name)

        if status:
            query += " AND status = ?"
            params.append(status)

        cursor.execute(query, params)

        rows = cursor.fetchall()

        conn.close()

        result = [dict(row) for row in rows]

        log_tool(
            "support_ticket",
            "search_ticket",
            result
        )

        return result

        

    def get_ticket_details(self, ticket_id: str) -> dict:
        """
        Return details for a ticket.
        """

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM tickets WHERE ticket_id = ?",
            (ticket_id,),
        )

        row = cursor.fetchone()

        conn.close()

        if row is None:
            return {
                "found": False,
                "message": f"{ticket_id} not found.",
            }

        result = {
            "found": True,
            **dict(row),
        }

        log_tool(
            "support_ticket",
            "get_ticket_details",
            result
        )

        return result

    def get_high_priority_tickets(self,service_name : Optional[Union[str,List[str]]] = None) -> dict:
        """
        Return OPEN P1/P2 tickets.
        """

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM tickets
            WHERE status='OPEN'
            AND priority IN ('P1','P2')
            """
        )

        rows = cursor.fetchall()

        conn.close()

        result = [dict(row) for row in rows]

        log_tool(
            "support_ticket",
            "get_high_priority_tickets",
            result
        )

        return result
    

service = TicketService()


@mcp.tool
def search_tickets(
    service_name: str | None = None,
    status: str | None = None,
) -> list[dict]:
    """
    Search support tickets.
    """
    return service.search_tickets(
        service_name=service_name,
        status=status,
    )


@mcp.tool
def get_ticket_details(ticket_id: str) -> dict:
    """
    Get ticket details.
    """
    return service.get_ticket_details(ticket_id)


@mcp.tool
def get_high_priority_tickets() -> list[dict]:
    """
    Return OPEN P1/P2 tickets.
    """
    return service.get_high_priority_tickets()


if __name__ == "__main__":
    mcp.run()
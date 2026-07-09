from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "tickets.db"

TICKETS = [('TKT-1001', 'Payment API', 'P1', 'OPEN', 'Card payment timeout', 'Customers report payment failures and timeout errors.', '2026-07-08T09:58:00', 'High', 'Application Support'), ('TKT-1002', 'Payment API', 'P1', 'OPEN', 'Payment requests failing', 'Multiple merchants report failed payment authorization calls.', '2026-07-08T10:02:00', 'High', 'Application Support'), ('TKT-1003', 'Payment API', 'P2', 'OPEN', 'Intermittent payment retry failures', 'Retries are not completing successfully for some transactions.', '2026-07-08T10:05:00', 'Medium', 'Payments Engineering'), ('TKT-1004', 'Checkout Service', 'P2', 'OPEN', 'Checkout page slow', 'Checkout completion is slower than normal.', '2026-07-08T09:45:00', 'Medium', 'Platform Operations'), ('TKT-1005', 'Checkout Service', 'P2', 'OPEN', 'Intermittent checkout failure', 'Some checkout requests fail after validation.', '2026-07-08T09:50:00', 'Medium', 'Platform Operations'), ('TKT-1006', 'Order Service', 'P3', 'OPEN', 'Order search delay', 'Internal support users report slow order search.', '2026-07-08T08:30:00', 'Low', 'Order Platform Team'), ('TKT-1007', 'Identity Service', 'P3', 'RESOLVED', 'Login delay', 'A small number of users experienced delayed login.', '2026-07-07T22:10:00', 'Low', 'Identity Engineering'), ('TKT-1008', 'Notification Service', 'P2', 'RESOLVED', 'Order confirmation email delay', 'Order confirmation emails were delayed.', '2026-07-07T14:15:00', 'Medium', 'Messaging Support'), ('TKT-1009', 'Payment API', 'P3', 'OPEN', 'Payment dashboard lag', 'Operations dashboard metrics are delayed.', '2026-07-08T10:08:00', 'Low', 'Application Support'), ('TKT-1010', 'Order Service', 'P4', 'OPEN', 'Order export formatting', 'CSV export formatting issue.', '2026-07-08T08:10:00', 'Low', 'Order Platform Team'), ('TKT-1011', 'Notification Service', 'P3', 'OPEN', 'SMS delivery delay', 'Some SMS messages are delayed.', '2026-07-08T07:55:00', 'Low', 'Messaging Support'), ('TKT-1012', 'Checkout Service', 'P1', 'OPEN', 'Checkout error spike', 'Priority escalation for checkout failures impacting customers.', '2026-07-08T10:04:00', 'High', 'Platform Operations')]

def create_database() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""CREATE TABLE tickets (ticket_id TEXT PRIMARY KEY, service_name TEXT NOT NULL, priority TEXT NOT NULL, status TEXT NOT NULL, subject TEXT NOT NULL, description TEXT NOT NULL, created_at TEXT NOT NULL, customer_impact TEXT NOT NULL, assigned_group TEXT NOT NULL)""")
        connection.executemany("INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", TICKETS)
        connection.commit()
    print(f"Created {DB_PATH} with {len(TICKETS)} tickets.")

if __name__ == "__main__":
    create_database()

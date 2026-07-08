import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "tickets.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operational_tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            subject TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TEXT NOT NULL,
            customer_impact TEXT NOT NULL,
            assigned_group TEXT NOT NULL
        )
    """)

    cursor.execute("DELETE FROM operational_tickets")

    mock_tickets = [
        ("payment-gateway", "High", "Open", "API Latency Spike", "Customers report processing delays at checkout", "2026-07-08T09:58:00", "High", "Application Support"),
        ("merchant-portal", "High", "In Progress", "Authentication Failures", "Multiple merchants unable to authenticate via dashboard", "2026-07-08T10:02:00", "High", "Application Support"),
        ("core-ledger", "Medium", "Open", "Retry Failures", "Retries are not completing within the expected timeout windows", "2026-07-08T10:05:00", "Medium", "Payments Engineering"),
        ("checkout-service", "Medium", "Investigating", "Drop-off Alert", "Checkout completion rate dropped below 85% threshold", "2026-07-08T09:45:00", "Medium", "Platform Operations"),
        ("checkout-service", "Medium", "Open", "HTTP 502 Errors", "Some checkout requests failing with bad gateway errors", "2026-07-08T09:50:00", "Medium", "Platform Operations"),
        ("internal-admin", "Low", "Resolved", "UI Bug", "Internal support users cannot view historical audit logs", "2026-07-08T08:30:00", "Low", "Order Platform Team"),
        ("auth-service", "Low", "Closed", "Token Refresh", "A small number of users experiencing intermittent logout issues", "2026-07-07T22:10:00", "Low", "Identity Engineering"),
        ("notification-engine", "Medium", "Open", "SMS Delays", "Order confirmation SMS delivery delayed across regions", "2026-07-07T14:15:00", "Medium", "Messaging Support"),
        ("analytics-pipeline", "Low", "Open", "Stale Metrics", "Operations dashboard reporting 15 minute delay on ingestion", "2026-07-08T10:08:00", "Low", "Application Support"),
        ("reporting-app", "Low", "Open", "Export Crash", "CSV export formatting breaks on multi-byte characters", "2026-07-08T08:10:00", "Low", "Order Platform Team")
    ]

    cursor.executemany("""
        INSERT INTO operational_tickets 
        (service_name, priority, status, subject, description, created_at, customer_impact, assigned_group)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, mock_tickets)

    conn.commit()
    conn.close()
    print(f"Initialized database instance with custom tables at: {DB_PATH}")

if __name__ == "__main__":
    init_db()

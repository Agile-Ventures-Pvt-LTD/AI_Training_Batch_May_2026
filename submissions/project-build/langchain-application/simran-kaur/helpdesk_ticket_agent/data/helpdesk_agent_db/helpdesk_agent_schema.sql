CREATE INDEX idx_archival_memory_key ON archival_memory(memory_key);

CREATE INDEX idx_conversation_logs_session_id ON conversation_logs(session_id);

CREATE INDEX idx_ticket_comments_ticket_id ON ticket_comments(ticket_id);

CREATE INDEX idx_tickets_assigned_to ON tickets(assigned_to);

CREATE INDEX idx_tickets_category ON tickets(category);

CREATE INDEX idx_tickets_customer_tier ON tickets(customer_tier);

CREATE INDEX idx_tickets_due_at ON tickets(due_at);

CREATE INDEX idx_tickets_priority ON tickets(priority);

CREATE INDEX idx_tickets_status ON tickets(status);

CREATE TABLE archival_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_key TEXT NOT NULL,
    memory_value TEXT NOT NULL,
    memory_type TEXT,
    importance INTEGER DEFAULT 3,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE conversation_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    user_message TEXT,
    agent_response TEXT,
    tools_used TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE conversation_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    summary TEXT,
    key_decisions TEXT,
    open_items TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    customer_email TEXT,
    customer_age INTEGER,
    customer_gender TEXT,
    company_name TEXT,
    customer_tier TEXT CHECK(customer_tier IN ('Enterprise','Premium','Standard')),
    industry TEXT,
    region TEXT,
    account_manager TEXT
);

CREATE TABLE "raw_customer_support_tickets" (
"ticket_id" INTEGER,
  "customer_name" TEXT,
  "customer_email" TEXT,
  "customer_age" INTEGER,
  "customer_gender" TEXT,
  "product_purchased" TEXT,
  "date_of_purchase" TEXT,
  "ticket_type" TEXT,
  "ticket_subject" TEXT,
  "ticket_description" TEXT,
  "ticket_status" TEXT,
  "resolution" TEXT,
  "ticket_priority" TEXT,
  "ticket_channel" TEXT,
  "first_response_time" TEXT,
  "time_to_resolution" TEXT,
  "customer_satisfaction_rating" REAL
);

CREATE TABLE sla_policies (
    priority TEXT PRIMARY KEY,
    sla_hours INTEGER NOT NULL,
    description TEXT
);

CREATE TABLE sqlite_sequence(name,seq);

CREATE TABLE ticket_comments (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id TEXT NOT NULL,
    author TEXT,
    comment_type TEXT,
    comment TEXT NOT NULL,
    created_at TEXT,
    FOREIGN KEY(ticket_id) REFERENCES tickets(ticket_id)
);

CREATE TABLE tickets (
    ticket_id TEXT PRIMARY KEY,
    source_ticket_id INTEGER,
    customer_id TEXT,
    customer_name TEXT,
    company_name TEXT,
    customer_tier TEXT,
    product_purchased TEXT,
    date_of_purchase TEXT,
    category TEXT,
    ticket_type TEXT,
    priority TEXT CHECK(priority IN ('Urgent','High','Medium','Low')),
    original_priority TEXT,
    status TEXT,
    channel TEXT,
    assigned_to TEXT,
    subject TEXT,
    description TEXT,
    resolution TEXT,
    created_at TEXT,
    due_at TEXT,
    last_updated_at TEXT,
    closed_at TEXT,
    sla_hours INTEGER,
    original_first_response_time TEXT,
    original_time_to_resolution TEXT,
    customer_satisfaction_rating REAL,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE tool_audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    tool_name TEXT,
    tool_input TEXT,
    tool_output TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE VIEW open_tickets AS
SELECT *
FROM tickets
WHERE status != 'Closed';

CREATE VIEW overdue_tickets AS
SELECT *,
       CASE
           WHEN status = 'Closed' THEN 'CLOSED'
           WHEN datetime(due_at) < datetime('2026-06-12 09:00:00') THEN 'BREACHED'
           WHEN date(due_at) = date('2026-06-12 09:00:00') THEN 'DUE_TODAY'
           ELSE 'WITHIN_SLA'
       END AS sla_status
FROM tickets
WHERE status != 'Closed'
  AND datetime(due_at) < datetime('2026-06-12 09:00:00');

CREATE VIEW ticket_work_queue AS
SELECT
    ticket_id,
    customer_name,
    company_name,
    customer_tier,
    category,
    priority,
    status,
    assigned_to,
    subject,
    channel,
    created_at,
    due_at,
    CASE
        WHEN status = 'Closed' THEN 'CLOSED'
        WHEN datetime(due_at) < datetime('2026-06-12 09:00:00') THEN 'BREACHED'
        WHEN date(due_at) = date('2026-06-12 09:00:00') THEN 'DUE_TODAY'
        ELSE 'WITHIN_SLA'
    END AS sla_status,
    CASE priority
        WHEN 'Urgent' THEN 4
        WHEN 'High' THEN 3
        WHEN 'Medium' THEN 2
        ELSE 1
    END
    + CASE customer_tier
        WHEN 'Enterprise' THEN 3
        WHEN 'Premium' THEN 2
        ELSE 1
      END
    + CASE
        WHEN status != 'Closed' AND datetime(due_at) < datetime('2026-06-12 09:00:00') THEN 5
        WHEN status != 'Closed' AND date(due_at) = date('2026-06-12 09:00:00') THEN 3
        ELSE 0
      END AS priority_score
FROM tickets
WHERE status != 'Closed';
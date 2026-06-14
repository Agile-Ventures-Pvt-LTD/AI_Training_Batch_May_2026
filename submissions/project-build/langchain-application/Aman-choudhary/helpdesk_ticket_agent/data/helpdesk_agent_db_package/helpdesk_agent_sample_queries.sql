-- Sample queries for AI Helpdesk Ticket Operations Agent

-- 1. Count tickets by status
SELECT status, COUNT(*) AS total
FROM tickets
GROUP BY status
ORDER BY total DESC;

-- 2. Show open high-priority or urgent tickets
SELECT ticket_id, customer_name, customer_tier, category, priority, status, assigned_to, subject, due_at
FROM tickets
WHERE status != 'Closed'
  AND priority IN ('Urgent', 'High')
ORDER BY due_at ASC;

-- 3. Show overdue tickets using deterministic training reference time
SELECT ticket_id, customer_name, customer_tier, category, priority, status, assigned_to, subject, due_at, sla_status
FROM overdue_tickets
ORDER BY due_at ASC;

-- 4. Recommended work queue
SELECT ticket_id, customer_name, customer_tier, category, priority, status, subject, sla_status, priority_score
FROM ticket_work_queue
ORDER BY priority_score DESC, due_at ASC
LIMIT 20;

-- 5. Get one ticket details
SELECT *
FROM tickets
WHERE ticket_id = 'TCK-00001';

-- 6. Get ticket comments
SELECT comment_id, author, comment_type, comment, created_at
FROM ticket_comments
WHERE ticket_id = 'TCK-00001'
ORDER BY created_at ASC;

-- 7. Update ticket status
UPDATE tickets
SET status = 'In Progress', last_updated_at = CURRENT_TIMESTAMP
WHERE ticket_id = 'TCK-00001';

-- 8. Add internal comment
INSERT INTO ticket_comments(ticket_id, author, comment_type, comment, created_at)
VALUES ('TCK-00001', 'Agent', 'internal_note', 'Billing team is reviewing the duplicate invoice.', CURRENT_TIMESTAMP);

-- 9. Store archival memory
INSERT INTO archival_memory(memory_key, memory_value, memory_type, importance)
VALUES ('user_priority_preference', 'User prefers to prioritize Enterprise customer issues first.', 'preference', 5);

-- 10. Recall archival memory
SELECT *
FROM archival_memory
WHERE memory_key LIKE '%priority%'
   OR memory_value LIKE '%Enterprise%'
ORDER BY importance DESC, updated_at DESC;
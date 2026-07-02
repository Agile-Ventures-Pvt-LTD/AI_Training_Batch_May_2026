# Sample Queries and Execution Scenarios
This document outlines the standard natural language queries that the Jira Issue Assistant is designed to process, along with the expected tool flow and parameters.
## 1. List all Jira Projects
*   **Query:** "List all Jira projects" or "Show me what projects are available"
*   **Expected Tools Used:** `list_projects`
*   **Response Format:** Markdown table containing project key, name, and style.
*   **Write Action:** `False`
---
## 2. Show Open Issues
*   **Query:** "Show all open issues" or "List issues that are open"
*   **Expected Tools Used:** `search_issues`
*   **Expected JQL parameter:** `status = 'Open'` (or equivalent open status names like `status = 'To Do'`)
*   **Response Format:** Markdown table of issues.
*   **Write Action:** `False`
---
## 3. Show High-Priority Issues
*   **Query:** "Show all high priority issues" or "Show me issues that are urgent"
*   **Expected Tools Used:** `search_issues`
*   **Expected JQL parameter:** `priority = 'High' OR priority = 'Highest'` (or matching priority terms)
*   **Response Format:** Sorted list of high priority issues.
*   **Write Action:** `False`
---
## 4. Summarize an Issue
*   **Query:** "Summarize issue ABC-12" or "Give me details on DEMO-2"
*   **Expected Tools Used:** `get_issue_details`
*   **Expected Parameters:** `issue_key: "ABC-12"` or `"DEMO-2"`
*   **Response Format:** Structured breakdown of the summary, status, priority, assignee, reporter, and description.
*   **Write Action:** `False`
---
## 5. Show Comments
*   **Query:** "Show comments for issue ABC-12" or "What are the comments on ticket DEMO-1?"
*   **Expected Tools Used:** `get_issue_comments`
*   **Expected Parameters:** `issue_key: "ABC-12"` or `"DEMO-1"`
*   **Response Format:** Chronological listing of comments showing author, date, and body text.
*   **Write Action:** `False`
---
## 6. Add a Comment
*   **Query:** "Add a comment to ABC-5 saying QA validation is pending" or "Comment on ticket DEMO-1: 'Ready for review'"
*   **Expected Tools Used:** `add_issue_comment`
*   **Expected Parameters:** `issue_key: "ABC-5"`, `comment_text: "QA validation is pending"`
*   **Response Format:** Confirmation of comment creation with author and timestamp.
*   **Write Action:** `True`
---
## 7. Update Issue Status
*   **Query:** "Move issue ABC-12 to In Progress" or "Change status of DEMO-2 to Done"
*   **Expected Tools Used:** `update_issue_status`
*   **Expected Parameters:** `issue_key: "ABC-12"`, `status_name: "In Progress"`
*   **Response Format:** Confirmation of transition ID, transition name, and new status of the issue.
*   **Write Action:** `True`
---
## 8. Show Assigned Issues
*   **Query:** "Which issues are assigned to me?" or "Show my assigned tickets"
*   **Expected Tools Used:** `search_issues`
*   **Expected JQL parameter:** `assignee = currentUser()`
*   **Response Format:** List of issues assigned to the currently authenticated user.
*   **Write Action:** `False`
---
## Multi-Step Query Example: Summarize and List Comments
*   **Query:** "Summarize ABC-12 including comments"
*   **Expected Tools Used:** `get_issue_details`, `get_issue_comments`
*   **Flow:**
    1. LLM requests `get_issue_details(issue_key="ABC-12")`
    2. Client returns details
    3. LLM requests `get_issue_comments(issue_key="ABC-12")`
    4. Client returns comments list
    5. LLM combines details and comments to present a comprehensive, beautifully formatted report.
*   **Write Action:** `False`
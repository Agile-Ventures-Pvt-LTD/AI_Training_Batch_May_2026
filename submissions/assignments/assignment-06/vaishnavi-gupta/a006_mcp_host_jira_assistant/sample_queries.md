# Sample Queries

## Project Queries

### List all Jira projects

List all Jira projects.

---

## Issue Queries

### Show all open issues

Show all open issues.

### Show all unresolved bugs

Show unresolved bugs.


### Show all high-priority issues

Show all high-priority issues.


### Show all issues assigned to me

Which issues are assigned to me?

### Show blockers in the current sprint

What are the blockers in the current sprint?

---

## Issue Details

### Summarize an issue

Summarize issue PROJ-1.


### Show complete issue details

Show complete details of PROJ-1.

### Show issue comments

Show comments for PROJ-1.

### Summarize an issue including comments

Summarize PROJ-1 including all comments.

---

## Search Queries

### Search all bugs

Search all bug issues.

### Search open bugs

Show all open bugs.

### Search high-priority bugs

Show all high-priority bugs.

### Search issues assigned to a user

Show all issues assigned to John Doe.

---

## Write Operations

### Add a comment


Add a comment to PROJ-1 saying:

QA validation is pending.


### Add another comment

Add a comment to PROJ-1:

Issue verified successfully.


### Update issue status


Move PROJ-1 to In Progress.


### Mark issue as Done

Update PROJ-1 to Done.


### Close an issue


Close issue PROJ-1.

---

## Multi-Step Queries

### Issue summary with comments

Summarize PROJ-1 including comments.

### High-priority issues with details


Show all high-priority issues and summarize each one.


### Open bugs assigned to me

Show all open bugs assigned to me.


### Show blockers with comments

Show blockers in the current sprint along with their comments.
---

## Example Expected Output


{
    "user_query": "Show all open high-priority issues.",
    "tools_used": [
        "search_issues"
    ],
    "final_answer": "Found 5 open high-priority issues in the Jira project.",
    "write_action_performed": false
}


---

## Example Write Operation Output

{
    "user_query": "Add a comment to PROJ-1 saying QA validation is pending.",
    "tools_used": [
        "add_issue_comment"
    ],
    "final_answer": "The comment has been successfully added to PROJ-1.",
    "write_action_performed": true
}

---

## Notes

* Replace **PROJ-1** with an actual Jira issue key from your Jira project.
* Ensure the Jira MCP Server is running before starting the host.
* Configure all required environment variables in the .env file.
* The assistant uses MCP tools for all Jira-related operations and does not generate Jira data without querying the server.

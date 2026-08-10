
# Sample Queries
Run these against `python src/host.py` after creating dummy Jira issues.

## 1. List all Jira projects

Query: `List all Jira projects`
Tools used: `list_projects`
Expected: names and keys of every project visible to the configured account.

## 2. Show open issues

Query: `Show open issues`
Tools used: `search_issues` with a JQL like `statusCategory != Done`
Expected: a short list of currently open issue keys and summaries.

## 3. Show high-priority issues

Query: `Show all open high-priority issues.`
Tools used: `search_issues` with JQL like
`priority in (High, Highest) AND statusCategory != Done`
Expected: matching issue keys, summaries, and priorities.

## 4. Summarize an issue

Query: `Summarize issue ABC-12.`
Tools used: `get_issue_details`
Expected: a short prose summary of the issue's summary, status, priority,
and assignee.

## 5. Show comments

Query: `Show comments on ABC-12`
Tools used: `get_issue_comments`
Expected: a list of commenters and what they said.

## 6. Add a comment

Query: `Add a comment to ABC-5 saying QA validation is pending.`
Tools used: `add_issue_comment`
Expected: confirmation the comment was added, with an explicit note that a
write action was performed. `write_action_performed` is `true`.

## 7. Update issue status

Query: `Update ABC-9 status to Done`
Tools used: `update_issue_status`
Expected: confirmation of the new status, with an explicit note that a
write action was performed. `write_action_performed` is `true`.

## 8. Show assigned issues

Query: `Which issues are assigned to me?`
Tools used: `search_issues` with JQL like `assignee = currentUser()`
Expected: issues currently assigned to the authenticated Jira account.

## Additional multi-step example

Query: `Summarize ABC-12 including comments`
Tools used: `get_issue_details`, then `get_issue_comments`
Expected: a combined summary drawing on both tool results in a single
`final_answer`, with both tool names present in `tools_used` in call order.

## Additional blocker example

Query: `What are blockers in the current sprint?`
Tools used: `search_issues` with JQL like
`sprint in openSprints() AND (priority = Blocker OR labels = blocker)`
Expected: issues currently blocking the active sprint, if the project uses
sprints and a "Blocker" label or priority convention. --> -->

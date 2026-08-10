# Orchestration Patterns

## 1. Sequential
Used where a later step depends on an earlier result.

```text
Validate -> Retrieve -> Decision
```

## 2. Parallel / Fan-Out
After intake is Valid, independent evidence specialists should run in parallel:

```text
                 Supervisor
                     |
      +--------------+--------------+
      |       |       |       |      |
   Pattern Returns Product Customer Safety
```

## 3. Fan-In
The Supervisor collects all specialist results before making the final classification.

Rules:
- Missing result != Passed.
- Preserve Failed, Missing, and Unverified states.
- Do not invent evidence.

## 4. Hierarchical
The Supervisor delegates domain analysis to child agents and retains final decision authority.

## 5. Conditional
Decision priority:
1. Safety
2. Previous incident + repeated failure
3. Return-rate threshold
4. Complaint cluster
5. Monitoring/Informational

## 6. Loop / Reassessment
When new evidence arrives:
- identify changed evidence domain;
- rerun only the affected specialist where appropriate;
- preserve unaffected results;
- recalculate classification.

## 7. Fallback
If Microsoft Learn MCP is unavailable:
`Microsoft guidance unavailable - manual review.`

MCP failure must not alter the core quality decision.

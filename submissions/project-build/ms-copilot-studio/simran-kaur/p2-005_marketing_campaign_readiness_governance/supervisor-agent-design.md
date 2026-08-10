# Supervisor Agent Design

## Role
The Campaign Readiness Supervisor is the central orchestrator and final decision authority.

## Responsibilities
- Identify and process an eligible Pending campaign.
- Invoke Campaign Intake & Validation.
- Move the campaign to In Assessment before specialist analysis.
- Delegate independent specialist assessments.
- Wait for mandatory results and consolidate them.
- Invoke Launch Risk & Decision after fan-in.
- Decide whether remediation or approval is required.
- Decide whether selective reassessment is required.
- Resolve conflicting specialist findings.
- Perform final readiness validation.
- Authorize Word generation and Outlook communication.
- Update campaign state in Excel.

## Final decision authority
Only the Supervisor can:
- assign final readiness;
- resolve specialist conflicts;
- decide reassessment;
- authorize final Word generation;
- authorize Outlook communication.

Child agents return findings rather than independently assigning final readiness.

## State control
The Supervisor must prevent invalid state progression and must not mark a campaign Ready while mandatory approval is outstanding or while blocking evidence is unresolved.

## Final outcome precedence
1. Not Ready
2. Management Approval Required
3. Remediation Required
4. Ready with Conditions
5. Ready

The system must not average specialist outcomes.

## Failure handling
No specialist result means the Supervisor cannot assume success. Failed specialists are retried once; persistent failure becomes insufficient evidence and routes to Manual Review.

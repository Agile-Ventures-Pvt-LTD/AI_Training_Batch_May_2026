# Known Limitations

The following are implementation limitations or evidence items to be tracked during the build. They should be updated to reflect actual observed behavior before submission.

## 1. Copilot Studio execution semantics
The project requires logical parallel fan-out/fan-in. The PRD does not require proof of infrastructure-level simultaneous execution; the implementation must demonstrate independent specialist branches and waiting for required results.

## 2. External human approval
Human approval must be represented by an actual approval state or mechanism. The agent must never infer or fabricate an approval.

## 3. Connector availability
Excel, Word, and Outlook connector access depends on the configured Microsoft 365 environment and permissions.

## 4. Evidence
Screenshots are placeholders until replaced with actual Copilot Studio screenshots.

## 5. Test status
The repository contains the required test matrix, but tests must be executed and evidence recorded before claims of completion are made.

## 6. Data scope
The project is intended to use synthetic data.

## 7. Failure handling
Word/Outlook/Excel failures must be recorded without falsely claiming that the downstream action succeeded.

## 8. Campaign launch
The system evaluates readiness only. It does not autonomously launch campaigns.

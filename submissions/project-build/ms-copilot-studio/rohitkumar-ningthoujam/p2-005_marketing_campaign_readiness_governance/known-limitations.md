# Known Limitations

## Current Limitations

### 1. Excel as Data Store
The solution uses Excel Online as the campaign repository. While suitable for demonstration purposes, Excel is not intended for high-volume concurrent updates and may encounter row locking during simultaneous operations.

### 2. Rule Configuration
Business rules are stored in the dataset and agent instructions. Changes to governance policies require updating the configuration rather than using a centralized rule engine.

### 3. Child Agent Responses
The supervisor depends on child agents returning valid structured outputs. Unexpected or empty responses require fallback handling or manual review.

### 4. Remediation Cycles
The implementation supports selective reassessment after remediation. Repeated failures are escalated to manual review rather than allowing unlimited reassessment loops.

### 5. External Connectors
Word document generation, Outlook email, and Excel updates rely on Microsoft 365 connector availability and permissions. Connector failures may interrupt the final workflow.

### 6. Dataset Scope
The supplied dataset represents sample campaign scenarios from the project. Production deployment would require integration with enterprise campaign management systems.

### 7. Approval Workflow
Executive approvals are simulated using decision logic. Integration with enterprise approval platforms is outside the scope of this implementation.

## Assumptions

- Campaign IDs are unique.
- Specialist agents return standardized outputs.
- Required Microsoft 365 connectors are configured.
- Dataset follows the provided project schema.
- Supervisor agent is the only orchestration entry point.

## Future Improvements

- Replace Excel with Dataverse or SQL Server.
- Externalize governance rules into a configurable rule engine.
- Add audit logging and monitoring dashboards.
- Support dynamic specialist selection.
- Integrate enterprise approval workflows.
- Add notification retries with exponential backoff.
- Enable versioned policy management.
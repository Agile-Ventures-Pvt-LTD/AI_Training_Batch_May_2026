# Known Limitations

## Overview

This document outlines the current technical limitations of the Campaign Readiness Assessment Supervisor. These limitations primarily arise from the capabilities of Microsoft Copilot Studio, Power Automate, and the use of Excel Online as the operational data source. None of these limitations affect the overall architectural design of the solution.

---

# 1. Excel as the Operational Data Source

The solution currently uses **Excel Online (Business)** to store campaign information and supporting datasets.

### Limitations

- Limited support for concurrent updates.
- No relational database capabilities.
- No built-in referential integrity.
- Performance may decrease with large datasets.
- Less scalable than enterprise databases such as Microsoft Dataverse.

---

# 2. AI Builder Prompt Input Constraints

AI Builder Prompt requires explicit input parameter mapping.

### Limitations

- Individual fields must be mapped manually.
- Complex objects cannot always be passed directly.
- Prompt execution depends on correctly configured input bindings.

---

# 3. Copilot Studio Variable Management

Microsoft Copilot Studio currently has limited support for sharing variables across topics and workflow components.

### Limitations

- Variables must be managed explicitly within topics.
- Table outputs require iteration before individual records can be accessed.
- Complex data structures require additional processing.

---

# 4. Table Processing Limitations

Excel connector actions such as **List Rows** return collections rather than individual records.

### Limitations

- Returned tables cannot be directly passed to AI Builder Prompts.
- Individual campaign records must be extracted before validation.
- Additional looping logic is required for record processing.

---

# 5. Stateless Workflow Execution

Each assessment is executed independently.

### Limitations

- Previous execution context is not retained automatically.
- Historical assessment information requires external storage.
- Long-term campaign history is not maintained by the Supervisor Agent.

---

# 6. Dependency on Microsoft Services

The solution depends on Microsoft cloud services.

These include:

- Microsoft Copilot Studio
- Power Automate
- Excel Online (Business)
- Microsoft Outlook
- Microsoft Word

Temporary service interruptions may affect workflow execution.

---

# 7. Manual Dataset Maintenance

Campaign information is maintained within Excel Online.

The solution assumes:

- Correct campaign information
- Consistent data formats
- Valid business values
- Complete records

Data quality directly affects assessment accuracy.

---

# Future Enhancements

The architecture supports future enhancements including:

- Migration from Excel Online to Microsoft Dataverse.
- Persistent assessment history.
- Advanced approval tracking.
- Dashboard and analytics integration.
- Audit logging.
- Role-based security.
- Real-time monitoring.
- Enterprise reporting.

---

# Assumptions

The solution assumes:

- Campaign IDs are unique.
- Campaign data follows the defined schema.
- Required Microsoft connectors are configured.
- Users have appropriate permissions.
- Specialist agents return standardized outputs.

---

# Conclusion

The identified limitations are primarily platform-related rather than architectural. The Campaign Readiness Assessment Supervisor has been designed using modular orchestration and standardized specialist interactions, allowing the solution to evolve as additional Microsoft Copilot Studio capabilities and enterprise services become available.
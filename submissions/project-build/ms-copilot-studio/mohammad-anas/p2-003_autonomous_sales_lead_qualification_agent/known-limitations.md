# Known Limitations

## Project Information

| Item | Details |
|------|---------|
| Project ID | P2-003 |
| Project Name | Autonomous Sales Lead Qualification Agent |
| Platform | Microsoft Copilot Studio |
| Participant | Mohammad Anas |

---

# Purpose

This document describes the known limitations of the Autonomous Sales Lead Qualification Agent at the time of project submission.

These limitations do not prevent the solution from demonstrating the required project objectives but identify areas where future improvements or additional configuration would enhance the solution.

---

# Current Limitations

## 1. Outlook Reply Action

### Description

During testing, the **Reply to Email (V3)** connector occasionally returned a recipient validation error within the Microsoft Copilot Studio test environment.

### Impact

- Customer acknowledgement emails may not be sent successfully during manual testing.
- The core lead qualification workflow remains unaffected.

### Future Improvement

- Validate the workflow in a fully published environment.
- Replace the reply action with **Send an Email (V2)** if the business process does not require replying within the original email thread.

---

## 2. Dependency on Microsoft 365 Services

### Description

The solution depends entirely on Microsoft 365 services and connectors.

### Impact

If any required Microsoft service is unavailable, affected workflow steps cannot be completed.

Affected services include:

- Outlook
- Excel Online (Business)
- Word Online (Business)

### Future Improvement

Implement monitoring and notification mechanisms for connector failures.

---

## 3. Connector Authentication

### Description

All connector actions require valid Microsoft 365 authentication.

### Impact

Expired credentials or revoked permissions will prevent connector execution.

### Future Improvement

Implement periodic authentication validation and connector health monitoring.

---

## 4. AI Information Extraction

### Description

Lead information is extracted from unstructured email content using AI capabilities.

### Impact

If customer emails contain incomplete, ambiguous, or poorly formatted information, some fields may remain unknown.

The agent intentionally avoids guessing missing values.

### Future Improvement

Use standardized lead submission forms or structured templates to improve extraction accuracy.

---

## 5. Business Rule Maintenance

### Description

Qualification decisions depend on operational reference tables.

### Impact

Outdated qualification rules, territory mappings, or product catalogs may produce outdated classifications.

### Future Improvement

Establish a governance process for regular maintenance of reference tables.

---

## 6. Human Review Dependency

### Description

The solution routes uncertain cases for manual review instead of making unsupported autonomous decisions.

### Impact

Certain opportunities require human intervention before processing can continue.

### Future Improvement

Expand business rules and confidence thresholds to reduce manual reviews while maintaining governance.

---

## 7. Performance Validation

### Description

Testing focused on functional correctness.

Large-scale production workloads were not evaluated.

### Impact

Performance characteristics under high email volumes are currently unknown.

### Future Improvement

Conduct load testing using production-scale datasets.

---

## 8. Limited Attachment Processing

### Description

The current implementation primarily evaluates email content.

Attachments are available through the Outlook trigger but are not analyzed as part of the qualification process.

### Impact

Important business information contained only in attached files may not be considered during qualification.

### Future Improvement

Extend the workflow to process supported attachment formats such as PDF, DOCX, and Excel files.

---

## 9. Language Support

### Description

The solution is optimized for English-language sales enquiries.

### Impact

Emails written in other languages may reduce extraction accuracy and qualification confidence.

### Future Improvement

Add multilingual prompts and language detection before processing.

---

## 10. External System Integration

### Description

The project integrates only with Microsoft 365 services.

### Impact

The solution does not automatically synchronize data with CRM platforms such as Dynamics 365, Salesforce, or HubSpot.

### Future Improvement

Implement additional connector integrations to synchronize qualified leads with enterprise CRM systems.

---

# Assumptions

The solution assumes that:

- Microsoft 365 connectors are correctly configured.
- Required permissions are available.
- Operational Excel tables contain valid business data.
- Incoming emails follow the expected sales enquiry format.
- Users have access to the required Microsoft services.

---

# Out of Scope

The following capabilities are intentionally outside the scope of this project:

- Price quotation generation
- Contract creation
- Commercial negotiation
- Invoice generation
- Customer onboarding
- Payment processing
- CRM synchronization
- Predictive lead scoring using historical analytics

---

# Recommendations

The following enhancements are recommended for future versions:

- Replace or reconfigure the Outlook reply action after deployment validation.
- Add attachment analysis.
- Support multilingual lead processing.
- Integrate with enterprise CRM platforms.
- Implement centralized logging and monitoring.
- Add workflow analytics dashboards.
- Perform production-scale performance testing.
- Introduce automated health monitoring for Microsoft 365 connectors.

---

# Conclusion

The Autonomous Sales Lead Qualification Agent successfully demonstrates the required project functionality while operating within the defined project scope.

The identified limitations primarily relate to deployment configuration, Microsoft 365 connector dependencies, and planned future enhancements rather than deficiencies in the core qualification workflow.

Addressing these limitations would further improve reliability, scalability, and enterprise readiness while preserving the existing autonomous lead qualification process.
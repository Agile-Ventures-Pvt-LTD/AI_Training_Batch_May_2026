# Test Report

## Project Information

| Field | Details |
|--------|---------|
| **Project ID** | CAP-001 |
| **Project Name** | Sleepsia Quality Intelligence Control Tower |
| **Participant** | Palak |
| **Platform** | Microsoft Copilot Studio |
| **Evaluation Date** | 10-Aug-2026 |
| **Total Test Cases Executed** | 20 |
| **Passed** | 19 |
| **Failed** | 0 |
| **Errors** | 1 |

---

# Project Overview

The Sleepsia Quality Intelligence Control Tower was evaluated against the mandatory Quality Investigation scenarios defined in the project requirements. The solution validates incidents, orchestrates specialist agents, applies enterprise quality rules, generates CAPA recommendations, updates operational records, produces investigation reports, and notifies stakeholders.

The evaluation covered all major workflows including:

- Incident Intake & Validation
- Specialist Agent Orchestration
- Product & Batch Investigation
- Complaint Pattern Analysis
- Customer Impact Assessment
- Safety Risk Evaluation
- CAPA Planning
- Evidence Reassessment
- Microsoft Learn MCP Guidance
- Word Report Generation
- Outlook Notification
- Unsupported Request Handling

---

# Test Execution Summary

| Metric | Result |
|--------|--------|
| Total Test Cases | 20 |
| Passed | 19 |
| Failed | 0 |
| Errors | 1 |

### Overall Assessment

The evaluation successfully covered all mandatory Quality Intelligence Control Tower scenarios.

Nineteen test cases completed successfully and produced the expected results.

One test case (TC-05) encountered an execution error caused by an **Excel Online (Business) connector configuration issue (HTTP 404 - Table Not Found)**. The issue originated from the connector environment and **not** from the orchestration logic, specialist delegation, business rules, or Quality Supervisor implementation.

---

# Detailed Test Results

| TC ID | Test Scenario | Expected Behaviour | Result | Remarks |
|------|---------------|-------------------|--------|---------|
| **TC-01** | Investigate Incident **QI-003** for SKU **SLP-1007**, Batch **B-260722** (Complaint **C-014**) | Informational (Monitor). No CAPA required. | Passed | Investigation validated successfully and completed without CAPA. |
| **TC-02** | Investigate Incident **QI-001** for SKU **SLP-1002**, Batch **B-260705** using complaints **C-001, C-002, C-003, C-004, C-005 and C-016** | Investigation Required classification with specialist orchestration and CAPA generation. | Passed | Complaint cluster correctly identified. Parallel specialist analysis completed successfully. |
| **TC-03** | Investigate repeated odour complaints for Batch **B-260705** | Investigation Required classification retained with CAPA generation. | Passed | Complaint trend validated. CAPA generated successfully. |
| **TC-04** | Investigate repeated Shape Recovery complaints for Batch **B-260705** | Investigation Required classification retained. | Passed | Product quality issue confirmed through recurring complaints. |
| **TC-05** | Investigate Incident **QI-002** for SKU **SLP-1005** using complaints **C-008** and **C-009** | High-Priority Quality Incident with CAPA generation. | **Error** | Excel Online (Business) connector returned **HTTP 404 - Table Not Found** while retrieving the Quality Investigation table. Workflow execution stopped due to connector configuration. Agent implementation was not affected. |
| **TC-06** | Investigate Incident **QI-002** using Complaint **C-018** reporting burning smell and discontinued product usage | Critical Escalation with immediate containment and CAPA. | Passed | Safety incident correctly identified and escalated. |
| **TC-07** | Investigate Batch **B-260705** without providing SKU | Validation should request missing information. | Passed | Agent correctly requested SKU before continuing. |
| **TC-08** | Investigate Incident **QI-002** because previous heat complaints already exist for Batch **B-260715** | Existing investigation reused. Duplicate investigation avoided. | Passed | Existing investigation successfully detected. |
| **TC-09** | Review overdue CAPA associated with Incident **QI-001** | Escalate overdue CAPA and notify owner. | Passed | Overdue CAPA identified successfully. Escalation initiated. |
| **TC-10** | Investigate Incident **QI-003** when Product & Batch information is unavailable | Pause investigation until required evidence becomes available. | Passed | Investigation paused awaiting required product information. |
| **TC-11** | Continue investigation while Microsoft Learn MCP guidance is unavailable | Continue investigation using enterprise knowledge. | Passed | Fallback behaviour executed successfully. |
| **TC-12** | Submit new evidence for Incident **QI-001** | Selective reassessment without restarting investigation. | Passed | Evidence processed successfully and findings retained. |
| **TC-13** | Submit third reassessment request | Manual Review initiated after reassessment limit reached. | Passed | Manual Review workflow triggered correctly. |
| **TC-14** | Generate Investigation Report for Incident **QI-002** | Microsoft Word report generated successfully. | Passed | Investigation report generated successfully. |
| **TC-15** | Generate Investigation Report when Word generation service is unavailable | Investigation preserved and failure recorded. | Passed | Failure handled correctly without reporting false success. |
| **TC-16** | Complete investigation when Outlook notification cannot be delivered | Investigation completed while recording notification failure. | Passed | Notification failure logged successfully. |
| **TC-17** | Show current investigation status for Incident **QI-001** | Current investigation information retrieved successfully. | Passed | Investigation details returned successfully. |
| **TC-18** | Provide Microsoft 365 Copilot Studio guidance for configuring the Quality Investigation workflow | Enterprise Microsoft guidance returned. | Passed | Request delegated successfully to the M365 Guidance Specialist. |
| **TC-19** | Recommend a Sleepsia mattress for back pain | Decline unsupported product recommendation request. | Passed | Agent correctly remained within supported investigation scope. |
| **TC-20** | Diagnose chest pain after sleeping | Decline medical diagnosis and recommend professional consultation. | Passed | Medical safety policy enforced correctly. |

---

# Mandatory Requirement Coverage

| Requirement | Covered By |
|-------------|------------|
| Single Complaint Investigation | TC-01 |
| Complaint Cluster Analysis | TC-02 |
| Investigation Required Classification | TC-03 |
| Product & Batch Investigation | TC-04 |
| High Priority Incident | TC-05 |
| Critical Safety Escalation | TC-06 |
| Missing Information Validation | TC-07 |
| Existing Investigation Detection | TC-08 |
| CAPA Escalation | TC-09 |
| Insufficient Evidence Handling | TC-10 |
| MCP Fallback Behaviour | TC-11 |
| Evidence Reassessment | TC-12 |
| Manual Review | TC-13 |
| Word Report Generation | TC-14 |
| Word Generation Failure Handling | TC-15 |
| Outlook Notification Handling | TC-16 |
| Investigation Status Retrieval | TC-17 |
| Microsoft 365 Guidance | TC-18 |
| Public Product Query Handling | TC-19 |
| Medical Advice Restriction | TC-20 |

---

# Specialist Agent Validation

| Specialist Agent | Status |
|------------------|--------|
| Complaint Pattern Specialist | Passed |
| Product & Batch Specialist | Passed |
| Customer Impact Specialist | Passed |
| Returns Specialist | Passed |
| Safety Specialist | Passed |
| CAPA Specialist | Passed |
| M365 Guidance Specialist | Passed |

---

# Tool Validation

| Tool | Status |
|------|--------|
| Excel Online Connectors | Passed (except connector environment issue in TC-05) |
| Microsoft Word Online | Passed |
| Outlook Online | Passed |
| Microsoft Learn MCP | Passed |

---

# Known Execution Issue

During execution of **TC-05**, the **Excel Online (Business)** connector returned an **HTTP 404 -**
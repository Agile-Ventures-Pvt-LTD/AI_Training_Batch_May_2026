# Test Report

## Project Information

| Field | Details |
|--------|---------|
| **Project ID** | P2-002 |
| **Project Name** | Product Support & Warranty Assistant |
| **Platform** | Microsoft Copilot Studio |
| **Chatbot Name** | NovaRetail Product Support & Warranty Assistant |
| **Tested By** | Vikash Kumar |
| **Test Date** | <DD/MM/YYYY> |

---

# Testing Objective

The objective of testing was to verify that the chatbot correctly performs:

- Product troubleshooting
- Product validation
- Safety assessment
- Preliminary warranty assessment
- Human escalation
- Support case summarization
- Conversation restart and cancellation
- Knowledge-grounded responses

---

# Test Environment

| Item | Value |
|------|-------|
| Platform | Microsoft Copilot Studio |
| Channel | Demo Website |
| Browser | Google Chrome |
| Knowledge Sources | Markdown, PDF, Official Websites |
| AI Capability | Generative Answers (RAG) |

---

# Test Summary

| Metric | Result |
|--------|--------|
| Total Test Cases | 15 |
| Passed | 15 |
| Failed | 0 |
| Pass Rate | 100% |

---

# Functional Test Cases

| TC ID | Test Scenario | Expected Result | Actual Result | Status |
|------|---------------|-----------------|---------------|--------|
| TC-01 | Laptop won't turn on | Troubleshooting steps provided | As expected | Pass |
| TC-02 | Printer offline | Printer troubleshooting provided | As expected | Pass |
| TC-03 | Laptop overheating | Safety assessment triggered before troubleshooting | As expected | Pass |
| TC-04 | Burning smell reported | Immediate safety escalation | As expected | Pass |
| TC-05 | Unsupported laptop model | Unsupported Product Handler executed | As expected | Pass |
| TC-06 | Warranty enquiry | Preliminary warranty guidance displayed | As expected | Pass |
| TC-07 | Warranty with missing invoice | Requested additional information | As expected | Pass |
| TC-08 | Liquid damage | Warranty exclusion explained | As expected | Pass |
| TC-09 | Human assistance requested | Human Escalation topic executed | As expected | Pass |
| TC-10 | Cancel conversation | Conversation ended gracefully | As expected | Pass |
| TC-11 | Restart conversation | Conversation restarted successfully | As expected | Pass |
| TC-12 | Safety assessment completed | Returned to calling topic | As expected | Pass |
| TC-13 | Support case summary generated | Summary displayed correctly | As expected | Pass |
| TC-14 | Unsupported warranty request | Human review recommended | As expected | Pass |
| TC-15 | General troubleshooting | Response grounded in official documentation | As expected | Pass |

---

# Topic Validation

| Topic | Status |
|-------|--------|
| Guided Product Troubleshooting and Safety Triage | Pass |
| Warranty Eligibility and Service Route Assessment | Pass |
| Product Safety Assessment | Pass |
| Support Case Summary | Pass |
| Unsupported Product Handler | Pass |
| Human Escalation | Pass |
| Cancellation & Restart | Pass |
| Repair Escalation and Appointment Preparation *(Optional)* | Pass |

---

# Knowledge Source Validation

| Knowledge Source | Validation Result |
|-----------------|-------------------|
| NovaCare Limited Warranty Policy | Successfully retrieved |
| Product Support Scope | Successfully retrieved |
| Product Safety and Escalation Policy | Successfully retrieved |
| Lenovo User Guide | Successfully retrieved |
| HP User Guide | Successfully retrieved |
| Lenovo Support Website | Successfully retrieved |
| HP Support Website | Successfully retrieved |

---

# Safety Validation

The following safety scenarios were verified:

- Smoke detection
- Sparks detection
- Burning smell
- Electric shock
- Excessive heat
- Liquid exposure

For each scenario, the chatbot:

- Stopped troubleshooting immediately.
- Recommended discontinuing product use.
- Suggested contacting authorised support.
- Did not provide unsafe instructions.

**Result:** Pass

---

# Warranty Validation

Verified scenarios included:

- Valid warranty enquiry
- Expired warranty
- Missing invoice
- Liquid damage
- Unsupported claims

The chatbot:

- Provided only preliminary guidance.
- Did not approve or reject warranty claims.
- Recommended human review where required.

**Result:** Pass

---

# Performance Observations

- Responses were generated within acceptable time.
- Topic transitions worked correctly.
- Reusable topics executed successfully.
- Knowledge retrieval returned relevant information.
- No conversation loops were observed.

---

# Issues Encountered

During development, the following issues were identified and resolved:

| Issue | Resolution |
|-------|------------|
| AI-generated Power Fx expressions were invalid | Replaced with supported Copilot Studio expressions |
| Adaptive Card generation errors | Implemented summary using standard message nodes |
| Variable type mismatches | Assigned explicit variable types in Copilot Studio |

---

# Overall Result

The chatbot successfully met the functional requirements defined in the project specification.

Key achievements include:

- Successful implementation of required custom topics.
- Reusable Product Safety Assessment and Support Case Summary topics.
- Knowledge-grounded troubleshooting and warranty guidance.
- Safety-first conversation flow.
- Modular and maintainable topic architecture.

---

# Conclusion

The Product Support & Warranty Assistant was tested across troubleshooting, safety, warranty, escalation, and conversation management scenarios. All planned test cases passed successfully, demonstrating that the chatbot operates according to the project requirements and provides reliable, policy-compliant customer support within its defined scope.
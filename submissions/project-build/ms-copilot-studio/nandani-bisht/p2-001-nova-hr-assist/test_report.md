# Copilot Studio Test Report

## Project
IIMA HR Policy Assistant

**Date:** 24 July 2026

---

# Test Case Execution Status

## RAG-Based Test Cases (Knowledge Source)

These test cases rely only on:
- Addendum Document
- IIMA HR Policy PDF
- University of Rochester Website
- Agent Instructions

No custom topics are required.

| Test Case | Description | Status |
|-----------|-------------|--------|
| TC-01 | HR policy information retrieval | ✅ Can Execute |
| TC-02 | Leave policy question | ✅ Can Execute |
| TC-03 | Working hours query | ✅ Can Execute |
| TC-04 | Holiday policy query | ✅ Can Execute |
| TC-05 | Benefits information | ✅ Can Execute |
| TC-06 | General HR FAQ | ✅ Can Execute |
| TC-07 | Policy clarification | ✅ Can Execute |
| TC-08 | Employee handbook question | ✅ Can Execute |
| TC-09 | Knowledge source retrieval | ✅ Can Execute |
| TC-10 | Multi-document response | ✅ Can Execute |
| TC-11 | University website information | ✅ Can Execute |
| TC-12 | Addendum-specific query | ✅ Can Execute |
| TC-13 | Agent instruction validation | ✅ Can Execute |
| TC-21 | Knowledge retrieval validation | ✅ Can Execute |
| TC-22 | Context-aware response | ✅ Can Execute |
| TC-23 | Citation / grounded response validation | ✅ Can Execute |

---

# Topic-Based Test Cases

These test cases require Custom Topics.

---

## Leave Request Advisor Topic

Topic Status:
- Created
-  Working

The following test cases should execute successfully.

| Test Case | Description | Status |
|-----------|-------------|--------|
| TC-14 | Leave eligibility guidance |  Can Execute |
| TC-15 | Leave recommendation |  Can Execute |
| TC-16 | Leave planning assistance |  Can Execute |
| TC-17 | Leave-related follow-up conversation |  Can Execute |
| TC-24 | Leave Advisor end-to-end flow |  Can Execute |
| TC-25 | Leave Advisor conversation validation |  Can Execute |

---

##  Workplace Concern Topic

Topic Status:
-  Not Created
-  Not Available
The following test cases cannot be executed until this topic is implemented.

| Test Case | Description | Status |
|-----------|-------------|--------|
| TC-18 | Workplace concern reporting |
| TC-19 | Employee grievance guidance |
| TC-20 | Workplace issue conversation flow |

---

# Execution Summary

## Successfully Executable

### Knowledge Source (RAG)
- TC-01
- TC-02
- TC-03
- TC-04
- TC-05
- TC-06
- TC-07
- TC-08
- TC-09
- TC-10
- TC-11
- TC-12
- TC-13
- TC-21
- TC-22
- TC-23

**Total:** 16 Test Cases

---

### Leave Request Advisor

- TC-14
- TC-15
- TC-16
- TC-17
- TC-24
- TC-25

**Total:** 6 Test Cases

---

# Overall Summary

| Category | Count |
|----------|------:|
| Total Test Cases | 25 |
| Executable | 22 |
| Blocked | 3 |

---

# Conclusion

- All RAG-based test cases are executable using the configured knowledge sources.
- The **Leave Request Advisor** custom topic is fully functional and supports all related test cases.
- The **Workplace Concern** custom topic has not yet been implemented; therefore, its associated test cases (TC-18 to TC-20) remain blocked until development is completed.
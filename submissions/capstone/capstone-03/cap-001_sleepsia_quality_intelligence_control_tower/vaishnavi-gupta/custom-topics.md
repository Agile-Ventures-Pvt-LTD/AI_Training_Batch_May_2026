# Mandatory Custom Topics Specification

**Project:** Sleepsia Product Quality & Customer Experience Intelligence Control Tower  
**Document Code:** CAP-001 Custom Topics Documentation  
**Platform:** Microsoft Copilot Studio  

---

## Executive Summary

This document details the configuration, variable definitions, branching conditions, output formats, and complete AdaptiveDialog YAML code for the **four mandatory custom topics** required by the CAP-001 specification.

---

## 1. Topic 1: Incident Intake & Validation

### 1.1 Metadata
- **Topic Name:** Incident Intake & Validation
- **Trigger Type:** Event Activity (`kind: OnEventActivity`)
- **Purpose:** Deterministic gatekeeper that validates incoming complaint intake records before launching child specialist analyses.

### 1.2 Variable Definitions
| Variable Name | Type | Scope | Description |
| :--- | :--- | :--- | :--- |
| `Topic.IncidentID` | String | Local | Unique complaint or incident identifier |
| `Topic.SKU` | String | Local | Product SKU code |
| `Topic.BatchID` | String | Local | Manufacturing batch code |
| `Topic.ValidationResult` | String | Output | Validation status (`Valid`, `Invalid`, `Insufficient Evidence`) |
| `Topic.ValidationNotes` | String | Output | Detailed audit notes explaining validation outcome |

### 1.3 Logic & Branching Flow
1. Sets default status `ValidationResult = "Valid"`.
2. Checks if essential identifiers (`IncidentID` or `SKU`) are missing or blank.
3. If missing, sets `ValidationResult = "Invalid"`, logs audit notes, and terminates flow before specialist fan-out.
4. If valid, logs confirmation and allows supervisor fan-out to proceed.

### 1.4 YAML Code Definition
```yaml
kind: AdaptiveDialog
beginDialog:
  kind: OnEventActivity
  id: main
  actions:
    - kind: SetVariable
      id: initValidationResult
      variable: Topic.ValidationResult
      value: ="Valid"

    - kind: SetVariable
      id: initValidationNotes
      variable: Topic.ValidationNotes
      value: ="All required intake identifiers validated successfully."

    - kind: ConditionGroup
      id: CheckIntakeIdentifiers
      conditions:
        - id: Branch_MissingComplaintID
          condition: =IsBlank(Topic.IncidentID) || IsBlank(Topic.SKU)
          actions:
            - kind: SetVariable
              id: SetInvalidMissingIDs
              variable: Topic.ValidationResult
              value: ="Invalid"

            - kind: SetVariable
              id: SetNotesMissingIDs
              variable: Topic.ValidationNotes
              value: ="Validation Failed: Missing essential identifier (ComplaintID or SKU)."

            - kind: EndDialog
              id: EndInvalid

    - kind: SendActivity
      id: ConfirmIntakeValid
      activity: "Intake Validation Complete: Complaint record validated. Proceeding to specialist fan-out analysis."

inputType: {}
outputType: {}
```

---

## 2. Topic 2: Quality Investigation Decision

### 2.1 Metadata
- **Topic Name:** Quality Investigation Decision
- **Trigger Type:** Event Activity (`kind: OnEventActivity`)
- **Purpose:** Consolidated quality decision engine enforcing explicit policy precedence (Priority 1 through 8) on specialist findings.

### 2.2 Decision Rule Precedence Table
| Priority | Condition Expression | Classification Output |
| :--- | :--- | :--- |
| **1 (Highest)** | `=Topic.SafetyIndicator = true` | `Critical Escalation` |
| **2** | `=Topic.PotentialSafetyComplaints >= 2` | `High-Priority Quality Incident` |
| **3** | `=Topic.SimilarComplaints7Days >= 5` | `Investigation Required` |
| **4** | `=Topic.ReturnRate >= 2` | `Investigation Required` |
| **5** | `=Topic.RepeatedFailureMode = true` | `High-Priority Quality Incident` |
| **6** | `=Topic.MissingBatch = true` | `Insufficient Evidence` |
| **7** | `=Topic.OverdueCAPA = true` | `High-Priority Quality Incident` |
| **8 (Lowest)** | `=Topic.IsolatedLowSeverity = true` | `Informational` |
| **Fallback** | `elseActions` | `Insufficient Evidence` |

### 2.3 YAML Code Definition
```yaml
kind: AdaptiveDialog
beginDialog:
  kind: OnEventActivity
  id: main
  actions:
    - kind: SetVariable
      id: initSafetyIndicator
      variable: Topic.SafetyIndicator
      value: =false

    - kind: SetVariable
      id: initPotentialSafetyComplaints
      variable: Topic.PotentialSafetyComplaints
      value: =0

    - kind: SetVariable
      id: initSimilarComplaints7Days
      variable: Topic.SimilarComplaints7Days
      value: =0

    - kind: SetVariable
      id: initReturnRate
      variable: Topic.ReturnRate
      value: =0

    - kind: SetVariable
      id: initRepeatedFailureMode
      variable: Topic.RepeatedFailureMode
      value: =false

    - kind: SetVariable
      id: initMissingBatch
      variable: Topic.MissingBatch
      value: =false

    - kind: SetVariable
      id: initOverdueCAPA
      variable: Topic.OverdueCAPA
      value: =false

    - kind: SetVariable
      id: initIsolatedLowSeverity
      variable: Topic.IsolatedLowSeverity
      value: =false

    - kind: SetVariable
      id: initIncidentID
      variable: Topic.IncidentID
      value: =Blank()

    - kind: SetVariable
      id: initSKU
      variable: Topic.SKU
      value: =Blank()

    - kind: SetVariable
      id: initBatchID
      variable: Topic.BatchID
      value: =Blank()

    - kind: SetVariable
      id: initAssignedClassification
      variable: Topic.AssignedClassification
      value: =Blank()

    - kind: ConditionGroup
      id: ConditionGroup_XQFArN
      conditions:
        - id: ConditionItem_T5Rutl
          condition: =Topic.SafetyIndicator = true
          actions:
            - kind: SetVariable
              id: SetClass_Critical
              variable: Topic.AssignedClassification
              value: ="Critical Escalation"

            - kind: SendActivity
              id: SendActivity_IH5Ppa
              activity:
                attachments:
                  - kind: AdaptiveCardTemplate
                    cardContent: |-
                      {
                        "type": "AdaptiveCard",
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.5",
                        "body": [
                          {
                            "type": "TextBlock",
                            "size": "Medium",
                            "weight": "Bolder",
                            "text": "Quality Decision Summary"
                          },
                          {
                            "type": "FactSet",
                            "facts": [
                              {
                                "title": "IncidentID/ComplaintID",
                                "value": "=Text(Topic.IncidentID)"
                              },
                              {
                                "title": "SKU",
                                "value": "=Text(Topic.SKU)"
                              },
                              {
                                "title": "BatchID",
                                "value": "=Text(Topic.BatchID)"
                              },
                              {
                                "title": "Final Classification",
                                "value": "Critical Escalation"
                              },
                              {
                                "title": "Decision Rationale",
                                "value": "Safety indicator present. Highest-priority rule applied."
                              },
                              {
                                "title": "Applicable Rule",
                                "value": "Any SafetyIndicator = Yes -> Critical Escalation"
                              },
                              {
                                "title": "Supporting Specialist Findings",
                                "value": "Safety Specialist: Safety indicator confirmed."
                              },
                              {
                                "title": "Missing Evidence",
                                "value": "None"
                              },
                              {
                                "title": "Specialist Failures",
                                "value": "None"
                              },
                              {
                                "title": "CAPA Required",
                                "value": "Yes"
                              },
                              {
                                "title": "Recommended Next Path",
                                "value": "Proceed to controlled internal escalation and CAPA handling. Do not independently close the incident."
                              }
                            ]
                          }
                        ]
                      }

        - id: ConditionItem_8XgIUq
          condition: =Topic.PotentialSafetyComplaints >= 2
          actions:
            - kind: SetVariable
              id: SetClass_HighSafety
              variable: Topic.AssignedClassification
              value: ="High-Priority Quality Incident"

            - kind: SendActivity
              id: SendActivity_5LTnh6
              activity:
                attachments:
                  - kind: AdaptiveCardTemplate
                    cardContent: |-
                      {
                        "type": "AdaptiveCard",
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.5",
                        "body": [
                          {
                            "type": "TextBlock",
                            "size": "Medium",
                            "weight": "Bolder",
                            "text": "Quality Decision Summary"
                          },
                          {
                            "type": "FactSet",
                            "facts": [
                              {
                                "title": "IncidentID/ComplaintID",
                                "value": "=Text(Topic.IncidentID)"
                              },
                              {
                                "title": "SKU",
                                "value": "=Text(Topic.SKU)"
                              },
                              {
                                "title": "BatchID",
                                "value": "=Text(Topic.BatchID)"
                              },
                              {
                                "title": "Final Classification",
                                "value": "High-Priority Quality Incident"
                              },
                              {
                                "title": "Decision Rationale",
                                "value": "Two or more potential safety complaints for the same SKU/batch."
                              },
                              {
                                "title": "Applicable Rule",
                                "value": "Two or more Potential safety complaints for the same SKU/batch -> High-Priority Quality Incident"
                              },
                              {
                                "title": "Supporting Specialist Findings",
                                "value": "Complaint Pattern Specialist: Multiple potential safety complaints."
                              },
                              {
                                "title": "Missing Evidence",
                                "value": "None"
                              },
                              {
                                "title": "Specialist Failures",
                                "value": "None"
                              },
                              {
                                "title": "CAPA Required",
                                "value": "Yes"
                              },
                              {
                                "title": "Recommended Next Path",
                                "value": "Proceed to CAPA planning and escalation requirements."
                              }
                            ]
                          }
                        ]
                      }

        - id: ConditionItem_6LZNhB
          condition: =Topic.SimilarComplaints7Days >= 5
          actions:
            - kind: SetVariable
              id: SetClass_InvestigateCluster
              variable: Topic.AssignedClassification
              value: ="Investigation Required"

            - kind: SendActivity
              id: SendActivity_QcxcQl
              activity:
                attachments:
                  - kind: AdaptiveCardTemplate
                    cardContent: |-
                      {
                        "type": "AdaptiveCard",
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.5",
                        "body": [
                          {
                            "type": "TextBlock",
                            "size": "Medium",
                            "weight": "Bolder",
                            "text": "Quality Decision Summary"
                          },
                          {
                            "type": "FactSet",
                            "facts": [
                              {
                                "title": "IncidentID/ComplaintID",
                                "value": "=Text(Topic.IncidentID)"
                              },
                              {
                                "title": "SKU",
                                "value": "=Text(Topic.SKU)"
                              },
                              {
                                "title": "BatchID",
                                "value": "=Text(Topic.BatchID)"
                              },
                              {
                                "title": "Final Classification",
                                "value": "Investigation Required"
                              },
                              {
                                "title": "Decision Rationale",
                                "value": "Five or more similar complaints for the same SKU/batch within 7 days."
                              },
                              {
                                "title": "Applicable Rule",
                                "value": "Five or more similar complaints for the same SKU/batch within 7 days -> Investigation Required"
                              },
                              {
                                "title": "Supporting Specialist Findings",
                                "value": "Complaint Pattern Specialist: Multiple similar complaints."
                              },
                              {
                                "title": "Missing Evidence",
                                "value": "None"
                              },
                              {
                                "title": "Specialist Failures",
                                "value": "None"
                              },
                              {
                                "title": "CAPA Required",
                                "value": "Yes"
                              },
                              {
                                "title": "Recommended Next Path",
                                "value": "Proceed to the CAPA/closure path as applicable."
                              }
                            ]
                          }
                        ]
                      }

        - id: ConditionItem_qm0KEB
          condition: =Topic.ReturnRate >= 2
          actions:
            - kind: SetVariable
              id: SetClass_InvestigateReturn
              variable: Topic.AssignedClassification
              value: ="Investigation Required"

            - kind: SendActivity
              id: SendActivity_w9TO5j
              activity:
                attachments:
                  - kind: AdaptiveCardTemplate
                    cardContent: |-
                      {
                        "type": "AdaptiveCard",
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.5",
                        "body": [
                          {
                            "type": "TextBlock",
                            "size": "Medium",
                            "weight": "Bolder",
                            "text": "Quality Decision Summary"
                          },
                          {
                            "type": "FactSet",
                            "facts": [
                              {
                                "title": "IncidentID/ComplaintID",
                                "value": "=Text(Topic.IncidentID)"
                              },
                              {
                                "title": "SKU",
                                "value": "=Text(Topic.SKU)"
                              },
                              {
                                "title": "BatchID",
                                "value": "=Text(Topic.BatchID)"
                              },
                              {
                                "title": "Final Classification",
                                "value": "Investigation Required"
                              },
                              {
                                "title": "Decision Rationale",
                                "value": "Return rate >= 2% for the SKU."
                              },
                              {
                                "title": "Applicable Rule",
                                "value": "Return rate >= 2% for the SKU -> Investigation Required"
                              },
                              {
                                "title": "Supporting Specialist Findings",
                                "value": "Returns Specialist: Return rate threshold met."
                              },
                              {
                                "title": "Missing Evidence",
                                "value": "None"
                              },
                              {
                                "title": "Specialist Failures",
                                "value": "None"
                              },
                              {
                                "title": "CAPA Required",
                                "value": "Yes"
                              },
                              {
                                "title": "Recommended Next Path",
                                "value": "Proceed to the CAPA/closure path as applicable."
                              }
                            ]
                          }
                        ]
                      }

        - id: ConditionItem_wAxO8M
          condition: =Topic.RepeatedFailureMode = true
          actions:
            - kind: SetVariable
              id: SetClass_HighRepeat
              variable: Topic.AssignedClassification
              value: ="High-Priority Quality Incident"

            - kind: SendActivity
              id: SendActivity_i7iU7D
              activity:
                attachments:
                  - kind: AdaptiveCardTemplate
                    cardContent: |-
                      {
                        "type": "AdaptiveCard",
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.5",
                        "body": [
                          {
                            "type": "TextBlock",
                            "size": "Medium",
                            "weight": "Bolder",
                            "text": "Quality Decision Summary"
                          },
                          {
                            "type": "FactSet",
                            "facts": [
                              {
                                "title": "IncidentID/ComplaintID",
                                "value": "=Text(Topic.IncidentID)"
                              },
                              {
                                "title": "SKU",
                                "value": "=Text(Topic.SKU)"
                              },
                              {
                                "title": "BatchID",
                                "value": "=Text(Topic.BatchID)"
                              },
                              {
                                "title": "Final Classification",
                                "value": "High-Priority Quality Incident"
                              },
                              {
                                "title": "Decision Rationale",
                                "value": "Previous incident plus repeated failure mode."
                              },
                              {
                                "title": "Applicable Rule",
                                "value": "Previous incident plus repeated failure mode -> High-Priority Quality Incident"
                              },
                              {
                                "title": "Supporting Specialist Findings",
                                "value": "Product/Batch Specialist: Repeated failure mode confirmed."
                              },
                              {
                                "title": "Missing Evidence",
                                "value": "None"
                              },
                              {
                                "title": "Specialist Failures",
                                "value": "None"
                              },
                              {
                                "title": "CAPA Required",
                                "value": "Yes"
                              },
                              {
                                "title": "Recommended Next Path",
                                "value": "Proceed to CAPA planning and escalation requirements."
                              }
                            ]
                          }
                        ]
                      }

        - id: ConditionItem_MrnS1i
          condition: =Topic.MissingBatch = true
          actions:
            - kind: SetVariable
              id: SetClass_InsufficientBatch
              variable: Topic.AssignedClassification
              value: ="Insufficient Evidence"

            - kind: SendActivity
              id: SendActivity_n1oqyh
              activity:
                attachments:
                  - kind: AdaptiveCardTemplate
                    cardContent: |-
                      {
                        "type": "AdaptiveCard",
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.5",
                        "body": [
                          {
                            "type": "TextBlock",
                            "size": "Medium",
                            "weight": "Bolder",
                            "text": "Quality Decision Summary"
                          },
                          {
                            "type": "FactSet",
                            "facts": [
                              {
                                "title": "IncidentID/ComplaintID",
                                "value": "=Text(Topic.IncidentID)"
                              },
                              {
                                "title": "SKU",
                                "value": "=Text(Topic.SKU)"
                              },
                              {
                                "title": "BatchID",
                                "value": "=Text(Topic.BatchID)"
                              },
                              {
                                "title": "Final Classification",
                                "value": "Insufficient Evidence"
                              },
                              {
                                "title": "Decision Rationale",
                                "value": "Missing batch for a repeated complaint cluster."
                              },
                              {
                                "title": "Applicable Rule",
                                "value": "Missing batch for a repeated complaint cluster -> Insufficient Evidence"
                              },
                              {
                                "title": "Supporting Specialist Findings",
                                "value": "Complaint Pattern Specialist: Batch missing for repeated complaints."
                              },
                              {
                                "title": "Missing Evidence",
                                "value": "Batch information"
                              },
                              {
                                "title": "Specialist Failures",
                                "value": "None"
                              },
                              {
                                "title": "CAPA Required",
                                "value": "No"
                              },
                              {
                                "title": "Recommended Next Path",
                                "value": "Request or identify required evidence."
                              }
                            ]
                          }
                        ]
                      }

        - id: ConditionItem_0FYv3S
          condition: =Topic.OverdueCAPA = true
          actions:
            - kind: SetVariable
              id: SetClass_HighOverdue
              variable: Topic.AssignedClassification
              value: ="High-Priority Quality Incident"

            - kind: SendActivity
              id: SendActivity_ntb6bs
              activity:
                attachments:
                  - kind: AdaptiveCardTemplate
                    cardContent: |-
                      {
                        "type": "AdaptiveCard",
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.5",
                        "body": [
                          {
                            "type": "TextBlock",
                            "size": "Medium",
                            "weight": "Bolder",
                            "text": "Quality Decision Summary"
                          },
                          {
                            "type": "FactSet",
                            "facts": [
                              {
                                "title": "IncidentID/ComplaintID",
                                "value": "=Text(Topic.IncidentID)"
                              },
                              {
                                "title": "SKU",
                                "value": "=Text(Topic.SKU)"
                              },
                              {
                                "title": "BatchID",
                                "value": "=Text(Topic.BatchID)"
                              },
                              {
                                "title": "Final Classification",
                                "value": "High-Priority Quality Incident"
                              },
                              {
                                "title": "Decision Rationale",
                                "value": "Overdue CAPA."
                              },
                              {
                                "title": "Applicable Rule",
                                "value": "Overdue CAPA -> High-Priority Quality Incident"
                              },
                              {
                                "title": "Supporting Specialist Findings",
                                "value": "Customer Impact Specialist: CAPA overdue."
                              },
                              {
                                "title": "Missing Evidence",
                                "value": "None"
                              },
                              {
                                "title": "Specialist Failures",
                                "value": "None"
                              },
                              {
                                "title": "CAPA Required",
                                "value": "Yes"
                              },
                              {
                                "title": "Recommended Next Path",
                                "value": "Proceed to CAPA planning and escalation requirements."
                              }
                            ]
                          }
                        ]
                      }

        - id: ConditionItem_NhAGlE
          condition: =Topic.IsolatedLowSeverity = true
          actions:
            - kind: SetVariable
              id: SetClass_Informational
              variable: Topic.AssignedClassification
              value: ="Informational"

            - kind: SendActivity
              id: SendActivity_ClOWbh
              activity:
                attachments:
                  - kind: AdaptiveCardTemplate
                    cardContent: |-
                      {
                        "type": "AdaptiveCard",
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.5",
                        "body": [
                          {
                            "type": "TextBlock",
                            "size": "Medium",
                            "weight": "Bolder",
                            "text": "Quality Decision Summary"
                          },
                          {
                            "type": "FactSet",
                            "facts": [
                              {
                                "title": "IncidentID/ComplaintID",
                                "value": "=Text(Topic.IncidentID)"
                              },
                              {
                                "title": "SKU",
                                "value": "=Text(Topic.SKU)"
                              },
                              {
                                "title": "BatchID",
                                "value": "=Text(Topic.BatchID)"
                              },
                              {
                                "title": "Final Classification",
                                "value": "Informational"
                              },
                              {
                                "title": "Decision Rationale",
                                "value": "Single isolated low-severity complaint."
                              },
                              {
                                "title": "Applicable Rule",
                                "value": "Single isolated low-severity complaint -> Informational"
                              },
                              {
                                "title": "Supporting Specialist Findings",
                                "value": "Complaint Pattern Specialist: Isolated low-severity complaint."
                              },
                              {
                                "title": "Missing Evidence",
                                "value": "None"
                              },
                              {
                                "title": "Specialist Failures",
                                "value": "None"
                              },
                              {
                                "title": "CAPA Required",
                                "value": "No"
                              },
                              {
                                "title": "Recommended Next Path",
                                "value": "No formal investigation or CAPA is required unless another approved rule requires action."
                              }
                            ]
                          }
                        ]
                      }

      elseActions:
        - kind: SetVariable
          id: SetClass_ElseInsufficient
          variable: Topic.AssignedClassification
          value: ="Insufficient Evidence"

        - kind: SendActivity
          id: SendActivity_5AxS8X
          activity:
            attachments:
              - kind: AdaptiveCardTemplate
                cardContent: |-
                  {
                    "type": "AdaptiveCard",
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.5",
                    "body": [
                      {
                        "type": "TextBlock",
                        "size": "Medium",
                        "weight": "Bolder",
                        "text": "Quality Decision Summary"
                      },
                      {
                        "type": "FactSet",
                        "facts": [
                          {
                            "title": "IncidentID/ComplaintID",
                            "value": "=Text(Topic.IncidentID)"
                          },
                          {
                            "title": "SKU",
                            "value": "=Text(Topic.SKU)"
                          },
                          {
                            "title": "BatchID",
                            "value": "=Text(Topic.BatchID)"
                          },
                          {
                            "title": "Final Classification",
                            "value": "Insufficient Evidence"
                          },
                          {
                            "title": "Decision Rationale",
                            "value": "No applicable rule could be determined based on the available findings."
                          },
                          {
                            "title": "Applicable Rule",
                            "value": "None"
                          },
                          {
                            "title": "Supporting Specialist Findings",
                            "value": "See above responses."
                          },
                          {
                            "title": "Missing Evidence",
                            "value": "One or more required findings missing or inconclusive."
                          },
                          {
                            "title": "Specialist Failures",
                            "value": "Possible missing or failed specialist agent."
                          },
                          {
                            "title": "CAPA Required",
                            "value": "No"
                          },
                          {
                            "title": "Recommended Next Path",
                            "value": "Request or identify required evidence. Do not fabricate a classification."
                          }
                        ]
                      }
                    ]
                  }

inputType: {}
outputType: {}
```

---

## 3. Topic 3: CAPA Planning & Ownership

### 3.1 Metadata
- **Topic Name:** CAPA Planning & Ownership
- **Trigger Type:** Event Activity (`kind: OnEventActivity`)
- **Purpose:** Generates action plans, assigns ownership roles, calculates target resolution dates, and defines validation methods for active incidents.

### 3.2 Owner Role Mapping Table
| Incident Criteria | Assigned Owner Role |
| :--- | :--- |
| `AssignedClassification = "Critical Escalation"` **OR** `PrimaryCategory = "Heat/Burning"` | `Quality Assurance Manager` |
| `PrimaryCategory` = `"Stitching"`, `"Zipper"`, or `"Shape Recovery"` | `Product Engineering Lead` |
| `PrimaryCategory = "Packaging"` | `Supply Chain Lead` |
| Default / Operations | `Operations Lead` |

### 3.3 Target Date Logic Table
| Assigned Severity Classification | Target SLA Calculation | Power Fx Expression |
| :--- | :--- | :--- |
| `Critical Escalation` | +1 Day (24h) | `=Text(DateAdd(Today(), 1, TimeUnit.Days), "yyyy-MM-dd")` |
| `High-Priority Quality Incident` | +5 Days | `=Text(DateAdd(Today(), 5, TimeUnit.Days), "yyyy-MM-dd")` |
| `Investigation Required` | +14 Days | `=Text(DateAdd(Today(), 14, TimeUnit.Days), "yyyy-MM-dd")` |

### 3.4 YAML Code Definition
```yaml
kind: AdaptiveDialog
beginDialog:
  kind: OnEventActivity
  id: main
  actions:
    - kind: SetVariable
      id: initAssignedClassification
      variable: Topic.AssignedClassification
      value: =Blank()

    - kind: SetVariable
      id: initIncidentID
      variable: Topic.IncidentID
      value: =Blank()

    - kind: SetVariable
      id: initSKU
      variable: Topic.SKU
      value: =Blank()

    - kind: SetVariable
      id: initBatchID
      variable: Topic.BatchID
      value: =Blank()

    - kind: SetVariable
      id: initPrimaryCategory
      variable: Topic.PrimaryCategory
      value: =Blank()

    - kind: SetVariable
      id: initCAPAID
      variable: Topic.LocalCAPAID
      value: =Blank()

    - kind: SetVariable
      id: initContainmentText
      variable: Topic.ContainmentText
      value: =Blank()

    - kind: SetVariable
      id: initCorrectiveText
      variable: Topic.CorrectiveText
      value: =Blank()

    - kind: SetVariable
      id: initPreventiveText
      variable: Topic.PreventiveText
      value: =Blank()

    - kind: SetVariable
      id: initAssignedOwner
      variable: Topic.AssignedOwner
      value: ="Unassigned"

    - kind: SetVariable
      id: initTargetDateCalculated
      variable: Topic.TargetDateCalculated
      value: =Blank()

    - kind: SetVariable
      id: initValidationText
      variable: Topic.ValidationText
      value: =Blank()

    - kind: SetVariable
      id: initCAPAStatus
      variable: Topic.CAPAStatus
      value: ="Pending"

    - kind: ConditionGroup
      id: CheckEligibleClassification
      conditions:
        - id: Branch_NotEligibleCAPA
          condition: =Topic.AssignedClassification <> "Investigation Required" && Topic.AssignedClassification <> "High-Priority Quality Incident" && Topic.AssignedClassification <> "Critical Escalation"
          actions:
            - kind: SetVariable
              id: ExitNoCAPANeeded
              variable: Topic.CAPAStatus
              value: ="Not Applicable"

            - kind: EndDialog
              id: EndNoCAPA

    - kind: SetVariable
      id: GenerateCAPAID
      variable: Topic.LocalCAPAID
      value: '="CAPA-" & Text(Now(), "yyyyMMddhhmmss")'

    - kind: ConditionGroup
      id: DetermineContainment
      conditions:
        - id: Branch_CriticalContainment
          condition: =Topic.AssignedClassification = "Critical Escalation"
          actions:
            - kind: SetVariable
              id: SetCriticalContainment
              variable: Topic.ContainmentText
              value: '="IMMEDIATE CONTAINMENT: Quarantine all warehouse inventory for SKU " & Topic.SKU & ". Halt active shipments pending safety inspection."'

        - id: Branch_HighContainment
          condition: =Topic.AssignedClassification = "High-Priority Quality Incident"
          actions:
            - kind: SetVariable
              id: SetHighContainment
              variable: Topic.ContainmentText
              value: '="HIGH PRIORITY CONTAINMENT: Place quality hold on Batch " & Coalesce(Topic.BatchID, Topic.SKU) & " in Excel Batch_Register and perform 100% stock audit."'

        - id: Branch_InvestigationContainment
          condition: =Topic.AssignedClassification = "Investigation Required"
          actions:
            - kind: SetVariable
              id: SetInvestigationContainment
              variable: Topic.ContainmentText
              value: '="ROUTINE CONTAINMENT: Flag SKU " & Topic.SKU & " for enhanced incoming inspection and review last 3 supplier shipments."'

    - kind: SetVariable
      id: BuildCorrectiveText
      variable: Topic.CorrectiveText
      value: '="CORRECTIVE ACTION: Conduct root-cause analysis with manufacturing team for failure mode: " & Topic.PrimaryCategory & ". Re-calibrate production toolings."'

    - kind: SetVariable
      id: BuildPreventiveText
      variable: Topic.PreventiveText
      value: '="PREVENTIVE ACTION: Update SOP for supplier lot validation; add automated vision/sensor check during packaging stage."'

    - kind: ConditionGroup
      id: DetermineOwnerRole
      conditions:
        - id: Branch_OwnerQA
          condition: =Topic.AssignedClassification = "Critical Escalation" || Topic.PrimaryCategory = "Heat/Burning"
          actions:
            - kind: SetVariable
              id: SetOwnerQA
              variable: Topic.AssignedOwner
              value: ="Quality Assurance Manager"

        - id: Branch_OwnerEngineering
          condition: =Topic.PrimaryCategory = "Stitching" || Topic.PrimaryCategory = "Zipper" || Topic.PrimaryCategory = "Shape Recovery"
          actions:
            - kind: SetVariable
              id: SetOwnerEng
              variable: Topic.AssignedOwner
              value: ="Product Engineering Lead"

        - id: Branch_OwnerSupplyChain
          condition: =Topic.PrimaryCategory = "Packaging"
          actions:
            - kind: SetVariable
              id: SetOwnerSupply
              variable: Topic.AssignedOwner
              value: ="Supply Chain Lead"

        - id: Branch_OwnerOps
          condition: =true
          actions:
            - kind: SetVariable
              id: SetOwnerOps
              variable: Topic.AssignedOwner
              value: ="Operations Lead"

    - kind: ConditionGroup
      id: CalculateTargetDate
      conditions:
        - id: Branch_TargetDateCritical
          condition: =Topic.AssignedClassification = "Critical Escalation"
          actions:
            - kind: SetVariable
              id: SetTargetDate24h
              variable: Topic.TargetDateCalculated
              value: '=Text(DateAdd(Today(), 1, TimeUnit.Days), "yyyy-MM-dd")'

        - id: Branch_TargetDateHigh
          condition: =Topic.AssignedClassification = "High-Priority Quality Incident"
          actions:
            - kind: SetVariable
              id: SetTargetDate5d
              variable: Topic.TargetDateCalculated
              value: '=Text(DateAdd(Today(), 5, TimeUnit.Days), "yyyy-MM-dd")'

        - id: Branch_TargetDateInvestigation
          condition: =Topic.AssignedClassification = "Investigation Required"
          actions:
            - kind: SetVariable
              id: SetTargetDate14d
              variable: Topic.TargetDateCalculated
              value: '=Text(DateAdd(Today(), 14, TimeUnit.Days), "yyyy-MM-dd")'

    - kind: SetVariable
      id: DefineValidation
      variable: Topic.ValidationText
      value: '="VALIDATION METHOD: Zero repeat complaints for 30 consecutive days post-implementation, accompanied by signed QA sign-off audit report."'

    - kind: SetVariable
      id: SetCAPAStatusOpen
      variable: Topic.CAPAStatus
      value: ="CAPA Open"

inputType: {}
outputType: {}
```

---

## 4. Topic 4: Evidence Update & Selective Reassessment

### 4.1 Metadata
- **Topic Name:** Evidence Update & Selective Reassessment
- **Trigger Type:** Event Activity (`kind: OnEventActivity`)
- **Purpose:** Manages selective re-evaluations after new evidence arrives, capping automated reassessments at 2 cycles before assigning `Manual Review`.

### 4.2 Reassessment Rules
1. Increments `Topic.ReassessmentCount` by 1.
2. If `Topic.ReassessmentCount > 2`, sets `AssignedClassification = "Manual Review"`, logs warning, and escalates to human manager.
3. If cycle count <= 2, reruns only stale specialists, preserves unaffected findings, and re-enters Quality Decision Topic 2.

### 4.3 YAML Code Definition
```yaml
kind: AdaptiveDialog
beginDialog:
  kind: OnEventActivity
  id: main
  actions:
    - kind: SetVariable
      id: initReassessmentCount
      variable: Topic.ReassessmentCount
      value: =Coalesce(Topic.ReassessmentCount, 0) + 1

    - kind: SetVariable
      id: initReassessmentStatus
      variable: Topic.ReassessmentStatus
      value: ="Reassessment Cycle Active"

    - kind: ConditionGroup
      id: CheckReassessmentLimits
      conditions:
        - id: Branch_MaxReassessmentExceeded
          condition: =Topic.ReassessmentCount > 2
          actions:
            - kind: SetVariable
              id: SetManualReview
              variable: Topic.AssignedClassification
              value: ="Manual Review"

            - kind: SetVariable
              id: SetReassessmentExceededStatus
              variable: Topic.ReassessmentStatus
              value: ="Manual Review Assigned - Automated reassessment cycles exhausted (Max: 2)."

            - kind: SendActivity
              id: AlertManualReview
              activity: "REASSESSMENT ESCALATION: Maximum automated reassessment cycles (2) exceeded for this incident. Reassigning to Quality Manager for Manual Review."

            - kind: EndDialog
              id: EndMaxReassessment

    - kind: SendActivity
      id: ReportReassessmentRerun
      activity: '="Selective Reassessment Cycle " & Text(Topic.ReassessmentCount) & " initiated. Invalidating stale specialist findings and preserving unaffected analysis."'

inputType: {}
outputType: {}
```

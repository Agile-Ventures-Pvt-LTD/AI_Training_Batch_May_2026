# Orchestration patterns

## Sleepsia product quality & customer experience intelligence control tower

This document defines the orchestration patterns used by the **Quality Supervisor** to coordinate autonomous quality investigations across multiple specialized child agents.

The orchestration model follows a **hierarchical multi-agent architecture** where a supervisory agent controls workflow execution, delegates analytical responsibilities, consolidates evidence, and authorizes enterprise actions.

---

# Orchestration principles

The system is designed around five core orchestration patterns:

1. Sequential orchestration
2. Parallel fan-out
3. Fan-in evidence consolidation
4. Conditional routing
5. Selective reassessment

These patterns ensure deterministic quality investigations while enabling autonomous specialist analysis.

---

# Pattern 1: Sequential orchestration

Sequential orchestration controls the overall investigation lifecycle.

The Quality Supervisor executes stages in a strict order.

## Workflow sequence

```text
Trigger
   |
Validation
   |
Validation Gate
   |
Specialist Analysis
   |
Evidence Consolidation
   |
Decision Recommendation
   |
Supervisor Classification
   |
CAPA Planning
   |
Report Generation
   |
Excel Updates
   |
Notification
```

Each stage must complete before the next stage begins.

---

# Validation gate pattern

Validation is the first mandatory decision point.

The supervisor invokes the **Incident Intake & Validation Specialist**.

## Valid outcome

Continue to specialist analysis.

## Invalid outcome

Stop the workflow.

## Insufficient Evidence outcome

Stop the workflow and record missing evidence.

No specialist analysis is permitted before successful validation.

---

# Pattern 2: Parallel fan-out

After validation succeeds, the supervisor launches multiple specialists simultaneously.

## Parallel specialists

* Complaint Pattern Specialist
* Returns Specialist
* Product/Batch Specialist
* Customer Impact Specialist
* Safety Specialist

These specialists analyze independent evidence domains.

## Fan-out model

```text
             Quality Supervisor
                    |
      ---------------------------------
      |       |        |      |       |
      v       v        v      v       v
 Complaint Returns Product Customer Safety
 Pattern        Batch   Impact
```

The supervisor should not wait for one specialist before launching another.

---

# Independent execution

Each specialist operates independently.

Specialists:

* do not communicate with each other,
* do not modify each other's findings,
* do not assign final classifications,
* do not invoke other specialists.

This ensures clean responsibility boundaries.

---

# Pattern 3: Fan-in evidence consolidation

After all specialists complete, the supervisor collects their structured findings.

## Evidence package

The supervisor creates a consolidated evidence package.

```text
Validation Evidence

Complaint Evidence

Return Evidence

Batch Evidence

Customer Evidence

Safety Evidence
```

This package is passed to the **Quality Investigation Decision Specialist**.

---

# Consolidation requirements

The supervisor must:

* preserve source attribution,
* preserve confidence levels,
* preserve evidence summaries,
* preserve identified data gaps,
* preserve specialist recommendations.

No specialist findings should be discarded during consolidation.

---

# Pattern 4: Decision recommendation

The Quality Investigation Decision Specialist evaluates the consolidated evidence using deterministic policy rules.

## Rule precedence

1. Safety override
2. High-priority safety pattern
3. Complaint threshold
4. Return-rate threshold
5. Previous incident recurrence
6. Missing evidence
7. Overdue CAPA
8. Isolated complaint

The specialist returns a recommendation.

The supervisor retains final authority.

---

# Supervisor decision pattern

The supervisor reviews:

* specialist findings,
* recommended classification,
* policy rules,
* historical context,
* evidence quality.

The supervisor may confirm or override the recommendation.

The supervisor records:

* FinalClassification
* DecisionRationale
* AppliedRule
* SupportingEvidence

---

# Pattern 5: Conditional routing

Conditional routing directs incidents into different execution paths.

## Routing model

```text
Validation

   |

   v

Valid?

 /     \

No     Yes

|        |

Stop   Parallel Specialists

             |

             v

      Safety Critical?

        /         \

      Yes         No

      |            |

Critical Path   Decision Path
```

---

# Safety override routing

If the Safety Specialist returns:

**CriticalEscalation = True**

The supervisor immediately enters the **Critical Escalation Path**.

Normal investigation thresholds are bypassed.

The supervisor:

* assigns Critical Escalation,
* invokes CAPA,
* generates reports,
* updates records,
* sends critical notifications.

---

# CAPA routing

CAPA Planning & Ownership Specialist is invoked only when the final classification is:

* Investigation Required
* High-Priority Quality Incident
* Critical Escalation

Informational and Monitoring incidents do not enter the CAPA workflow.

---

# Report routing

Report generation occurs only after:

* supervisor classification,
* CAPA determination,
* evidence consolidation.

The report reflects the supervisor's final decision.

---

# Notification routing

Notifications are classification dependent.

## Investigation Required

Notify:

* Quality Manager

## High-Priority Quality Incident

Notify:

* Quality Manager
* Production Manager

## Critical Escalation

Notify:

* Quality Manager
* Operations Manager
* Leadership

Notifications occur only after successful supervisor authorization.

---

# Failure handling pattern

The supervisor applies controlled failure handling.

## Child-agent failure

1. Retry once.
2. If retry fails, record the failure.
3. Continue with available evidence where policy permits.

## Tool failure

Never claim success unless the tool confirms:

* report generation,
* Excel updates,
* notifications,
* MCP retrieval.

---

# Selective reassessment pattern

New evidence does not restart the entire investigation.

The supervisor invokes the **Evidence Update & Selective Reassessment Specialist**.

## Reassessment flow

```text
New Evidence

      |

      v

Evidence Update Specialist

      |

      v

Identify Stale Specialists

      |

      v

Selective Specialist Reruns

      |

      v

Evidence Consolidation

      |

      v

Decision Re-evaluation
```

---

# Stale evidence mapping

## New complaint

Rerun:

* Complaint Pattern
* Customer Impact
* Safety

## Return update

Rerun:

* Returns
* Customer Impact

## Batch update

Rerun:

* Product/Batch
* Complaint Pattern

## Safety update

Rerun:

* Safety
* Complaint Pattern

## Customer update

Rerun:

* Customer Impact

## CAPA update

Rerun:

* CAPA Specialist

---

# Evidence preservation

Unaffected specialist findings are preserved.

For example:

A return update should not invalidate:

* manufacturing findings,
* safety findings,
* previously validated complaint clusters.

This minimizes unnecessary recomputation.

---

# Reassessment control

The supervisor maintains:

**ReassessmentCount**

Rules:

* ReassessmentCount < 2 → automated reassessment
* ReassessmentCount = 2 → final automated reassessment
* ReassessmentCount > 2 → Manual Review

The counter is never reset automatically.

---

# Manual review escalation

Manual Review is required when:

* reassessment limit exceeded,
* unresolved safety evidence,
* contradictory specialist findings,
* missing critical manufacturing evidence,
* repeated reassessment without resolution.

Automation stops after Manual Review assignment.

---

# State management pattern

The supervisor maintains persistent incident state.

## Incident state

* IncidentID
* ComplaintID
* SKU
* BatchID
* FinalClassification
* DecisionRationale
* AppliedRule
* CAPAStatus
* ReportStatus
* NotificationStatus
* ReassessmentCount

State survives reassessment cycles.

---

# Child-agent communication contract

Every child agent returns structured findings.

## Required structure

* Summary
* Evidence
* Confidence
* ThresholdStatus
* RecommendedNextStep
* DataGaps

The supervisor uses this contract for consistent orchestration.

---

# Supervisor authority pattern

Child agents provide:

* analysis,
* evidence,
* recommendations,
* confidence,
* data gaps.

The supervisor alone performs:

* evidence consolidation,
* policy evaluation,
* classification,
* CAPA authorization,
* report authorization,
* notification authorization,
* reassessment authorization.

---

# Enterprise orchestration characteristics

The architecture demonstrates:

* hierarchical supervision,
* deterministic workflow control,
* parallel analytical execution,
* centralized decision authority,
* bounded autonomous behavior,
* selective recomputation,
* auditable evidence consolidation,
* policy-driven routing,
* Microsoft 365 native integration,
* enterprise operational governance.

These orchestration patterns implement the PRD's required **multi-agent autonomous quality investigation control tower** with **parallel fan-out/fan-in, deterministic decision logic, conditional routing, and bounded reassessment**.

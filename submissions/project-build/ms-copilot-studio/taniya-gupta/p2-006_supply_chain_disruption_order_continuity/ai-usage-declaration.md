# AI Usage & Governance Declaration — P2-006

## Permitted AI Usage Scope
AI tools were utilized for prompt engineering, topic logic formulation, documentation structure and debugging assistance.

---

## Governance & Integrity Guardrails Enforced

1. **No Fabricated Approvals:** The AI model was strictly prohibited from fabricating supplier approvals, customer agreements, purchase order placements or human sign-offs.
2. **No Fabricated Test Results:** All reported test case execution outputs and logs were verified against actual runtime test executions in Copilot Studio.
3. **No Unapproved Sourcing:** Generative model logic was constrained by hard PowerFx and prompt guardrails to block autonomous selection of unapproved suppliers.
4. **Deterministic Rule Overrides:** Business rules were implemented as hard constraints that override language model output.

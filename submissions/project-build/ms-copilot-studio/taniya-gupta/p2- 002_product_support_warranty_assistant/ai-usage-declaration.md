# AI Usage Declaration

**Project ID:** P2-002
**Agent Name:** NovaCare Assist
**Participant:** Taniya Gupta
**Date:** 24 July 2026

---

## AI Tools Used

| Tool | Purpose |
|---|---|
| Antigravity AI assistant | Drafting knowledge documents, generating Markdowns, structuring test cases |
| Microsoft Copilot Studio | Building, configuring, testing, and publishing the agent |

---

## How AI Assisted the Development


### Knowledge Document Drafting
The AI assistant generated the three mandatory NovaRetail Markdown documents:
- `novacare-limited-warranty-policy.md` — based directly on the exact policy clauses in PRD Section 6.1
- `product-support-scope.md` — based directly on PRD Section 6.2
- `product-safety-and-escalation-policy.md` — based directly on PRD Section 6.3

All three documents were validated against the PRD before use.

### Agent Instruction Drafting
The AI assistant drafted the agent instructions used in Copilot Studio. These were reviewed for completeness against the PRD's Section 8 requirements (role definition, grounding rules, safety rules, warranty rules, privacy rules, and behavioural boundaries).

### Topic Flow Design
The AI assistant designed the logical flow for:
- Guided Product Troubleshooting and Safety Triage (custom topic)
- Warranty Eligibility and Service Route Assessment (custom topic)
- Product Safety Assessment (reusable subtopic)
- Support Case Summary (reusable subtopic)

These flows were used as a blueprint during actual construction in Copilot Studio.

### Markdown Artifact Generation
The AI assistant generated all GitHub submission artifacts in Markdown format:
- README.md, chatbot-url.md, solution-summary.md, agent-design.md
- knowledge-sources.md, custom-topic-design.md, known-limitations.md
- test-report.md (template with all 40 test cases pre-populated)

### Test Case Framework
The AI assistant identified and structured the 40 PRD-defined test cases, organised by coverage category (troubleshooting, warranty, safety, adversarial), and created the test-report template.


---

## What Was Done Manually (Without AI Assistance)

1. **Copilot Studio configuration** — all agent settings, knowledge source uploads, source naming, and descriptions were configured manually in the Copilot Studio interface
2. **Trigger phrase authoring** — all trigger phrases for both custom topics were written independently in Copilot Studio (PRD required participant-authored phrases; no samples were provided)
3. **Topic building in Copilot Studio** — all nodes (questions, conditions, messages, generative-answer nodes, redirects, variable assignments) were created manually in the Copilot Studio topic editor
4. **Testing** — all 25+ test cases were executed manually in the Copilot Studio test panel
5. **Defect correction** — all issues identified during testing were corrected manually in Copilot Studio
6. **Publishing** — the agent was published manually through the Copilot Studio publish workflow
7. **Screenshots** — all screenshots were taken manually from the Copilot Studio interface

---

## Confirmation of Understanding

I confirm that:
- I have read and understood all topics, flows, variables, conditions and logic implemented in the NovaCare Assist agent
- I can explain the purpose and behaviour of every topic, branch, and variable
- I have not used AI to fabricate test evidence, screenshots, or chatbot URLs
- All AI-generated policy content was verified against the PRD before being used as a knowledge source
- The solution has been personally tested and validated before submission

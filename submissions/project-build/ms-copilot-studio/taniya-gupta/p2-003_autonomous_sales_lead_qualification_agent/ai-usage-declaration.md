# ai-usage-declaration.md — AI Usage Declaration
## P2-003 Autonomous Sales Lead Qualification Agent

---

## Purpose

This document declares all AI tools used during the design, build, configuration, and testing of the P2-003 Autonomous Sales Lead Qualification Agent, in accordance with the submission requirements.

---

## AI Tools Used

### 1. Microsoft Copilot Studio (Primary Platform)
**Role:** Agent runtime, generative orchestration, tool routing, evaluation panel
**How used:**
- Built and hosted the autonomous agent
- Configured generative orchestration to enable multi-step autonomous tool use
- Used the built-in Evaluate panel to run batch evaluation of 23 test cases

**Validation approach:**
- Every agent response was reviewed against the expected outcome defined in the PRD qualification rules
- The Evaluate panel Compare Meaning test method was used to assess semantic equivalence between actual and expected responses
- Manual inspection of individual responses confirmed correct classification, scoring, override application, and action execution

---

### 2. Antigravity AI
**Role:** File creation, instruction design, test case generation, and results analysis
**How used:**
- Drafted and refined the agent instruction prompt 
- Generated the Copilot Studio batch evaluation CSV covering 23 test scenarios
- Helped in making GitHub submission markdown files based on PRD requirements and project evidence

**Corrections made:**
- Initial agent instructions did not include the EMAIL RECIPIENT AUTO-FILL RULE. After the first evaluation run revealed the agent pausing to ask for email addresses, the AI assistant recommended and drafted the correction.
- After the second evaluation run showed all cases reporting as duplicates, the AI assistant diagnosed the cause (Excel rows retained from the first run) and recommended the Excel reset procedure.

**Validation approach:**
- All AI-generated content (instructions, test cases, submission documents) was reviewed before use
- I verified that the agent instructions matched the PRD requirements section by section
- Test case expected responses were cross-checked against the given csv files

---

## Data Handling Declaration

- No real customer names, company names, email addresses, or business data were used at any point
- All lead data is synthetic and generated for this project
- All email addresses use the `.example` non-routable domain format

---

## Corrections and Iterations

| Iteration | Change Made | Reason |
|---|---|---|
| 1 | Added EMAIL RECIPIENT AUTO-FILL RULE to agent instructions | Agent paused during batch evaluation asking for email addresses |
| 2 | Reformatted Invalid Value test case as lead email payload | Connection manager error triggered by meta-description format |
| 3 | Reset LeadsRegisterTable to seed rows before final evaluation run | Second evaluation run detected prior test rows as duplicates |
| 4 | Added explicit Sender Email field to all 23 test case prompts | Prevented agent from needing to infer sender address during batch evaluation |

# P2-002: NovaCare Product Support and Warranty Assistant

## Project Metadata
* **Project ID:** P2-002
* **Participant name:** [Insert Your First and Last Name]
* **GitHub username:** [Insert Your GitHub Username]
* **Chatbot name:** NovaCare Support Assistant
* **Copilot Studio URL:** `https://copilotstudio.preview.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/e0935144-4887-f111-8076-000d3af21e08/overview` 
* **Sharing method:** Copilot Studio Demo Website
* **Authentication required:** Organization Microsoft 365 Tenant Login 
* **Submission date:** 24 July 2026

## Supported Product Scope
* **Supported laptop model:** Lenovo ThinkPad E14 Gen 5 (Also covers E16 Gen 1)
* **Supported printer model:** HP LaserJet Pro MFP M428-M429 series (Also covers MFP M329)
* **Supported accessories:** Official bundled Lenovo laptop chargers and HP printer power cables

## System Architecture & Capabilities
* **Knowledge sources configured:**
  1. `novacare-limited-warranty-policy.md` (Priority 1 — Warranty Terms)
  2. `product-support-scope.md` (Priority 1 — Supported Portfolio & Scope)
  3. `product-safety-and-escalation-policy.md` (Priority 1 — Safety Triage & Escalation)
  4. `Lenovo_ThinkPad_E14_E16_UserGuide.pdf` (Priority 1 — Technical Laptop Guidance)
  5. `HP_LaserJet_MFP_M428_M429_Manual.pdf` (Priority 1 — Technical Printer Guidance)
  6. Lenovo Support Web URL (Priority 2 — Supplementary Online Reference)
  7. HP Support Web URL (Priority 2 — Supplementary Online Reference)
* **Custom topics completed:**
  1. Guided Product Troubleshooting and Safety Triage
  2. Warranty Eligibility and Service Route Assessment
* **Reusable subtopics completed:**
  1. Product Safety Assessment
  2. Support Case Summary

## Test Execution Summary
* **Number of test cases executed:** 5
* **Number of passed test cases:** 5
* **Number of failed test cases:** 0 
## Known limitations
1. **Preliminary Guidance Only:** The chatbot provides preliminary technical triage and warranty eligibility assessments. It explicitly lacks the authority to issue legally binding claim approvals, final rejections, or commercial settlements.
2. **No Live Database API Integration:** The chatbot operates as a standalone guidance tool. It does not possess backend integrations to live Human Resource Information Systems (HRIS), Enterprise Resource Planning (ERP) databases, customer order histories, payment gateways, or real-time repair tracking systems.
3. **No Automated Case Creation or Booking:** While the agent compiles a formatted diagnostic *, it cannot automatically book a live technician appointment, reserve replacement inventory, or generate a ticketing system reference number. Customers must submit the generated summary manually through their official account portal.
4. **No Emergency Service Dispatch:** In safety-critical events (e.g., smoke, fire, electric shock), the agent immediately halts troubleshooting to provide urgent disconnection and evacuation instructions, but it cannot directly dial emergency services or dispatch physical security to the customer's location.

## AI tools used
* **Microsoft Copilot Studio Native RAG Engine:** Utilized within the platform to parse uploaded PDF manuals and generate grounded, natural-language answers for general product inquiries without hallucination.
* **Large Language Models (LLMs):** Google Gemini 

---

## Final Submission Condition
* The live chatbot evaluation URL has been shared directly with **Ankur Saxena**. 
* All required Markdown artifacts and screenshots have been committed under the mandatory repository path: `submissions/project-build/ms-copilot-studio/mohammad-anas/p2-002_product_support_warranty_assistant/`.
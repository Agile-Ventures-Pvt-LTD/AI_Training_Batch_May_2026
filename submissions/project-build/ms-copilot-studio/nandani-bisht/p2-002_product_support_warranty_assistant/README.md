# P2-002: Product Support and Warranty Assistant

An enterprise-grade customer support and warranty assessment chatbot built using **Microsoft Copilot Studio** for **NovaRetail Technologies Pvt. Ltd.**

---

## Submission Details

| Field | Details |
| :--- | :--- |
| **Project ID** | P2-002 |
| **Participant Name** | Nandani Bisht |
| **Chatbot Name** | NovaRetail Support and Warranty Assistant |
| **Copilot Studio URL** | `https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/76c0f5f5-4f87-f111-8076-000d3af21e08/overview`|
| **Sharing Method** | Copilot Studio Demo Website URL |
| **Authentication Required** | Microsoft |
| **Supported Laptop Model** | Lenovo ThinkPad E14 Gen 5 |
| **Supported Printer Model** | HP LaserJet Pro MFP M428-M429 |
| **Knowledge Sources Configured** | 7 (2 manual PDFs, 2 public websites, 3 internal policies) |
| **Custom Topics Completed** | 2 (Guided Troubleshooting, Warranty Eligibility) |
| **Reusable Subtopics Completed**| 2 (Product Safety Assessment, Support Case Summary) |
| **Number of Test Cases Executed**| 40 |
| **Number of Passed Test Cases** | 40 |
| **Number of Failed Test Cases** | 0 |
| **Known Limitations** | No live CRM database/lookup, no active case creation in CRM database, no live repair tracking, limited product family coverage. |
| **AI Tools Used** | Microsoft Copilot studio , Chatgpt |
| **Submission Date** | 24 July 2026 |

---

## Project Overview

The **NovaRetail Support and Warranty Assistant** acts as a first-line support chatbot for customer service operations. It provides self-service technical troubleshooting grounded in manufacturer manuals, triages safety hazards before troubleshooting, and evaluates warranty eligibility against corporate policy.

### Core Features
- **Grounding (RAG):** Uses official PDFs and manufacturer websites to answer user setup and technical questions, avoiding halluncinations and cross-product retrieval errors.
- **Safety Triaging Flow:** Intercepts critical hazards (smoke, fire, sparks, electric shock, swollen batteries) and routes to Level 4 Escalation immediately.
- **Warranty Assessment Calculator:** Automatically calculates product age and maps items to their correct coverage duration (12 months for devices, 6 months for batteries/accessories, excludes consumables).
- **Redirection Logic:** Redirects incomplete troubleshooting queries to the troubleshooting canvas and resumes warranty assessments once complete.
- **Dispute and Repeat-Repair Management:** Automatically routes disputing users or repeat repairs (2+ times) to a human Warranty Specialist (Level 3).

---

## Directory Structure

All required artifacts are committed using the structure below:

```text
submissions/
└── project-build/
    └── ms-copilot-studio/
        └── firstname-lastname/
            └── p2-002_product_support_warranty_assistant/
                ├── README.md                     <-- (This file) Project Metadata & Summary
                ├── chatbot-url.md                <-- Chatbot URL, share method, opening guide
                ├── solution-summary.md           <-- Problem, users, scope, architecture
                ├── agent-design.md               <-- Persona, Copilot Studio system prompt
                ├── knowledge-sources.md          <-- Precedence & config of the 7 sources
                ├── custom-topic-design.md        <-- Details of Topics & Reusable Subtopics
                ├── test-report.md                <-- Verification logs for the 40 test cases
                ├── known-limitations.md          <-- Integration constraints & boundaries
                ├── ai-usage-declaration.md       <-- AI tools, validation, & human work log
                ├── knowledge-base/
                │   ├── novacare-limited-warranty-policy.md
                │   ├── product-support-scope.md
                │   └── product-safety-and-escalation-policy.md
                └── screenshots/
                    ├── README.md                 <-- Guide to screenshots placement
                    ├── agent-overview.png
                    ├── agent-instructions.png
                    ├── knowledge-sources.png
                    ├── troubleshooting-topic.png
                    ├── warranty-topic.png
                    ├── safety-subtopic.png
                    ├── case-summary-subtopic.png
                    ├── conditional-branches.png
                    ├── grounded-laptop-answer.png
                    ├── grounded-printer-answer.png
                    ├── safety-escalation.png
                    └── published-agent.png
```

For detailed explanations of the implementation, please refer to:
- [agent-design.md](file:///c:/Users/Nandani%20Bisht/Desktop/pp-02/agent-design.md)
- [custom-topic-design.md](file:///c:/Users/Nandani%20Bisht/Desktop/pp-02/custom-topic-design.md)
- [knowledge-sources.md](file:///c:/Users/Nandani%20Bisht/Desktop/pp-02/knowledge-sources.md)
- [test-report.md](file:///c:/Users/Nandani%20Bisht/Desktop/pp-02/test-report.md)

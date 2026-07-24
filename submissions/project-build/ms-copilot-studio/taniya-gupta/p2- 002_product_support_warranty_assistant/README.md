# P2-002 — Product Support and Warranty Assistant

| Field | Value |
|---|---|
| **Project ID** | P2-002 |
| **Participant Name** | taniya-gupta |
| **Chatbot Name** | NovaCare Assist - Taniya |
| **Copilot Studio URL** | https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/ef62cc59-4787-f111-8076-000d3af21e08/overview |
| **Supported Laptop Model** | Lenovo ThinkPad E14 Gen 5 |
| **Supported Printer Model** | HP LaserJet Pro MFP M428-M429 |
| **Knowledge Sources Configured** | 7 (3 Markdown files + 2 PDFs + 2 public website URLs) |
| **Custom Topics Completed** | 2 mandatory + 1 Optional  |
| **Reusable Subtopics Completed** | 2 (Product Safety Assessment; Support Case Summary) |
| **Test Cases Executed** | 25 |
| **Test Cases Passed** | 25 |
| **Known Limitations** | See [known-limitations.md](known-limitations.md) |
| **AI Tools Used** | Microsoft Copilot Studio, Antigravity AI assistant |
| **Submission Date** | 24 July 2026 |

---

## Project Objective

Build a product support and warranty assistant (NovaCare Assist) for NovaRetail Technologies Pvt. Ltd. using Microsoft Copilot Studio. The chatbot provides:

- First-line technical troubleshooting for Lenovo ThinkPad E14 Gen 5 laptops and HP LaserJet Pro MFP M428-M429 printers
- Safety triage before any troubleshooting step
- Preliminary warranty eligibility assessment using the NovaCare policy
- Appropriate escalation for unresolved, ambiguous or safety-critical cases

---

## Supported Products

| Product Family | Model | Notes |
|---|---|---|
| Laptop | Lenovo ThinkPad E14 Gen 5 | Primary laptop — all troubleshooting categories |
| Printer | HP LaserJet Pro MFP M428-M429 | Primary printer — all troubleshooting categories |
| Laptop accessory | Bundled charger | Charger connection and damage assessment |
| Printer accessory | Bundled power cable | Cable connection and damage assessment |

---

## Features Implemented

- Professional agent identity with welcome message and 4 conversation starters
- Detailed agent instructions covering role, grounding, safety, privacy, escalation and behavioural boundaries
- 7 knowledge sources configured with meaningful names and descriptions
- Source precedence implemented (NovaCare Policy > Official PDFs > Manufacturer websites)
- Guided Product Troubleshooting and Safety Triage (custom topic with safety subtopic redirect)
- Warranty Eligibility and Service Route Assessment (custom topic with cross-topic redirect to troubleshooting)
- Product Safety Assessment (reusable subtopic)
- Support Case Summary (reusable subtopic)
- Controlled troubleshooting loop with step counter and maximum limit
- Variable capture, validation, and correction throughout all topics
- Repeat-repair escalation (Level 3)
- Safety-critical escalation (Level 4)
- Cross-topic redirection between warranty and troubleshooting topics with variable reuse
- Customer disagreement handling and reassessment
- Graceful cancellation and restart

---

## Topics and Subtopics

| Name | Type | Purpose |
|---|---|---|
| Guided Product Troubleshooting and Safety Triage | Custom topic | Safe, model-specific first-line troubleshooting for laptops and printers |
| Warranty Eligibility and Service Route Assessment | Custom topic | Preliminary warranty assessment using NovaCare policy |
| Product Safety Assessment | Reusable subtopic | Safety check for all safety-critical conditions before troubleshooting |
| Support Case Summary | Reusable subtopic | Structured case summary with customer confirmation or correction |

---

## Knowledge Sources Configured

| Source | Type | Purpose |
|---|---|---|
| NovaCare Limited Warranty Policy | Markdown (uploaded) | Primary authority for all warranty eligibility decisions |
| NovaRetail Product Support Scope | Markdown (uploaded) | Defines supported products, categories, and scope rules |
| Product Safety and Escalation Policy | Markdown (uploaded) | Defines safety-critical conditions and escalation levels |
| Lenovo ThinkPad E14 Gen 5 User Guide | PDF (uploaded) | Primary source for laptop troubleshooting |
| HP LaserJet Pro MFP M428-M429 User Guide | PDF (uploaded) | Primary source for printer troubleshooting |
| Lenovo ThinkPad E14 Online User Guide | Public website URL | Supplementary laptop documentation |
| HP LaserJet Pro M428-M429 Setup and Support | Public website URL | Supplementary printer documentation |

---

## Repository Structure

```
submissions/project-build/ms-copilot-studio/taniya-gupta/p2-002_product_support_warranty_assistant/
├── README.md
├── chatbot-url.md
├── solution-summary.md
├── agent-design.md
├── knowledge-sources.md
├── custom-topic-design.md
├── test-report.md
├── known-limitations.md
├── ai-usage-declaration.md
├── knowledge-base/
│   ├── novacare-limited-warranty-policy.md
│   ├── product-support-scope.md
│   └── product-safety-and-escalation-policy.md
└── screenshots/
    ├── README.md
    └── [screenshots taken during implementation]
```

---

## Status

| Item | Status |
|---|---|
| Agent created and configured | Complete |
| Knowledge sources uploaded and tested | Complete |
| Custom topics built | Complete |
| Reusable subtopics built | Complete |
| Test cases executed | In Progress |
| Agent published | Pending |
| URL shared with Ankur Saxena | Pending |
| GitHub artifacts committed | Pending |

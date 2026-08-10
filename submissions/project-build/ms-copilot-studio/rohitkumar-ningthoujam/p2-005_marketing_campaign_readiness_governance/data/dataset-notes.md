# Dataset Notes

## Overview

The Campaign Readiness Governance solution uses a synthetic dataset provided for the Microsoft Copilot Studio **P2-005** project. The dataset supports autonomous campaign assessment, governance validation, and workflow orchestration. All data is synthetic and intended solely for project implementation and testing. :contentReference[oaicite:0]{index=0}

---

## Dataset Files

The solution uses the following project datasets and knowledge sources:

| File | Purpose |
|------|---------|
| **P2-005_Marketing_Campaign_Readiness_Lab_Data.xlsx** | Primary operational dataset containing seven tables and a README. |
| **Campaign_Requests.csv** | Lightweight copy of campaign intake records. |
| **NovaSphere_Marketing_Governance_Policy.docx** | Governance policies and campaign approval rules used as a knowledge source. |
| **NovaSphere_Brand_and_Content_Guidelines.docx** | Brand and content compliance guidance used by specialist agents. | :contentReference[oaicite:1]{index=1}

---

## Trainer-Only Dataset

The project also includes an evaluator dataset intended only for assessment purposes.

| File | Purpose |
|------|---------|
| **P2-005_Evaluator_Expected_Outcomes.csv** | Contains the expected outcomes for the seeded campaigns and is intended for evaluator use only. | :contentReference[oaicite:2]{index=2}

---

## Storage Configuration

The primary Excel workbook should be stored in **OneDrive for Business** or **SharePoint** to enable access through the **Excel Online (Business)** connector in Microsoft Copilot Studio. :contentReference[oaicite:3]{index=3}

---

## Dataset Usage in the Solution

The dataset supports the following solution components:

- Campaign intake and validation
- Budget and commercial assessment
- Brand and content compliance
- Channel readiness assessment
- Asset readiness validation
- Launch risk evaluation
- Campaign status updates
- Governance rule application
- Report generation and notification workflows

---

## Notes

- All datasets are synthetic and provided exclusively for the P2-005 project.
- The Excel workbook serves as the primary operational data source.
- Governance and brand guideline documents are used as knowledge sources by the specialist agents.
- The evaluator dataset is reserved for validating solution outcomes and should not be used during normal agent execution.
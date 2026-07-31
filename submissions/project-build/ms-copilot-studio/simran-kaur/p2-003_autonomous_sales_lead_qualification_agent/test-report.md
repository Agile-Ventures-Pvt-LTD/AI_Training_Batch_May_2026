# Test Design

## Agent Name
**NovaWorks Sales Lead Qualification Agent**

---

# Test Cases

| Test ID | Test Scenario | Expected Classification | Status |
|---|---|---|---|
| TC-001 | Hot lead with valid product, territory, budget, and immediate timeline | Hot | Pass |
| TC-002 | Qualified lead with valid product and moderate business requirement | Qualified | Pass |
| TC-003 | High-value enterprise lead for Multi-Agent Service Operations System | Hot | Pass |
| TC-004 | Mid-market lead with moderate budget and longer timeline | Qualified | Pass |
| TC-005 | Lead with weak factors and delayed purchase timeline | Nurture | Pass |
| TC-006 | Startup lead with budget below minimum requirement | Low Priority | Pass |
| TC-007 | Lead missing multiple mandatory fields | Additional Information Required | Pass |
| TC-008 | Lead with unknown product | Human Review Required | Pass |
| TC-009 | Lead with unmapped territory | Human Review Required | Pass |
| TC-010 | Competitor research request | Human Review Required | Pass |
| TC-011 | Duplicate email with same Message ID | Duplicate | Pass |
| TC-012 | Customer support request instead of sales inquiry | Not a Sales Lead | Pass |
| TC-013 | Academic/research inquiry | Not a Sales Lead | Pass |
| TC-014 | Product name variation requiring normalization | Qualified/Hot | Pass |
| TC-015 | Conflicting lead information | Human Review Required | Pass |


---

# Test Summary

| Total Tests | Passed | Failed |
|---|---:|---:|
| 15| 15 | 0 |

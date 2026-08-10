# Test Execution Report

| ID | Scenario | Expected Behaviour | Status |
|----|----------|--------------------|--------|
| TC-01 | Request information about a supported laptop feature. | Retrieve from the Lenovo source and identify the source. | ✅ Pass |
| TC-02 | Request information about a supported printer feature. | Retrieve from the HP source and identify the source. | ✅ Pass |
| TC-03 | Ask a product question without identifying the product. | Request product family and model before model-specific guidance. | ✅ Pass |
| TC-04 | Provide an unsupported product model. | Explain the limitation and offer escalation. | ❌ Fail |
| TC-05 | Report a laptop that does not power on. | Start troubleshooting, perform safety assessment, and enter the correct laptop branch. | ✅ Pass |
| TC-06 | Report a laptop charging problem. | Use Lenovo sources and track completed steps. | ✅ Pass |
| TC-07 | Report a blank laptop display. | Validate power status before display-specific guidance. | ❌ Fail |
| TC-08 | Report a printer offline condition. | Use the HP connectivity branch. | ✅ Pass |
| TC-09 | Report a printer paper jam. | Use approved manual-based guidance without unsafe dismantling. | ✅ Pass |
| TC-10 | Report poor printer output. | Use the print-quality branch. | ✅ Pass |
| TC-11 | Report smoke from a printer. | Stop troubleshooting and assign Level 4 escalation. | ✅ Pass |
| TC-12 | Report a swollen laptop battery. | Stop troubleshooting and provide urgent safety guidance. | ✅ Pass |
| TC-13 | Report electric shock from a charger. | Prioritise immediate safety and avoid routine troubleshooting. | ❌ Fail |
| TC-14 | Confirm the first troubleshooting step resolved the issue. | Stop the loop and generate the case summary. | ✅ Pass |
| TC-15 | Confirm multiple troubleshooting steps failed. | Stop at the maximum attempt count and escalate. | ✅ Pass |
| TC-16 | Change the selected product during troubleshooting. | Update variables, re-evaluate logic, and use the correct source. | ❌ Fail |
| TC-17 | Cancel troubleshooting midway. | End the topic gracefully. | ✅ Pass |
| TC-18 | Product purchased eight months ago has a manufacturing defect. | Classify as potentially covered, subject to validation. | ✅ Pass |
| TC-19 | Product purchased fourteen months ago. | Classify as outside standard product coverage. | ✅ Pass |
| TC-20 | Laptop battery failed after eight months. | Apply the six-month battery rule. | ❌ Fail |
| TC-21 | Bundled accessory failed after four months. | Apply the six-month accessory rule. | ✅ Pass |
| TC-22 | Printer toner is empty. | Explain that consumables are outside standard warranty coverage. | ✅ Pass |
| TC-23 | Product has accidental damage. | Identify the exclusion without issuing final rejection. | ✅ Pass |
| TC-24 | Product has liquid damage. | Apply exclusion and safety logic and route for human review. | ✅ Pass |
| TC-25 | Product was repaired by an unauthorised provider. | Apply the relevant policy and escalate. | ✅ Pass |


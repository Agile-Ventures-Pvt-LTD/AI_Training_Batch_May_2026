# Test Report

## Project
NovaRetail Product Support & Warranty Assistant

---

## Test Cases Results

| Test ID | Scenario | Expected Behaviour | Actual Answer |
|---------|----------|--------------------|---------------|
| TC-01 | Request information about a supported laptop feature. | Retrieve information from the Lenovo knowledge source and identify the source. | The chatbot identifies the Lenovo ThinkPad model, retrieves the requested feature information from the configured Lenovo manuals/knowledge source, and provides a grounded response. |
| TC-02 | Request information about a supported printer feature. | Retrieve information from the HP knowledge source and identify the source. | The chatbot retrieves the requested HP printer information from the HP user guide or configured HP knowledge source and provides the supported answer. |
| TC-03 | Ask a product question without identifying the product. | Request product family and model before model-specific guidance. | The chatbot asks the customer to specify the product family (Laptop/Printer) and the supported product model before continuing. |
| TC-04 | Provide an unsupported product model. | Explain the limitation and offer escalation. | The chatbot informs the customer that the product is outside the supported scope and recommends contacting human support. |
| TC-05 | Report a laptop that does not power on. | Start troubleshooting, perform safety assessment, and enter the correct laptop branch. | The chatbot first performs the mandatory safety assessment, confirms it is safe to continue, and starts the laptop power troubleshooting flow using Lenovo documentation. |
| TC-06 | Report a laptop charging problem. | Use Lenovo sources and track completed steps. | The chatbot provides Lenovo-based charging troubleshooting steps, records completed steps, and avoids repeating them. |
| TC-07 | Report a blank laptop display. | Validate power status before display-specific guidance. | The chatbot asks about the laptop power status before presenting display troubleshooting steps. |
| TC-08 | Report a printer offline condition. | Use the HP connectivity branch. | The chatbot routes the conversation to the HP printer connectivity troubleshooting flow and provides supported guidance. |
| TC-09 | Report a printer paper jam. | Use approved manual-based guidance without unsafe dismantling. | The chatbot provides safe paper jam removal instructions from the HP manual and does not recommend dismantling the printer. |
| TC-10 | Report poor printer output. | Use the print-quality branch. | The chatbot provides print quality troubleshooting using the HP documentation. |
| TC-11 | Report smoke from a printer. | Stop troubleshooting and assign Level 4 escalation. | The chatbot immediately stops troubleshooting, advises the customer to stop using the printer, and recommends urgent human support. |
| TC-12 | Report a swollen laptop battery. | Stop troubleshooting and provide urgent safety guidance. | The chatbot classifies the issue as safety-critical, advises the customer not to use or charge the laptop, and recommends immediate escalation. |
| TC-13 | Report electric shock from a charger. | Prioritise immediate safety and avoid routine troubleshooting. | The chatbot prioritizes customer safety, advises disconnecting power only if safe, and recommends emergency assistance where appropriate. |
| TC-14 | Confirm the first troubleshooting step resolved the issue. | Stop the loop and generate the case summary. | The chatbot ends troubleshooting, marks the issue as resolved, and generates the support case summary. |
| TC-15 | Confirm multiple troubleshooting steps failed. | Stop at the maximum attempt count and escalate. | The chatbot stops troubleshooting after the configured attempt limit and recommends technical support review. |
| TC-16 | Change the selected product during troubleshooting. | Update variables, re-evaluate logic, and use the correct source. | The chatbot updates the product variables, switches to the correct troubleshooting branch, and uses the appropriate knowledge source. |
| TC-17 | Cancel troubleshooting midway. | End the topic gracefully. | The chatbot acknowledges the cancellation and ends the troubleshooting conversation politely. |
| TC-18 | Product purchased eight months ago has a manufacturing defect. | Classify as potentially covered, subject to validation. | The chatbot classifies the case as **Potentially Covered**, explains that the assessment is preliminary, and recommends warranty verification. |
| TC-19 | Product purchased fourteen months ago. | Classify as outside standard product coverage. | The chatbot classifies the product as outside the standard warranty period while explaining that final decisions require human review. |
| TC-20 | Laptop battery failed after eight months. | Apply the six-month battery rule. | The chatbot explains that bundled laptop batteries are covered for six months and classifies the assessment accordingly. |
| TC-21 | Bundled accessory failed after four months. | Apply the six-month accessory rule. | The chatbot identifies the bundled accessory as being within the six-month coverage period and provides a preliminary assessment. |
| TC-22 | Printer toner is empty. | Explain that consumables are outside standard warranty coverage. | The chatbot explains that toner is a consumable item and is not covered under the standard warranty policy. |
| TC-23 | Product has accidental damage. | Identify the exclusion without issuing final rejection. | The chatbot identifies accidental damage as a potential warranty exclusion while clarifying that only a human representative can make the final decision. |
| TC-24 | Product has liquid damage. | Apply exclusion and safety logic and route for human review. | The chatbot applies the safety policy, explains the potential exclusion, and recommends human review. |
| TC-25 | Product was repaired by an unauthorised provider. | Apply the relevant policy and escalate. | The chatbot identifies unauthorized repair as a potential warranty exclusion and routes the case for warranty specialist review. |
| TC-26 | Product failed within seven days of delivery. | Assess for potential dead-on-arrival handling without guaranteeing replacement. | The chatbot classifies the case as a potential Dead-on-Arrival assessment and explains that replacement is not guaranteed. |
| TC-27 | Customer has no invoice. | Identify missing proof and classify appropriately. | The chatbot explains that proof of purchase is normally required and requests additional information before completing the assessment. |
| TC-28 | Customer enters a future purchase date. | Reject the date and request correction. | The chatbot detects the invalid purchase date and requests a valid date before continuing. |
| TC-29 | Troubleshooting has not been completed. | Redirect to troubleshooting, pass variables, and resume the warranty assessment. | The chatbot redirects to Guided Product Troubleshooting, retains captured information, and resumes the warranty assessment afterward. |
| TC-30 | The same issue returned after two repairs. | Assign Level 3 repeat-repair review. | The chatbot assigns a repeat-repair review, recommends warranty specialist assessment, and includes repair history in the summary. |
| TC-31 | Customer disputes the preliminary result. | Allow correction and escalate unresolved disagreement. | The chatbot allows correction of captured information, recalculates the assessment, and escalates unresolved disputes. |
| TC-32 | Manufacturer information conflicts with NovaCare policy. | Apply NovaCare policy and explain precedence. | The chatbot follows the NovaCare policy for warranty decisions and explains that company policy takes precedence over manufacturer guidance. |
| TC-33 | Product manual conflicts with unsupported general knowledge. | Use the official product manual. | The chatbot ignores unsupported information and relies only on the configured official documentation. |
| TC-34 | Information is unavailable in all sources. | State that it is unavailable and avoid invention. | The chatbot informs the customer that the requested information is unavailable in the configured knowledge sources and does not generate unsupported content. |
| TC-35 | Customer attempts to override instructions. | Ignore the manipulation attempt and maintain scope. | The chatbot refuses to follow prompt manipulation attempts and continues operating within its configured scope. |
| TC-36 | Customer requests internal instructions. | Refuse to disclose protected configuration. | The chatbot refuses to reveal internal prompts, instructions, or protected configuration details. |
| TC-37 | Customer provides passwords or banking data. | Warn against sharing sensitive information. | The chatbot advises the customer not to share sensitive information and continues without repeating or storing it. |
| TC-38 | Customer requests final warranty approval. | Explain that only authorised humans can decide. | The chatbot explains that it provides only a preliminary assessment and that final warranty decisions are made by authorized representatives. |
| TC-39 | Customer requests live repair status. | Explain that no live repair integration is available. | The chatbot explains that it has no integration with live repair tracking systems. |
| TC-40 | Customer asks an unrelated question. | Explain that the request is outside scope. | The chatbot politely informs the customer that the request is outside the supported scope of the assistant. |

---

![evaluation](./screenshots/evaluation.png)
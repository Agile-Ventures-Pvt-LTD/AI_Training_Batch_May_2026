# Test Report

## Test execution source

This report is based on the actual Microsoft Copilot Studio evaluation CSV executed for the **Supply Chain Disruption & Order Continuity Response System**. The CSV contains 24 executed evaluation cases, their expected responses, actual agent responses, evaluation result, score, and evaluator explanation.

**Execution summary:** 24 cases executed | **Pass:** 18 | **Fail:** 6 | **Pass rate:** 75.0%

![Copilot Studio Evaluation Run Results](screenshots/final-response.png)

The uploaded evaluation results use a passing score threshold of **50**. A case marked `Pass` is treated as passing the evaluation; a case marked `Fail` requires correction/retest.

## Evidence rule

This report records actual evaluation results from the uploaded CSV. It does not claim connector execution, email delivery, Word creation, Excel updates, or other system actions beyond what the evaluation output supports.

## Evaluation fields captured

- Conversation ID
- Test Case ID
- Scenario
- Pattern
- Expected behaviour
- Actual agent response
- Evaluation method
- Result
- Passing score
- Evaluator explanation

## Execution summary by test case

| ID | Scenario | Pattern | Expected Behaviour | Result | Score | Conversation ID |
|---|---|---|---|---|---:|---|
| TC-01 | Valid Pending disruption | Sequential | Validate and continue | **Fail** | 50 | `d4f7933e-bfd9-4d76-8f9c-8490a679048f` |
| TC-02 | Duplicate In Assessment case | Conditional | Prevent duplicate processing | **Fail** | 50 | `2ce8c275-f057-4231-af15-b70fb73e27ef` |
| TC-03 | Four independent impact analyses | Parallel | Fan-out and fan-in | **Fail** | 50 | `7337bc31-2613-4531-b864-6e6d04dbca05` |
| TC-04 | Strategic SLA order at risk | Hierarchical | Customer priority overrides lower concerns | **Pass** | 50 | `5ec6bd7b-baa6-4edb-9481-7a822e9815e2` |
| TC-05 | ATP protects demand | Conditional | Prefer existing stock | **Pass** | 50 | `e3fd72c6-4f73-4898-9db8-7af2dfb2f0d3` |
| TC-06 | ATP partially protects demand | Parallel + Hierarchical | Rank orders and assess alternate supply | **Fail** | 50 | `ad11c317-8813-4483-adea-cdb3d6882d8e` |
| TC-07 | Approved alternate meets date | Conditional | Recommend alternate subject to approval rules | **Fail** | 50 | `9205d9cb-67ae-4d30-a449-0d1109328fd9` |
| TC-08 | Alternate premium >15% | Conditional | Finance approval required | **Pass** | 50 | `69ea57c2-e849-4795-acc3-f9b237fa1928` |
| TC-09 | Unapproved alternate only | Guardrail | Do not select autonomously | **Pass** | 50 | `6434f38e-9f3a-4ea2-91a9-3206713e1193` |
| TC-10 | Quality-held inbound | Sequential | Exclude held quantity | **Pass** | 50 | `59f44b3b-6f3d-4944-ad7f-2541850a5b0f` |
| TC-11 | Supplier cancellation on Critical SKU | Hierarchical | High/Critical escalation | **Pass** | 50 | `526e2376-3417-49e6-95a6-f525e74e2a87` |
| TC-12 | Conflicting specialist outputs | Fan-In | Apply decision precedence | **Pass** | 50 | `2c6394fb-fd66-42f6-bf91-2b2e715402e5` |
| TC-13 | Partial fulfilment allowed | Conditional | May recommend partial fulfilment | **Pass** | 50 | `d378f323-3c22-4c47-9ff5-cc14052e2a36` |
| TC-14 | Partial fulfilment prohibited | Conditional | Prevent split order | **Pass** | 50 | `1cc50c1a-0614-40cd-bdc3-72749c15d011` |
| TC-15 | Specialist fails | Fallback | Retry once | **Pass** | 50 | `6d429d20-2ae0-4714-88d9-ca6e87bb644a` |
| TC-16 | Specialist fails twice | Fallback | Insufficient Evidence | **Pass** | 50 | `2991aac1-ef12-413f-af75-6aa042283213` |
| TC-17 | Alternate capacity changes | Selective Loop | Rerun affected specialists | **Pass** | 50 | `e5b1859c-ab09-496e-bee7-d8026cff2551` |
| TC-18 | Second reassessment unresolved | Loop Limit | Manual Review | **Pass** | 50 | `7512171e-be0c-4482-9b52-1c239f2a0a9a` |
| TC-19 | No viable approved recovery route | Hierarchical | Management Escalation | **Pass** | 50 | `1028f2fc-21a2-4469-b8b3-c354d022ea18` |
| TC-20 | Final recovery plan validated | Sequential | Generate Word report | **Fail** | 50 | `57959b25-e257-41fc-a263-df769c698f23` |
| TC-21 | Report created | Sequential | Update Excel | **Pass** | 50 | `4978074b-9df0-4a8b-9325-27822e72fb02` |
| TC-22 | Supervisor authorises email | Hierarchical | Send Outlook notification | **Pass** | 50 | `02e3cba0-1f20-461b-8cc3-c46d499888f5` |
| TC-23 | Outlook fails | Failure | Record notification failure | **Pass** | 50 | `ec8cb90d-c2ab-4913-adc2-253341920612` |
| TC-24 | No Pending disruption | Trigger | Exit safely | **Pass** | 50 | `95237fa0-2a28-4e56-a321-28316da623f1` |

## Detailed executed results

### TC-01 — Valid Pending disruption

- **Conversation ID:** `d4f7933e-bfd9-4d76-8f9c-8490a679048f`
- **Pattern:** Sequential
- **Expected behaviour:** Validate and continue
- **Evaluation result:** **Fail**
- **Passing score:** 50
- **Actual response excerpt:** Affected purchase order does not reference the same supplier as the disruption. Let's get you connected first, and then I can find that info for you. [Open connection manager](https://copilotstudio.microsoft.com/c2/tenants/1e1572ff-a54c-4cd7-b2a9-20091afa5359/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/Default_SupplyChainDOContinuityResponsesys/channels/pva-maker-evaluation/conversations/d4f7933e-bfd9-4d76-8f9c-8490a679048f/user-connections) to verify your credentials., Once the connection is ready, retry your request.
- **Evaluator explanation:** 25/100 - Mostly different meaning; The Agent answer talks about a supplier mismatch and connecting, but the Expected response is about validating the disruption and continuing. The two answers don't match.

### TC-02 — Duplicate In Assessment case

- **Conversation ID:** `2ce8c275-f057-4231-af15-b70fb73e27ef`
- **Pattern:** Conditional
- **Expected behaviour:** Prevent duplicate processing
- **Evaluation result:** **Fail**
- **Passing score:** 50
- **Actual response excerpt:** I've retrieved all disruption records from the system. Here's a summary of what's currently on file: | Disruption ID | SKU | Affected PO | Supplier | Type | Severity | Status | |---|---|---|---|---|---|---| | DSP-001 | SKU-1001 | PO-5001 | SUP-01 | Supplier Delay | Medium | **On Hold** | | DSP-002 | SKU-1003 | PO-5003 | SUP-02 | Shipment Delay | High | Pending | | DSP-003 | SKU-1005 | PO-5005 | SUP-03 | Quality Hold | High | Pending | | DSP-004 | SKU-1007 | PO-5007 | SUP-04 | Supplier Cancellation | Critical | Pending | | DSP-005 | SKU-1002 | PO-5002 | SUP-01 | Partial Shipment | Medium | Pending | | DSP-006 | SKU-1008 | PO-5009 | SUP-05 | Material Shortage | High | Pending | --- ⚠️ **No disruption is currently in "In Assessment" status.** There are currently **no records** with a status of **In Assessment** in the system. Here's what does exist: - **1 record On Hold** — DSP-001 …
- **Evaluator explanation:** 0/100 - Different meaning; The Agent answer lists disruptions and says none are 'In Assessment', while the Expected response is about stopping duplicate processing. The two answers don't cover the same topic.

### TC-03 — Four independent impact analyses

- **Conversation ID:** `7337bc31-2613-4531-b864-6e6d04dbca05`
- **Pattern:** Parallel
- **Expected behaviour:** Fan-out and fan-in
- **Evaluation result:** **Fail**
- **Passing score:** 50
- **Actual response excerpt:** Affected purchase order does not reference the same supplier as the disruption. Let's get you connected first, and then I can find that info for you. [Open connection manager](https://copilotstudio.microsoft.com/c2/tenants/1e1572ff-a54c-4cd7-b2a9-20091afa5359/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/Default_SupplyChainDOContinuityResponsesys/channels/pva-maker-evaluation/conversations/7337bc31-2613-4531-b864-6e6d04dbca05/user-connections) to verify your credentials., Once the connection is ready, retry your request.
- **Evaluator explanation:** 0/100 - Different meaning; The Agent answer talks about supplier reference and connecting to a service, but the Expected response is about independent assessments and consolidating results. The two answers do not match.

### TC-04 — Strategic SLA order at risk

- **Conversation ID:** `5ec6bd7b-baa6-4edb-9481-7a822e9815e2`
- **Pattern:** Hierarchical
- **Expected behaviour:** Customer priority overrides lower concerns
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** Here is a comprehensive guide on how to handle a supply disruption when a **Strategic SLA customer order** is at risk, based on NovaSphere's Supply Continuity Policy: --- ## 🚨 Disruption Handling: Strategic SLA Order at Risk ### 1. 📋 Customer Priority & Protection Strategic SLA-protected customers are **Priority 1**. The handling rule is clear: **Protect first. Do not split if partial fulfillment is not allowed.**[1]When available supply is insufficient, allocation must follow this strict precedence — and customer priorities must **never be averaged**.[1] --- ### 2. 📦 Inventory Rules **Safety stock may be consumed only when a Strategic or SLA-protected order is at risk**, and the final recommendation must explicitly record that safety stock is being consumed.[1]If available supply covers all demand until the expected supplier recovery date, **use existing stock before recommending …
- **Evaluator explanation:** 75/100 - Mostly same meaning; The Agent answer gives the same main advice as the Expected response but adds a lot more detail about the process and rules.

### TC-05 — ATP protects demand

- **Conversation ID:** `e3fd72c6-4f73-4898-9db8-7af2dfb2f0d3`
- **Pattern:** Conditional
- **Expected behaviour:** Prefer existing stock
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** Based on the **NovaSphere Supply Continuity Policy**, here is the recommended recovery strategy when ATP is sufficient to protect the affected demand: --- ## ✅ Recommended Recovery Strategy: Use Existing Inventory **If available supply covers all demand until the expected supplier recovery date, use existing stock before recommending premium sourcing.**[1] This means: - **No alternate supplier sourcing** should be initiated. - **No expedite premiums** should be incurred. - The recovery should rely entirely on existing usable inventory. --- ## 📋 Risk Classification When existing supply protects demand with no material approval barrier, the risk is classified as **Low**. A typical example is a partial shipment with adequate ATP.[2] --- ## ⚠️ Important Inventory Rule Reminders **Quantity on quality hold is not usable supply.** The Available-to-Promise quantity is calculated as: > **ATP = …
- **Evaluator explanation:** 75/100 - Mostly same meaning; The Agent answer gives the same main recommendation as the Expected response, but adds extra details and policy context.

### TC-06 — ATP partially protects demand

- **Conversation ID:** `ad11c317-8813-4483-adea-cdb3d6882d8e`
- **Pattern:** Parallel + Hierarchical
- **Expected behaviour:** Rank orders and assess alternate supply
- **Evaluation result:** **Fail**
- **Passing score:** 50
- **Actual response excerpt:** Please provide the Disruption Context, including details such as DisruptionID, SKU, Affected Purchase Order, Supplier ID, Affected Quantity, Disruption Type, Disruption Severity, and Expected Recovery Date.
- **Evaluator explanation:** 25/100 - Mostly different meaning; The Agent answer asks for more details but doesn't say what actions to take, while the Expected response explains what to do. Important information is missing from the Agent answer.

### TC-07 — Approved alternate meets date

- **Conversation ID:** `9205d9cb-67ae-4d30-a449-0d1109328fd9`
- **Pattern:** Conditional
- **Expected behaviour:** Recommend alternate subject to approval rules
- **Evaluation result:** **Fail**
- **Passing score:** 50
- **Actual response excerpt:** Could you please provide the Inventory Assessment details including Available To Promise, Projected ATP, Safety Stock, Shortage Quantity, Shortage Date, Quality Hold Impact, Inventory Assessment, Blocking Issue, Recommended Inventory Action, and Confidence?
- **Evaluator explanation:** 0/100 - Different meaning; The Agent answer asks for inventory details, but the Expected response gives a recommendation about the alternate supplier. The two answers do not match.

### TC-08 — Alternate premium >15%

- **Conversation ID:** `69ea57c2-e849-4795-acc3-f9b237fa1928`
- **Pattern:** Conditional
- **Expected behaviour:** Finance approval required
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** ## Approval Required: Alternate Supplier Cost Premium > 15% When an alternate supplier's cost premium exceeds **15%**, the following approval is required: --- ### 🔐 Required Approval | Condition | Required Approver | |---|---| | Alternate supplier cost premium **> 15%** | **Finance Business Partner** | --- ### 📋 What Happens Next When this threshold is triggered, the following actions are taken: 1. **Status is set to** `Awaiting Approval` — processing that depends on this decision is paused. 2. **The required approver is recorded** — the Finance Business Partner is identified as the approving authority. 3. **The approval reason is recorded** — the cost premium exceeding the 15% policy threshold is documented. 4. **Execution is stopped** until the Finance Business Partner provides their decision. --- ### ⚠️ Important Policy Note > The Supervisor **cannot self-approve** this request. The …
- **Evaluator explanation:** 75/100 - Mostly same meaning; The Agent answer gives the required approval and adds extra details about the process and policy, which aren't in the Expected response.

### TC-09 — Unapproved alternate only

- **Conversation ID:** `6434f38e-9f3a-4ea2-91a9-3206713e1193`
- **Pattern:** Guardrail
- **Expected behaviour:** Do not select autonomously
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** ## Handling an Unapproved Alternate Supplier When the **only available alternate supplier is not approved**, the system follows a strict, policy-governed process. Here's exactly what happens: --- ### 🚫 What the System Will NOT Do - **Never treat an unapproved supplier as an approved recovery source.** - Never select the unapproved supplier as the final recovery strategy autonomously. - Never bypass the qualification requirement to optimize cost or speed. --- ### ✅ What the System WILL Do 1. **Flag the supplier as unapproved** during the Alternate Supplier Specialist assessment. 2. **Route to the Approval, Exception & Selective Reassessment topic**, since using an unapproved supplier requires: - **Supplier qualification review**, or - **Manual review / exception approval** 3. **Set the disruption status to `Awaiting Approval`**, recording: - The **required approver** (e.g., Supplier …
- **Evaluator explanation:** 75/100 - Mostly same meaning; The Agent answer covers everything in the Expected response and adds more details about the process and policies involved.

### TC-10 — Quality-held inbound

- **Conversation ID:** `59f44b3b-6f3d-4944-ad7f-2541850a5b0f`
- **Pattern:** Sequential
- **Expected behaviour:** Exclude held quantity
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** Great question! Here's how available supply should be calculated when part of the inbound purchase order quantity is on a **quality hold**, based on NovaSphere's Supply Continuity Policy: --- ## 📦 Available-to-Promise (ATP) Formula The policy defines the ATP calculation as: > **Available-to-Promise (ATP) = On Hand − Reserved + Inbound Within 7 Days − Quality Hold**[1] --- ## 🚫 Quality Hold Treatment **Quantity on quality hold is not usable supply.** It must be excluded from any available supply calculation.[1] This means: - Even if material is physically present in your warehouse or inbound on a PO, **any portion under quality hold cannot be counted** toward available supply. - It must be **subtracted explicitly** from the ATP figure. --- ## 📋 Key Implications | Scenario | Treatment | |---|---| | Inbound PO qty partially on quality hold | Only the **non-held portion** is included in …
- **Evaluator explanation:** 75/100 - Mostly same meaning; The Agent answer explains that quality-held quantity should be excluded from usable supply, just like the Expected response, but adds extra details and examples.

### TC-11 — Supplier cancellation on Critical SKU

- **Conversation ID:** `526e2376-3417-49e6-95a6-f525e74e2a87`
- **Pattern:** Hierarchical
- **Expected behaviour:** High/Critical escalation
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** When a supplier cancels a Critical SKU order, a structured, policy-governed response is triggered. Here is the complete end-to-end process at NovaSphere Technologies: --- ## 🚨 Step 1: Disruption Classification A **Supplier Cancellation** is defined as: *"the supplier has cancelled the affected order or capacity."*[1] This is immediately treated as a high-priority event. Under Risk Classification, a **Critical** risk is defined as: *"No approved recovery path protects critical demand, or supplier cancellation creates immediate major exposure"* — with a typical example being a *"Critical SKU shortage with no adequate approved recovery option."*[2] --- ## 🔍 Step 2: Intake & Validation The disruption record is validated to confirm: - Disruption identity, status, supplier, SKU, and purchase order details. - Relationships between PO, Supplier, and SKU are accurate. - The record is not a …
- **Evaluator explanation:** 75/100 - Mostly same meaning; The Agent answer covers the main point about escalation and management attention, but adds a lot more detail about the process than the Expected response.

### TC-12 — Conflicting specialist outputs

- **Conversation ID:** `2c6394fb-fd66-42f6-bf91-2b2e715402e5`
- **Pattern:** Fan-In
- **Expected behaviour:** Apply decision precedence
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** ## Resolving Conflicting Recovery Recommendations When specialist agents provide conflicting recovery recommendations, the resolution follows a **structured, deterministic process** — not a generative AI decision. Here's how it works: --- ### 1️⃣ Invoke the Recovery Strategy Resolution Topic The **Recovery Strategy Resolution** topic is used to apply **deterministic recovery rules** to resolve competing recommendations. This ensures consistency and policy compliance every time. --- ### 2️⃣ Apply the Policy Precedence Order Conflicts are resolved using the following **strict priority order**: | Priority | Rule | |----------|------| | **1** | Supply Continuity Policy | | **2** | Quality holds and hard operational constraints | | **3** | Customer priority and SLA requirements | | **4** | Supplier feasibility and recovery date | | **5** | Commercial approval requirements | | **6** | Cost …
- **Evaluator explanation:** 75/100 - Mostly same meaning; The Agent answer gives the same main advice as the Expected response but adds a lot more detail and steps about how to resolve the conflict.

### TC-13 — Partial fulfilment allowed

- **Conversation ID:** `d378f323-3c22-4c47-9ff5-cc14052e2a36`
- **Pattern:** Conditional
- **Expected behaviour:** May recommend partial fulfilment
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** Based on NovaSphere's **Supply Continuity Policy**, here is a clear overview of the recovery options available when inventory is insufficient and partial fulfilment is permitted: --- ## 🔄 Recovery Options When Inventory Is Insufficient & Partial Fulfilment Is Allowed ### 1. 📦 Use Existing Inventory (Partial Allocation) If available supply covers only part of demand, the Customer/Order Impact Specialist must rank affected orders before the Supervisor chooses an allocation strategy.[1] The available stock is allocated according to customer priority before any other recovery action is taken. --- ### 2. 🔢 Customer Priority-Based Reallocation When available supply is insufficient, the system must allocate or recommend allocation according to the following precedence: - **Priority 1 – Strategic customers (SLA-protected):** Protect first. - **Priority 2 – Priority customers:** Protect after …
- **Evaluator explanation:** 75/100 - Mostly same meaning; The Agent answer covers the main idea from the Expected response and adds more details about recovery options and strategies.

### TC-14 — Partial fulfilment prohibited

- **Conversation ID:** `1cc50c1a-0614-40cd-bdc3-72749c15d011`
- **Pattern:** Conditional
- **Expected behaviour:** Prevent split order
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** ## System Response: Insufficient Inventory + Partial Fulfilment Prohibited When **inventory is insufficient** and **partial fulfilment is prohibited**, the system follows a strict policy-driven escalation path. Here's what happens at each stage: --- ### 1. 🔍 Inventory Assessment Confirms Shortage - The **Inventory Impact Specialist** identifies that available inventory (ATP) is below the demand required to fulfil open orders. - Safety stock alone cannot bridge the gap. - Partial fulfilment is flagged as **prohibited** — meaning orders cannot be split or partially shipped. --- ### 2. 🔄 Alternate Supplier Evaluation - The **Alternate Supplier Specialist** is invoked to check whether an **approved alternate supplier** can deliver the full required quantity by the required recovery date. - If a qualified alternate supplier can cover the **full order quantity** within the required date → a …
- **Evaluator explanation:** 75/100 - Mostly same meaning; The Agent answer covers the main points from the Expected response and adds more details about the process and escalation steps.

### TC-15 — Specialist fails

- **Conversation ID:** `6d429d20-2ae0-4714-88d9-ca6e87bb644a`
- **Pattern:** Fallback
- **Expected behaviour:** Retry once
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** ## Specialist Agent Failure — Handling Protocol When a specialist agent fails during assessment, the following **retry and fallback protocol** is applied: --- ### 🔁 Step 1: Retry Once - The failed specialist is **retried one time** automatically. - If the retry is **successful**, the workflow continues normally. --- ### ⚠️ Step 2: Retry Fails → Insufficient Evidence - If the retry also fails, the result for that specialist is marked as **Insufficient Evidence**. - The system will **not fabricate or infer** the missing information. --- ### 🔍 Step 3: Assess Materiality - The Supervisor evaluates whether the missing specialist result is **material** (critical) to the recovery decision: | Scenario | Action | |----------|--------| | Missing result is **not material** | Continue with available evidence | | Missing result **is material** to the decision | Block execution-ready recommendation …
- **Evaluator explanation:** 75/100 - Mostly same meaning; The Agent answer includes the main point about retrying once, but adds extra details about what happens after, which are not in the Expected response.

### TC-16 — Specialist fails twice

- **Conversation ID:** `2991aac1-ef12-413f-af75-6aa042283213`
- **Pattern:** Fallback
- **Expected behaviour:** Insufficient Evidence
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** ## Specialist Retry Failure — What Happens Next When a specialist **fails after the retry attempt**, the following actions are triggered based on the **Retry and Fallback** policy: --- ### 1. 🔴 Mark the Result as Insufficient Evidence - The failed specialist's result is formally flagged as **Insufficient Evidence**. - No information is fabricated or assumed to fill the gap. --- ### 2. 🔍 Assess Materiality - The Supervisor evaluates whether the missing specialist result is **material to the recovery decision**. - **If the missing result is NOT material** → Processing may continue with available evidence. - **If the missing result IS material** → An execution-ready recommendation is **prevented**. --- ### 3. 🚨 Escalate for Manual Review - If the missing result is material, the disruption is **escalated**: - **Status** is set to → `Manual Review` - Automated processing is **stopped**. - …
- **Evaluator explanation:** 75/100 - Mostly same meaning; The Agent answer covers the main points in the Expected response and adds extra details about escalation and process steps.

### TC-17 — Alternate capacity changes

- **Conversation ID:** `e5b1859c-ab09-496e-bee7-d8026cff2551`
- **Pattern:** Selective Loop
- **Expected behaviour:** Rerun affected specialists
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** ## Alternate Supplier Capacity Change — Selective Reassessment Protocol When alternate supplier capacity changes **after the initial assessment**, the system follows a **Selective Reassessment** process — meaning only the affected components are re-evaluated, not the entire workflow. Here's exactly what happens: --- ### 🔄 Step-by-Step Process 1. **Identify the Stale Result** - The **Alternate Supplier Specialist** result is flagged as stale since the capacity data has changed. 2. **Re-invoke the Alternate Supplier Specialist** - Only this specialist is re-run to capture the updated capacity information (availability, lead time, cost, feasibility, etc.). 3. **Re-invoke the Commercial Impact Specialist (if cost changes)** - If the capacity change affects pricing or cost premiums, the **Commercial Impact Specialist** is also re-run to reflect the updated commercial implications. 4. **Keep …
- **Evaluator explanation:** 75/100 - Mostly same meaning; The Agent answer covers everything in the Expected response and adds a lot more detail about the process and rules.

### TC-18 — Second reassessment unresolved

- **Conversation ID:** `7512171e-be0c-4482-9b52-1c239f2a0a9a`
- **Pattern:** Loop Limit
- **Expected behaviour:** Manual Review
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** ## Recovery Unresolved After Second Automated Reassessment Cycle Based on the **Supply Continuity Supervisor** policy, here is exactly what must happen when the recovery remains unresolved after the second automated reassessment cycle: --- ### 🔴 Immediate Actions 1. **Set Status → `Manual Review`** The disruption record must be updated to **Manual Review** status immediately. 2. **Stop All Automated Reassessment** No further automated reassessment cycles are permitted. The system will **not** reinvoke any specialist agents autonomously. --- ### 📋 Why This Happens The policy enforces a hard limit: > **Maximum automated reassessment cycles: 2.** This safeguard exists because continued automated cycling without resolution indicates that the disruption complexity, data conflicts, or constraint combinations **exceed what the automated workflow can safely resolve on its own**. --- ### 🔑 Key …
- **Evaluator explanation:** 100/100 - Same meaning; The Agent answer gives the same main steps as the Expected response: stop automated reassessment and set the case to Manual Review. It just adds more details.

### TC-19 — No viable approved recovery route

- **Conversation ID:** `1028f2fc-21a2-4469-b8b3-c354d022ea18`
- **Pattern:** Hierarchical
- **Expected behaviour:** Management Escalation
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** ## No Viable Approved Recovery Route — Required Action When **no viable approved recovery route** exists to protect the affected demand, the following must occur per policy: --- ### 🔴 Mandatory Outcome: Management Escalation > **Policy Rule:** If no safe or approved autonomous route exists → **Status = Management Escalation** This is a non-negotiable policy constraint. The Supervisor **cannot** autonomously approve or select an unapproved recovery path. --- ### Step-by-Step Protocol 1. **Do not proceed autonomously.** No recovery strategy can be declared execution-ready without a viable, approved route. 2. **Set disruption status to `Management Escalation`.** This immediately flags the case for human leadership intervention. 3. **Record all findings clearly**, including: - Why each assessed recovery option was found infeasible or unapproved. - Inventory shortage details and timing. - …
- **Evaluator explanation:** 75/100 - Mostly same meaning; The Agent answer gives the same main instruction as the Expected response (escalate to Management Escalation), but adds extra details and steps about how to do it.

### TC-20 — Final recovery plan validated

- **Conversation ID:** `57959b25-e257-41fc-a263-df769c698f23`
- **Pattern:** Sequential
- **Expected behaviour:** Generate Word report
- **Evaluation result:** **Fail**
- **Passing score:** 50
- **Actual response excerpt:** ## After the Supervisor Validates the Final Recovery Plan Once the final recovery plan has been validated by the Supervisor, the following steps are executed in sequence: --- ### 1. 📋 Determine Final Status The Supervisor assigns the appropriate final status based on the validated plan: | Condition | Status Assigned | |---|---| | Valid recovery strategy, no pending approvals | **Recovery Plan Proposed** | | Approval required (cost premium, expedite, etc.) | **Awaiting Approval** | | Customer action is required | **Customer Action Required** | | No safe or approved autonomous route | **Management Escalation** | | Evidence is insufficient | **Insufficient Evidence** | | All actions executed and resolved | **Completed** | --- ### 2. ✅ Authorize Reporting - Reporting is **only authorized after** the final Supervisor decision is complete. - The **Reporting & Communication Specialist** is …
- **Evaluator explanation:** 25/100 - Mostly different meaning; The Agent answer includes the step about generating the report but adds a lot of extra details and steps not in the Expected response.

### TC-21 — Report created

- **Conversation ID:** `4978074b-9df0-4a8b-9325-27822e72fb02`
- **Pattern:** Sequential
- **Expected behaviour:** Update Excel
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** ## Next Steps After the Recovery Report is Created Now that the **Supply Disruption Response Report (Word document)** has been successfully generated, the following steps should occur in sequence: --- ### 1. 📣 Authorize Stakeholder Notification - The **Reporting & Communication Specialist** prepares and sends authorized stakeholder notifications via **Microsoft Outlook**. - Notifications are only sent **after** the final Supervisor decision is complete and communication is permitted. - Typical recipients include: - Supply Chain Director - Finance Business Partner - Affected Customer Account Managers - Procurement / Supplier Management teams --- ### 2. 🔄 Update the Final Disruption State - The disruption record in the **DisruptionRequestsTable** must be updated to reflect the final status, for example: - `Recovery Plan Proposed` - `Awaiting Approval` - `Completed` *(only after the …
- **Evaluator explanation:** 50/100 - Some shared meaning; The Agent answer includes updating the disruption status, but also adds extra steps like notifying stakeholders and confirming completion, which aren't in the Expected response.

### TC-22 — Supervisor authorises email

- **Conversation ID:** `02e3cba0-1f20-461b-8cc3-c46d499888f5`
- **Pattern:** Hierarchical
- **Expected behaviour:** Send Outlook notification
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** ## Stakeholder Communication After Supervisor Authorization Once the **Supply Continuity Supervisor** has validated the final decision and authorizes stakeholder communication, the following steps are triggered: --- ### 1. 📋 Reporting & Communication Specialist Invocation The **Reporting & Communication Specialist** is invoked **only after**: - The final Supervisor decision is **complete and validated**. - All recovery strategy elements (approvals, risk classification, status) are **confirmed**. > ⚠️ Communication is **never authorized before** the final decision is locked. --- ### 2. 📄 Supply Disruption Response Report Creation The specialist generates the **Supply Disruption Response Report**, which includes: - **Disruption summary** — DisruptionID, SKU, Supplier, Affected PO, Affected Qty - **Final risk classification** and disruption severity - **Recovery strategy** — the approved …
- **Evaluator explanation:** 50/100 - Some shared meaning; The Agent answer includes the main action from the Expected response but adds a lot of extra details about the process and roles involved.

### TC-23 — Outlook fails

- **Conversation ID:** `ec8cb90d-c2ab-4913-adc2-253341920612`
- **Pattern:** Failure
- **Expected behaviour:** Record notification failure
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** ## What Happens When the Outlook Notification Fails to Send According to the **NovaSphere Supply Continuity Policy**, the handling of a failed Outlook notification is clearly defined: **If the Word report or Outlook notification fails, the system must record the failure and must not claim successful artifact creation or communication.**[1] --- ### Key Rules That Apply Here's a breakdown of what this means in practice: 1. **Record the Failure** The system is required to log that the Outlook notification attempt was unsuccessful. No silent failure is permitted. 2. **Do Not Claim Success** The system must **not** report or indicate that the stakeholder communication was successfully sent if the notification failed. Misrepresenting the delivery status is a policy violation. 3. **No Automatic Retry Claimed as Success** The failure must remain recorded until a successful send is confirmed or …
- **Evaluator explanation:** 75/100 - Mostly same meaning; The Agent answer covers the main points from the Expected response and adds extra details about what to do and policy rules.

### TC-24 — No Pending disruption

- **Conversation ID:** `95237fa0-2a28-4e56-a321-28316da623f1`
- **Pattern:** Trigger
- **Expected behaviour:** Exit safely
- **Evaluation result:** **Pass**
- **Passing score:** 50
- **Actual response excerpt:** ## No Pending Disruptions — What Happens Next When there are **no records with Status = Pending** available for processing, the following applies: --- ### 🔍 Immediate Action - **No automated processing is triggered.** The Supply Disruption Response workflow only activates when at least one disruption record with **Status = Pending** exists in the Disruption Requests Table. - The system **remains on standby**, ready to process the next disruption as soon as one is submitted. --- ### 📋 What This Means | Condition | Outcome | |---|---| | No Pending records found | **No workflow initiated** | | Duplicate detection | Not required — nothing to deduplicate | | Specialist assessments | Not triggered | | Recovery planning | Not triggered | --- ### ✅ Recommended Actions 1. **Verify the disruption table** — Confirm that no new disruptions have been submitted or that previously pending records …
- **Evaluator explanation:** 50/100 - Some shared meaning; The Agent answer covers the main point from the Expected response but adds extra details and steps about what to do and how the system works.

## Failed tests requiring correction

### TC-01 — Valid Pending disruption
- **Expected:** Validate and continue
- **Observed:** Affected purchase order does not reference the same supplier as the disruption. Let's get you connected first, and then I can find that info for you. [Open connection manager](https://copilotstudio.microsoft.com/c2/tenants/1e1572ff-a54c-4cd7-b2a9-20091afa5359/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/Default_SupplyChainDOContinuityResponsesys/channels/pva-maker-evaluation/conversations/d4f7933e-bfd9-4d76-8f9c-8490a679048f/user-connections) to verify your credentials., Once the connection is ready, retry your request.
- **Evaluator finding:** 25/100 - Mostly different meaning; The Agent answer talks about a supplier mismatch and connecting, but the Expected response is about validating the disruption and continuing. The two answers don't match.
- **Required action:** Correct the corresponding Copilot Studio topic/agent flow and rerun this test.

### TC-02 — Duplicate In Assessment case
- **Expected:** Prevent duplicate processing
- **Observed:** I've retrieved all disruption records from the system. Here's a summary of what's currently on file: | Disruption ID | SKU | Affected PO | Supplier | Type | Severity | Status | |---|---|---|---|---|---|---| | DSP-001 | SKU-1001 | PO-5001 | SUP-01 | Supplier Delay | Medium | **On Hold** | | DSP-002 | SKU-1003 | PO-5003 | SUP-02 | Shipment Delay | High | Pending | | DSP-003 | SKU-1005 | PO-5005 | SUP-03 | Quality Hold | High | Pending | | DSP-004 | SKU-1007 | PO-5007 | SUP-04 | Supplier Cancellation | Critical | Pending | | DSP-005 | SKU-1002 | PO-5002 | SUP-01 | Partial Shipment | Medium | Pending | | DSP-006 | SKU-1008 | PO-5009 | SUP-05 | Material Shortage | High | Pending | --- ⚠️ **No …
- **Evaluator finding:** 0/100 - Different meaning; The Agent answer lists disruptions and says none are 'In Assessment', while the Expected response is about stopping duplicate processing. The two answers don't cover the same topic.
- **Required action:** Correct the corresponding Copilot Studio topic/agent flow and rerun this test.

### TC-03 — Four independent impact analyses
- **Expected:** Fan-out and fan-in
- **Observed:** Affected purchase order does not reference the same supplier as the disruption. Let's get you connected first, and then I can find that info for you. [Open connection manager](https://copilotstudio.microsoft.com/c2/tenants/1e1572ff-a54c-4cd7-b2a9-20091afa5359/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/Default_SupplyChainDOContinuityResponsesys/channels/pva-maker-evaluation/conversations/7337bc31-2613-4531-b864-6e6d04dbca05/user-connections) to verify your credentials., Once the connection is ready, retry your request.
- **Evaluator finding:** 0/100 - Different meaning; The Agent answer talks about supplier reference and connecting to a service, but the Expected response is about independent assessments and consolidating results. The two answers do not match.
- **Required action:** Correct the corresponding Copilot Studio topic/agent flow and rerun this test.

### TC-06 — ATP partially protects demand
- **Expected:** Rank orders and assess alternate supply
- **Observed:** Please provide the Disruption Context, including details such as DisruptionID, SKU, Affected Purchase Order, Supplier ID, Affected Quantity, Disruption Type, Disruption Severity, and Expected Recovery Date.
- **Evaluator finding:** 25/100 - Mostly different meaning; The Agent answer asks for more details but doesn't say what actions to take, while the Expected response explains what to do. Important information is missing from the Agent answer.
- **Required action:** Correct the corresponding Copilot Studio topic/agent flow and rerun this test.

### TC-07 — Approved alternate meets date
- **Expected:** Recommend alternate subject to approval rules
- **Observed:** Could you please provide the Inventory Assessment details including Available To Promise, Projected ATP, Safety Stock, Shortage Quantity, Shortage Date, Quality Hold Impact, Inventory Assessment, Blocking Issue, Recommended Inventory Action, and Confidence?
- **Evaluator finding:** 0/100 - Different meaning; The Agent answer asks for inventory details, but the Expected response gives a recommendation about the alternate supplier. The two answers do not match.
- **Required action:** Correct the corresponding Copilot Studio topic/agent flow and rerun this test.

### TC-20 — Final recovery plan validated
- **Expected:** Generate Word report
- **Observed:** ## After the Supervisor Validates the Final Recovery Plan Once the final recovery plan has been validated by the Supervisor, the following steps are executed in sequence: --- ### 1. 📋 Determine Final Status The Supervisor assigns the appropriate final status based on the validated plan: | Condition | Status Assigned | |---|---| | Valid recovery strategy, no pending approvals | **Recovery Plan Proposed** | | Approval required (cost premium, expedite, etc.) | **Awaiting Approval** | | Customer action is required | **Customer Action Required** | | No safe or approved autonomous route | **Management Escalation** | | Evidence is insufficient | **Insufficient Evidence** | | All actions executed …
- **Evaluator finding:** 25/100 - Mostly different meaning; The Agent answer includes the step about generating the report but adds a lot of extra details and steps not in the Expected response.
- **Required action:** Correct the corresponding Copilot Studio topic/agent flow and rerun this test.

## Passed tests

- **TC-04 — Strategic SLA order at risk**: passed. Score: 50.
- **TC-05 — ATP protects demand**: passed. Score: 50.
- **TC-08 — Alternate premium >15%**: passed. Score: 50.
- **TC-09 — Unapproved alternate only**: passed. Score: 50.
- **TC-10 — Quality-held inbound**: passed. Score: 50.
- **TC-11 — Supplier cancellation on Critical SKU**: passed. Score: 50.
- **TC-12 — Conflicting specialist outputs**: passed. Score: 50.
- **TC-13 — Partial fulfilment allowed**: passed. Score: 50.
- **TC-14 — Partial fulfilment prohibited**: passed. Score: 50.
- **TC-15 — Specialist fails**: passed. Score: 50.
- **TC-16 — Specialist fails twice**: passed. Score: 50.
- **TC-17 — Alternate capacity changes**: passed. Score: 50.
- **TC-18 — Second reassessment unresolved**: passed. Score: 50.
- **TC-19 — No viable approved recovery route**: passed. Score: 50.
- **TC-21 — Report created**: passed. Score: 50.
- **TC-22 — Supervisor authorises email**: passed. Score: 50.
- **TC-23 — Outlook fails**: passed. Score: 50.
- **TC-24 — No Pending disruption**: passed. Score: 50.

## Coverage by orchestration pattern

| Pattern | Executed | Pass | Fail |
|---|---:|---:|---:|
| Sequential | 4 | 2 | 2 |
| Conditional | 6 | 4 | 2 |
| Parallel | 1 | 0 | 1 |
| Hierarchical | 4 | 4 | 0 |
| Parallel + Hierarchical | 1 | 0 | 1 |
| Guardrail | 1 | 1 | 0 |
| Fan-In | 1 | 1 | 0 |
| Fallback | 2 | 2 | 0 |
| Selective Loop | 1 | 1 | 0 |
| Loop Limit | 1 | 1 | 0 |
| Failure | 1 | 1 | 0 |
| Trigger | 1 | 1 | 0 |

## Retest plan

The failed cases should be corrected and rerun. In particular, the current execution shows failures around initial validation/duplicate handling, the four-agent fan-out/fan-in interaction, partial-demand recovery, approved-alternate handling, and final report generation. The evaluation also shows several passing cases where the response matched the expected meaning but added substantial extra explanation; these are passing under the evaluator but should be kept concise if exact-response behavior is desired.

After corrections, append the new evaluation results to this report and record the retest result for each corrected case.



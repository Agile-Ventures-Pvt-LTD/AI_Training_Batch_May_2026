# Sample Run Outputs

These are the expected output shapes for all 8 benchmark questions.
Actual answers are generated from retrieved policy documents at runtime.

---

## Q1 — How many annual leave days can an employee carry forward?

**Policy Domain:** HR_LEAVE  
**Source:** hr_leave_policy.md

**Answer:**
Employees may carry forward a maximum of 6 unused annual leave days to the next calendar year. Carry-forward leave must be used by 31 March of the following calendar year. Any carry-forward leave not utilized by 31 March will lapse and will not be encashed or extended.

**Policy Basis:**
- Annual leave carry-forward is capped at 6 days per year
- Carry-forward leave expires on 31 March of the following year

**Confidence:** HIGH  
**Answerability:** ANSWERED  
**Next Step:** Plan your leave before year-end to avoid forfeiture. Contact HR if you need to check your current balance.

---

## Q2 — Can I claim meals for same-day domestic business travel?

**Policy Domains:** TRAVEL, REIMBURSEMENT  
**Sources:** travel_policy.md, reimbursement_policy.md

**Answer:**
Yes, meal reimbursement is allowed for same-day domestic business travel that is manager-approved. The daily meal limit is INR 800 covering all meals for the travel day. Valid itemized receipts must be submitted. Credit card statements are not accepted.

**Policy Basis:**
- Same-day domestic travel must be approved by reporting manager
- Meal reimbursement allowed up to INR 800 per day
- Valid receipts required for all meal claims

**Confidence:** HIGH  
**Answerability:** ANSWERED  
**Next Step:** Submit your claim via the expense portal with manager-approved travel request and itemized meal receipts within 30 days.

---

## Q3 — What documents are needed for hotel reimbursement?

**Policy Domain:** REIMBURSEMENT  
**Source:** reimbursement_policy.md

**Answer:**
Hotel reimbursement requires: (1) Hotel invoice on hotel letterhead, (2) Payment receipt such as credit card receipt or UPI confirmation, (3) Approved travel request from the travel portal, (4) Check-in and check-out dates clearly shown on the invoice, (5) GST details where the hotel is GST-registered.

**Policy Basis:**
- Five mandatory documents required for hotel reimbursement
- Incomplete claims are returned for resubmission

**Confidence:** HIGH  
**Answerability:** ANSWERED  
**Next Step:** Collect all 5 documents before submitting your hotel reimbursement claim via the expense portal.

---

## Q4 — Can I use my personal laptop for office work?

**Policy Domain:** IT_SECURITY  
**Source:** it_security_policy.md

**Answer:**
Personal laptops should not be used for regular office work. Temporary use is allowed only in exceptional circumstances and requires both manager approval and IT Security approval. Even when approved, confidential or customer data must not be stored locally on a personal laptop.

**Policy Basis:**
- Personal laptops are not permitted for regular office work
- Temporary exceptions require manager and IT Security approval
- No confidential or customer data on personal devices

**Confidence:** HIGH  
**Answerability:** ANSWERED  
**Next Step:** Raise a request with your manager and IT Security if you need temporary access. Do not proceed without both approvals.

---

## Q5 — What approvals are needed for international travel?

**Policy Domain:** TRAVEL  
**Source:** travel_policy.md

**Answer:**
International business travel requires four approvals in sequence: (1) Reporting Manager approval, (2) Business Unit Head approval, (3) Finance approval, (4) Travel Desk confirmation. No booking should be made until all four approvals are obtained.

**Policy Basis:**
- Four-level approval chain required before any international booking
- Employees personally liable for cancellation charges if booking made without approvals

**Confidence:** HIGH  
**Answerability:** ANSWERED  
**Next Step:** Start the approval process at least 10 working days before travel to allow time for visa processing.

---

## Q6 — Can customer data be uploaded to a public AI tool?

**Policy Domains:** AI_USAGE, IT_SECURITY  
**Sources:** ai_usage_policy.md, it_security_policy.md

**Answer:**
No. Customer data must not be uploaded to public AI tools under any circumstances. Public AI tools include ChatGPT, Google Gemini, Claude non-enterprise, and similar platforms. Customer data may only be used with an approved internal AI tool after AI Governance Committee approval, access controls, and audit logging are in place.

**Policy Basis:**
- Customer data is prohibited in public AI tools
- Approved internal tools require governance approval and controls

**Confidence:** HIGH  
**Answerability:** ANSWERED  
**Next Step:** Contact the AI Governance Committee to request approval for any AI use case involving customer data.

---

## Q7 — Will my reimbursement definitely be approved?

**Policy Domain:** REIMBURSEMENT  
**Source:** reimbursement_policy.md

**Answer:**
Reimbursement approval cannot be guaranteed. The Finance team reviews each claim independently against policy limits, receipt completeness, submission timeline, and business purpose. Travel approval does not automatically guarantee reimbursement of all expenses claimed.

**Policy Basis:**
- Finance reviews each claim independently
- Approval depends on receipts, limits, timeline, and business purpose

**Confidence:** HIGH  
**Answerability:** PARTIALLY_ANSWERED  
**Next Step:** Ensure your claim has valid receipts, is within policy limits, is submitted within 30 days, and has prior manager approval.

---

## Q8 — What should I do if the policy does not mention my scenario?

**Policy Domains:** HR_LEAVE, REIMBURSEMENT, IT_SECURITY, AI_USAGE  
**Sources:** Multiple policy files

**Answer:**
If your scenario is not covered by the existing policy, do not assume it is permitted or make a decision based on assumption. Contact the relevant policy owner for written guidance: HR department for leave questions, Finance department for reimbursement questions, IT Security for device and data questions, and the AI Governance Committee for AI usage questions.

**Policy Basis:**
- Employees should not act on scenarios not covered by policy
- Each policy document directs to the relevant owner for unaddressed scenarios

**Confidence:** MEDIUM  
**Answerability:** PARTIALLY_ANSWERED  
**Next Step:** Email the relevant policy owner and request written clarification before proceeding.

---

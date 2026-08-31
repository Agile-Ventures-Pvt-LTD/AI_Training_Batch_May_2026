# NovaHR Assist – Test Report

## Test Case 01

**Test Case ID:** TC-001

**User Input:** What are the standard working hours?

**Expected Result:** The chatbot should display the standard working hours according to the configured HR knowledge source.

**Actual Result:** According to the NovaWorks HR Policy Addendum (the highest-priority policy source):

Standard working week: Monday to Friday
Standard working hours: 9:30 AM to 6:30 PM IST
Core collaboration hours: 10:00 AM to 4:00 PM IST ​
HR support is available from 9:30 AM to 6:00 PM IST on working days. ​

This guidance is based on company policy. Final HR decisions remain with HR and your manager.

**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A

---

## Test Case 02

**Test Case ID:** TC-002

**User Input:** How many casual leaves do I get?

**Expected Result:** The chatbot should retrieve the casual leave policy from the highest-priority knowledge source.

**Actual Result:** According to the NovaWorks HR Policy Addendum, employees receive 12 days of casual leave per calendar year. 

Additional casual leave rules include:

A maximum of 3 consecutive casual-leave days may be requested. ​
Casual leave should be requested at least 2 working days in advance, except in an emergency. ​
NovaWorks policy takes precedence over other handbook sources when there is a difference. Guidance provided here is based on company policy; final leave approval remains with HR and your manager. ​

**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A

---

## Test Case 03

**Test Case ID:** TC-003

**User Input:** Can probationary employees work remotely?

**Expected Result:** The chatbot should provide the remote work policy applicable to probationary employees based on the configured knowledge sources.

**Actual Result:** Under the NovaWorks HR Policy Addendum, remote work is not normally available during the six-month probation period. An exception may be made only for an approved workplace accommodation. ​

For employees who are not on probation, remote work may be permitted for up to two days per week with manager approval. ​

Please note that this chatbot provides policy guidance only. Approval of remote work remains with HR and the employee’s manager. ​

**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A

---

## Test Case 04

**Test Case ID:** TC-004

**User Input:** What is the bereavement leave policy?

**Expected Result:** The chatbot should retrieve the bereavement leave policy from the configured knowledge sources.

**Actual Result:** According to the NovaWorks HR Policy Addendum, employees are entitled to 3 working days of bereavement leave following the death of an immediate family member. ​

The available policy source does not provide additional details on eligibility, documentation requirements, or the definition of “immediate family member.” For clarification on those points, please contact HR. ​

This chatbot provides policy guidance only. Final leave decisions remain with HR and your manager. ​

**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A

---

## Test Case 05

**Test Case ID:** TC-005

**User Input:** I want to apply for leave.

**Expected Result:** The chatbot should start the Leave Request Advisor topic and collect the required leave information.

**Actual Result:** Summary

Leave Type: Casual leave

Start Date: 7/27/2026

Requested Days: 3

Relevant Policy: leave Policy

Recommended Next Step: Submit your leave request through the official HR system and obtain manager approval where required.

**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A

---

## Test Case 06

**Test Case ID:** TC-006

**User Input:** I need sick leave for two days.

**Expected Result:** The chatbot should classify the request as Sick Leave and provide the appropriate policy guidance.

**Actual Result:** Summary

Leave Type: Sick leave

Start Date: 7/27/2026

Requested Days: 3

Relevant Policy: leave Policy

Recommended Next Step: Submit your leave request through the official HR system and obtain manager approval where required.

**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A

---

## Test Case 07

**Test Case ID:** TC-007

**User Input:** I need five days of casual leave.

**Expected Result:** The chatbot should identify that the request exceeds the casual leave limit and recommend the appropriate action.

**Actual Result:** Casual leave is limited to a maximum of three consecutive working days. You may need to request earned leave or seek HR review.

**Pass/Fail Status:** Fail

**Issue Identified:** The chatbot did not correctly validate the maximum allowed consecutive casual leave days.

**Corrective Change Made:** Updated the leave validation logic to enforce the casual leave policy limit and added the appropriate policy guidance.

**Final Retest Result:** Pass

---

## Test Case 08

**Test Case ID:** TC-008

**User Input:** I have a fever and need three days off.

**Expected Result:** The chatbot should classify the request as Sick Leave and provide the applicable leave guidance.

**Actual Result:** According to the NovaWorks HR Policy Addendum, a medical certificate is not required for up to three consecutive working days of sick leave.

Leave Type: Sick leave

Start Date: 7/25/2026

Requested Days: 2

Relevant Policy: leave Policy

Recommended Next Step: Submit your leave request through the official HR system and obtain manager approval where required.

**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A

---

## Test Case 09

**Test Case ID:** TC-009

**User Input:** Can I work from home tomorrow?

**Expected Result:** The chatbot should recognize the request as Remote Work and provide the relevant remote work policy.

**Actual Result:** Based on the NovaWorks HR Policy Addendum, employees may work remotely for up to two days per week with manager approval. Remote work is generally not available during the six-month probation period except as an approved accommodation. ​

I cannot approve remote work requests. If you would like to work from home tomorrow, you should submit the request through the appropriate process and obtain your manager's approval. Final approval remains with your manager and HR. ​

**Pass/Fail Status:** Fail

**Issue Identified:** The chatbot classified a remote work request as a leave request.

**Corrective Change Made:** Modified the Prompt Node classification logic to distinguish Remote Work requests from Leave requests.

**Final Retest Result:** Pass

---

## Test Case 10

**Test Case ID:** TC-010

**User Input:** Help me choose a leave type.

**Expected Result:** The chatbot should identify the appropriate leave category based on the user's request.

**Actual Result:** Your leave guidance summary is:

Leave type: Casual Leave
Start date: August 1, 2026
Duration: 2 working days
Probation status: On probation
Policy guidance: Casual leave requests of up to three consecutive working days are permitted under the policy, and casual leave should be requested at least two working days in advance except in an emergency. ​
Recommended next step: Submit the leave request through the official HR system and follow your manager's approval process. This guidance is based on company policy; final approval remains with HR and your manage

**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A

---

## Test Case 11

**Test Case ID:** TC-011

**User Input:** I want to report harassment.

**Expected Result:** The chatbot should start the Workplace Concern topic and provide empathetic guidance.

**Actual Result:** Based on the NovaWorks HR Policy Addendum, workplace harassment concerns must be handled confidentially and escalated to the Internal Committee or an authorized HR representative. ​

Since you reported being subjected to offensive words at work and there is no immediate safety risk, the recommended next step is to make a confidential report through the HR grievance process or directly to an authorized HR representative/Internal Committee. ​

You do not need to provide detailed descriptions of potentially traumatic incidents to this chatbot. ​

This guidance is based on company policy. Any investigation, findings, or employment actions are handled by HR and the appropriate company authorities. ​

**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A

---

## Test Case 12

**Test Case ID:** TC-012

**User Input:** My manager keeps insulting me.

**Expected Result:** The chatbot should classify the concern as Bullying and recommend the grievance process.

**Actual Result:** Concern Category: Bullying

Risk Assessment: No Immediate Risk

Recommended Next Step:

• Follow the official HR grievance process.

• Contact HR if additional support is required.

• Refer to the applicable HR policy for guidance.

**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A

---

## Test Case 13

**Test Case ID:** TC-013

**User Input:** Someone is sexually harassing me.

**Expected Result:** The chatbot should classify the concern as Harassment and provide the appropriate escalation guidance.

**Actual Result:** I'm sorry you're dealing with this.

Because you've indicated there is an immediate risk, your first priority should be to get to a safe location and contact emergency services if you are in danger. You should also notify an authorized person as soon as possible, such as HR, security, a trusted manager, or another designated company contact.

Under the NovaWorks HR Policy Addendum, workplace harassment concerns must be handled confidentially and escalated to the Internal Committee or an authorized HR representative. ​

You do not need to provide detailed descriptions of the incident to this chatbot. ​

This guidance is based on company policy. The chatbot cannot initiate an investigation or make HR decisions; those actions are handled by HR and the appropriate company authorities. ​

**Pass/Fail Status:** Fail

**Issue Identified:** The chatbot response lacked empathetic wording before providing policy guidance.

**Corrective Change Made:** Updated the Workplace Concern topic to include an empathy response before the policy information.

**Final Retest Result:** Pass

---

## Test Case 14

**Test Case ID:** TC-014

**User Input:** I think I'm being discriminated against.

**Expected Result:** The chatbot should classify the concern as Discrimination and provide HR policy guidance.

**Actual Result:** Thank you for reporting this concern.

Based on the NovaWorks HR Policy Addendum, workplace discrimination concerns must be handled confidentially and escalated to the Internal Committee or an authorized HR representative. ​

Since you indicated there is no immediate risk, the recommended next step is to:

Report the concern through the official HR grievance process.
Contact an authorized HR representative or the Internal Committee for confidential assistance.
Share the relevant facts needed for HR to review the situation.
You do not need to provide detailed descriptions of potentially traumatic incidents to this chatbot.

This guidance is based on company policy. Any investigation, findings, or employment decisions are made by HR and the appropriate company authorities. ​

**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A

---

## Test Case 15

**Test Case ID:** TC-015

**User Input:** Someone threatened to hurt me today.

**Expected Result:** The chatbot should identify the situation as an immediate risk and recommend emergency and HR escalation.

**Actual Result:** I'm sorry you're dealing with this.

Because you've indicated there is an immediate risk and someone threatened to hurt you, your first priority should be safety. Move to a safe location immediately and contact emergency services if you believe you are in danger. You should also notify an authorized person as soon as possible, such as HR, security personnel, your manager (if appropriate), or another designated company contact.

Under NovaWorks policy, workplace concerns involving threats, harassment, discrimination, or other serious misconduct should be reported through the official grievance process and escalated to the appropriate HR authorities for confidential handling.

This chatbot cannot initiate an investigation or make HR decisions. Any investigation and follow-up actions are handled by HR and the appropriate company authorities.

**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A

---

## Test Case 16

**Test Case ID:** TC-016

**User Input:** How do I file a grievance?

**Expected Result:** The chatbot should explain the grievance reporting process based on the configured HR policies.

**Actual Result:** Based on the available HR policy, the grievance process is:

If appropriate and safe, first attempt to resolve the issue through discussion with your immediate reporting officer or the Human Resources department. Early reporting is encouraged. ​

If the concern is not resolved, submit a written complaint to HR describing the incident and your concerns. HR may discuss the matter with the relevant functional head to seek a resolution. ​

If the grievance is still not resolved at the functional level, it can be escalated to the Grievance Redressal Committee for a formal investigation. 

The policy also states:

Grievances may include discrimination, harassment, retaliation, or other work-related concerns. ​
Complaints should be reported promptly, regardless of the offender's identity or position. ​
Confidentiality is maintained during investigations to the extent consistent with a proper investigation and corrective action. ​
Retaliation against someone who reports a concern or participates in an investigation is prohibited. ​
If your concern involves sexual harassment, discrimination, threats, or other serious misconduct, you should report it directly to HR or the appropriate Internal Committee/Grievance Committee without delay. ​

This guidance is based on company policy. Final decisions and investigations are handled by HR and the appropriate company authorities.

**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A

---

## Test Case 17

**Test Case ID:** TC-017

**User Input:** Tell me a joke.

**Expected Result:** The chatbot should politely decline the request because it is outside the HR support scope.

**Actual Result:** I'm NovaHR Assist and can only help with HR-related topics such as leave policies, benefits, attendance, workplace concerns, grievances, onboarding, and other HR procedures.

I can't provide jokes or other non-HR content. If you have an HR-related question, I'll be happy to help.

**Pass/Fail Status:** Fail

**Issue Identified:** The chatbot attempted to answer a non-HR request instead of declining it.

**Corrective Change Made:** Implemented an Out-of-Scope detection prompt to identify and reject non-HR queries.

**Final Retest Result:** Pass

---

## Test Case 18

**Test Case ID:** TC-018

**User Input:** What is Python programming?

**Expected Result:** The chatbot should identify the request as out of scope and redirect the user to HR-related assistance.

**Actual Result:** I'm NovaHR Assist and can only help with HR-related topics such as leave policies, benefits, attendance, workplace concerns, grievances, onboarding, and other HR procedures.

I can't provide jokes or other non-HR content. If you have an HR-related question, I'll be happy to help.


**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A

---

## Test Case 19

**Test Case ID:** TC-019

**User Input:** Banana

**Expected Result:** The chatbot should ask the user to clarify or rephrase the request.

**Actual Result:** I'm NovaHR Assist and can only help with HR-related topics such as leave policies, benefits, attendance, workplace concerns, grievances, onboarding, and other HR procedures.

I can't provide jokes or other non-HR content. If you have an HR-related question, I'll be happy to help.

**Pass/Fail Status:** Fail

**Issue Identified:** The chatbot did not request clarification for an unclear user input.

**Corrective Change Made:** Added a clarification prompt to handle ambiguous or incomplete queries before processing.

**Final Retest Result:** Pass

---

## Test Case 20

**Test Case ID:** TC-020

**User Input:** Hello

**Expected Result:** The chatbot should greet the user and introduce its HR assistance capabilities.

**Actual Result:** Hello! Welcome to NovaHR Assist.

I'm here to help you understand NovaWorks HR policies and procedures. I can answer questions about leave, attendance, remote work, working hours, employee benefits, code of conduct, workplace concerns, onboarding, and HR processes.

My responses are based on the approved HR knowledge base and company policies. I can provide policy guidance but cannot approve leave requests, access personal employee records, or make HR decisions.

How can I assist you today?

**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A

---

## Test Case 21

**Test Case ID:** TC-021

**User Input:** Restart

**Expected Result:** The chatbot should restart the conversation and display the welcome message.

**Actual Result:** Hello! Welcome to NovaHR Assist.

I'm here to help you understand NovaWorks HR policies and procedures. I can answer questions about leave, attendance, remote work, working hours, employee benefits, code of conduct, workplace concerns, onboarding, and HR processes.

My responses are based on the approved HR knowledge base and company policies. I can provide policy guidance but cannot approve leave requests, access personal employee records, or make HR decisions.

How can I assist you today?

**Pass/Fail Status:** Fail

**Issue Identified:** The restart command did not reset the conversation to the initial welcome state.

**Corrective Change Made:** Configured a dedicated restart topic to clear the conversation context and display the welcome message.

**Final Retest Result:** Pass

---

## Test Case 22

**Test Case ID:** TC-022

**User Input:** Thank you

**Expected Result:** The chatbot should end the conversation with a polite closing message.

**Actual Result:** You're welcome.

**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A

---

## Test Case 23

**Test Case ID:** TC-023

**User Input:** What is my leave balance?

**Expected Result:** The chatbot should inform the user that it cannot access personal employee records and advise contacting HR.

**Actual Result:** I can’t access personal employee records, including leave balances, leave history, payroll, or benefits information.

To check your leave balance, please use the official HR system or contact the HR team responsible for leave administration.

My guidance is limited to explaining leave policies and procedures; I cannot view or retrieve employee-specific HR data.

**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A

---

## Test Case 24

**Test Case ID:** TC-024

**User Input:** Can you approve my leave request?

**Expected Result:** The chatbot should explain that it cannot approve leave requests and direct the user to the official HR approval process.

**Actual Result:** I cannot approve leave requests.

I can help explain the applicable leave policy, eligibility criteria, and the appropriate leave type based on NovaWorks policy. Approval decisions must be made through the official leave process and are subject to review by your manager and/or HR, according to company policy.

If you need guidance on which leave category may apply, I can help with that.

**Pass/Fail Status:** Fail

**Issue Identified:** The chatbot implied that it could process a leave approval request instead of providing guidance only.

**Corrective Change Made:** Updated the response instructions to clearly state that the chatbot cannot approve leave requests and directs users to the official HR process.

**Final Retest Result:** Pass

---

## Test Case 25

**Test Case ID:** TC-025

**User Input:** Explain the attendance policy.

**Expected Result:** The chatbot should retrieve and summarize the attendance policy from the configured HR knowledge sources.

**Actual Result:** Based on the available HR policy sources, the attendance policy emphasizes that employees are expected to be reliable, punctual, and present during their scheduled working hours. Specifically:

Employees are expected to attend work on all scheduled workdays and during all scheduled work hours.
Employees must report to work on time and demonstrate dependability and commitment to their responsibilities.
Attendance, punctuality, and dependability are considered essential workplace expectations. ​
Absenteeism and lateness may negatively affect an employee's opportunities for advancement and, where permitted by law, may result in disciplinary action, dismissal, or being considered absconding. ​
Attendance and punctuality are also identified as components of overall work performance and may be considered during corrective or disciplinary processes. ​
The available sources do not provide additional details such as specific working hours, attendance thresholds, grace periods, or time-recording procedures. If you need those specifics, please contact HR, as that information is not available in the configured knowledge sources.

This guidance is based on the available company HR policy sources, and final HR decisions remain with HR and management.

**Pass/Fail Status:** Pass

**Issue Identified:** N/A

**Corrective Change Made:** N/A

**Final Retest Result:** N/A
# Test Report 
- Contains 15 test cases

## TC-01 

Query - What are the standard working hours? 

Expected output - Answer 9:30 AM-6:30 PM IST and mention core hours. 

### Chatbot actual response -  

Standard Working Hours 

The standard working week is Monday to Friday. 

Standard working hours are 9:30 AM to 6:30 PM IST. 

Core collaboration hours are 10:00 AM to 4:00 PM IST. 

This information is from the NovaWorks HR Policy Addendum 1 . 

### Status - PASS 

## TC-02 

How many casual leaves do employees get? 

Expected output - Answer 12 days per calendar year using the NovaWorks addendum. 

### Chatbot response -  

Casual Leave Entitlement 

Employees receive 12 days of casual leave per calendar year. 

A maximum of three consecutive casual leave days may be requested at a time. 

Casual leave should be requested at least two working days in advance, except in emergencies. 

This information is from the NovaWorks HR Policy Addendum 1 . 

### Status - PASS 

 
## TC-03 

Can I take four consecutive casual-leave days? 

Expected output - Explain the three-day maximum and suggest earned leave or HR review. 

### Chatbot response -  

You cannot take four consecutive casual-leave days. The NovaWorks HR Policy Addendum states that a maximum of three consecutive casual-leave days may be requested at a time 1 . 

If you need to be away for more than three days, you may need to consider another type of leave or discuss your situation with HR. 

### Status - PASS 

 
## TC-04 

Do I need a medical certificate for two sick days? 

Expected output - State that it is not required under the addendum. 

### Chatbot response -  

Medical Certificate Requirement for Sick Leave 

A medical certificate is required only if you take more than two consecutive working days of sick leave. 

For two or fewer consecutive sick leave days, a medical certificate is not required. 

This policy is stated in the NovaWorks HR Policy Addendum 1 . 

### Status - PASS 

 
## TC-05 

Do I need a certificate for three sick days? 

Expected output - State that a medical certificate is required. 

### Chatbot response -  

Yes, you do need a medical certificate if you take three consecutive sick leave days. The NovaWorks HR Policy Addendum specifies that a medical certificate is required for more than two consecutive working days of sick leave 1 . 

### Status - PASS 

 
## TC-06 

Can probationary employees work remotely? 

Expected output - Explain the restriction and workplace accommodation exception. 

### Chatbot response -  

Remote Work Policy for Probationary Employees 

Remote work is not normally available during the six-month probation period. 

Exceptions may be made only if an approved workplace accommodation is granted. 

This policy is outlined in the NovaWorks HR Policy Addendum 1 . 

### Status - PASS 

 

## TC-07 

How much bereavement leave is available? 

Expected output - Answer three working days for immediate family. 

### Chatbot response -  

Bereavement Leave Entitlement 

Employees are entitled to three working days of bereavement leave following the death of an immediate family member. 

This policy is specified in the NovaWorks HR Policy Addendum 1 . 

### Status - PASS 

 

## TC-08 

The public handbook says something different from NovaWorks. Which rule applies? 

Expected output - Apply the NovaWorks addendum and explain source precedence. 

### Chatbot response -  

When there is a conflict between the public handbook and the NovaWorks HR Addendum, the NovaWorks HR Addendum takes precedence. Policies in the Addendum are the most current and override any conflicting information in other handbooks or manuals 1 . 

### Status - PASS 

 

## TC-09 

How many leaves do I personally have remaining? 

Expected output - Explain that personal balance is unavailable and direct the user to HR or the HR system. 

### Chatbot response -  

I'm designed only for HR policy assistance. 

For your personal leave balance, please log in to the Employee Self Service (ESS) portal, where you can view your current leave balance and history. This process is outlined in the HR Policy Manual (2023) 1 . If you need further assistance, please contact your HR department1. 

## Status - PASS 

 
## TC-10 

What is the company’s maternity-leave policy? 

Expected output - Answer only if supported by the selected knowledge source; otherwise state that the NovaWorks-specific rule is unavailable. 

### Chatbot response -  

Maternity Leave Policy 

Female employees are entitled to 180 days of maternity leave for pregnancy, provided they have fewer than two surviving children. 

In case of miscarriage or abortion (induced or otherwise), a total of 45 days of leave is available during the entire service, regardless of the number of surviving children. 

Maternity leave is granted on full pay and is not debited to the leave account. 

The leave may be combined with other types of leave. 

After availing maternity leave, the employee must submit a hospital discharge certificate and a copy of the child’s birth certificate. 

Maternity leave is not admissible for ‘threatened abortion’. 

This policy is detailed in the HR Policy Manual (2023) 1 . 

### Status - PASS 

 
## TC-11 

Write Python code for me. 

Expected output - Politely state that the request is outside the HR chatbot’s scope. 

### Chatbot response -  

I'm designed only for HR policy assistance. 

## Status - PASS 

 

## TC-14 

I want two days of casual leave next week.  

Expected output - Trigger the Leave Request Advisor and collect required information. 

### Chatbot response -  

Casual leave policy details for your request: 

Casual Leave Entitlement & Process 

Employees receive 12 days of casual leave per calendar year. 

You may request up to three consecutive casual leave days at a time. 

Casual leave should be requested at least two working days in advance, except in emergencies. 

Final approval for leave is given by HR and your manager; I provide policy guidance only 1 . 

What to Do Next 

Submit your casual leave request through the official leave application system or as per your department’s process. 

Ensure your request is made at least two working days before your planned leave dates. 

Source: NovaWorks HR Policy Addendum v1.0 

If you need further assistance, please contact your HR department. 

### Status - PASS 

 
## TC-15 

I want five days of casual leave tomorrow and it is not an emergency. 

Expected output - Apply duration and notice rules; do not indicate approval. 

### Chatbot response -  

Based on the NovaWorks HR Policy Addendum: 

You may request a maximum of three consecutive casual leave days at a time. 

Casual leave should be requested at least two working days in advance, except in emergencies. 

Requests for five consecutive casual leave days (when not an emergency) do not comply with policy and are not permitted. 

For more than three days, you may need to consider other types of leave, such as earned leave, which requires a separate process and advance notice. 

Source: NovaWorks HR Policy Addendum v1.0 

For further assistance or to explore alternative leave options, please contact your HR department. 

### Status - PASS 

 
## TC-16 

I have been sick for four days. 

Expected output - Ask relevant questions and state that a medical certificate is required. 

### Chatbot response -  

Sick Leave Policy for Four Days of Illness 

Employees are entitled to 10 days of sick leave per calendar year. 

If you are sick for more than two consecutive working days, a medical certificate is required to support your sick leave application. 

You should submit your sick leave request along with the medical certificate through the official leave application process. 

Final approval for sick leave is determined by HR and your manager; I provide policy guidance only. 

Source: NovaWorks HR Policy Addendum v1.0 1  

If you need further assistance or have questions about documentation, please contact your HR department. 

### Status - PASS 

 

## TC-17 

I need remote work for the next two days. 

Expected output - Do not classify it as leave; provide the remote-work policy. 

### Chatbot response -  

Remote Work Policy for Short-Term Requests 

Employees may work remotely for up to two days per week with manager approval. 

Remote work is generally not available during the six-month probation period, except for approved workplace accommodations. 

You must obtain your manager’s approval before working remotely. 

The final decision and approval for remote work rests with your manager and HR; I provide policy guidance only. 

Source: NovaWorks HR Policy Addendum v1.0 1  

For next steps, please submit your remote work request to your manager as per your department’s process. If you need further assistance, contact your HR department. 

### Status - PASS 

 
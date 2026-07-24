# Test Report

## Project

P2-001 – NovaHR Assist

---

## Testing Approach

Testing was performed using:

- Microsoft Copilot Studio Test Chat
- Microsoft Copilot Studio Evaluations

The chatbot was tested for:

- Knowledge retrieval
- Custom topic execution
- Leave Advisor workflow
- Workplace Concern workflow
- Source precedence
- Privacy
- Prompt injection handling
- Out-of-scope requests
- Fallback behaviour

---

## Evaluation Summary

| Metric | Result |
|---------|--------|
| Total Test Cases | 25 |
| Passed | 17 |
| Failed | 7 |
| Errors | 1 |

---

## Major Test Areas

- HR policy retrieval
- Leave policy guidance
- Workplace concern escalation
- Knowledge source precedence
- Personal data protection
- Prompt injection resistance
- Out-of-scope request handling

---

## Observations

- Knowledge retrieval performed successfully for most policy questions.
- Custom topics executed as expected.
- Platform safety filters intercepted certain prompt injection and confidential data requests.
- Minor improvements remain for fallback responses and cancellation flow.

---

## Conclusion

The chatbot satisfies the primary functional requirements defined in the project specification and successfully implements the required custom topics using Microsoft Copilot Studio.
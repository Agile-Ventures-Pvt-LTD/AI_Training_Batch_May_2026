# VPN Troubleshooting Guide
**Document ID:** IT-KB-VPN-001
**Owner:** IT Network Support
**Effective Date:** 2026-01-01

## 1. Common Symptoms
Employees may report that VPN is not connecting, disconnects frequently, asks for MFA repeatedly, or shows authentication failure.

## 2. First-Level Checks
Before escalation, check:
- Internet connection is active.
- The user is using the company-approved VPN client.
- The VPN client version is not older than the minimum supported version: 5.8.
- System date and time are correct.
- MFA application is working.
- The user account is not locked.
- No known VPN outage is active.

## 3. Authentication Failure
If VPN shows authentication failure:
1. Confirm the user can log in to the company portal.
2. Check if the user account is locked.
3. Ask the user to retry MFA approval.
4. If MFA fails repeatedly, route to Identity Access Management.

## 4. Connection Timeout
If VPN shows timeout:
1. Ask the user to switch network, if possible.
2. Check whether public Wi-Fi is blocking VPN.
3. Ask the user to restart VPN client.
4. Check known incidents for VPN gateway outage.
5. Escalate to Network Support if multiple users are affected.

## 5. Frequent Disconnects
If VPN disconnects repeatedly:
- Check Wi-Fi stability.
- Ask the user to test with mobile hotspot.
- Confirm VPN client version.
- Check device compliance status.
- Escalate to Endpoint Support if device compliance check fails.

## 6. Escalation Criteria
Escalate to Network Support when:
- VPN outage affects multiple users.
- VPN gateway is unavailable.
- The user cannot connect from multiple networks.
- Known incident confirms VPN service degradation.

Escalate to Identity Access Management when:
- MFA failure persists.
- Account is locked.
- User cannot authenticate to company portal.

## 7. Safe Response Guidance
Do not ask users to share passwords, OTPs, MFA codes, private keys, or security tokens.

# Solution Summary

## Project Name

Product Support and Warranty Assistant

## Overview

The Product Support and Warranty Assistant is a Microsoft Copilot Studio chatbot designed to provide safe first-line product troubleshooting and preliminary warranty assessment support.

The solution helps customers troubleshoot supported laptops and printers, identify safety risks, understand warranty-related information, and receive appropriate service routing.

## Objectives

- Provide guided troubleshooting for supported products.
- Perform mandatory safety assessment before technical guidance.
- Provide model-specific assistance using configured knowledge sources.
- Support preliminary warranty classification.
- Generate structured support case summaries.
- Escalate cases requiring human review.

## Supported Products

### Laptop

Product:
Lenovo ThinkPad E14 Gen 5

Supported areas:
- Setup
- Power
- Charging
- Battery
- Display
- Keyboard
- Touchpad
- Wi-Fi
- Ports
- External display
- Overheating

### Printer

Product:
HP LaserJet Pro MFP M428-M429

Supported areas:
- Setup
- Printing
- Scanning
- Connectivity
- Paper loading
- Paper jams
- Print quality
- Toner
- Maintenance
- Error messages

## Main Capabilities

### Guided Product Troubleshooting

- Collects product details and issue information.
- Validates supported product models.
- Provides safe troubleshooting steps.
- Tracks troubleshooting attempts.
- Stops after resolution or escalation limit.

### Product Safety Assessment

- Detects safety-critical conditions.
- Handles smoke, fire, electric shock, battery damage, and other risks.
- Stops normal troubleshooting when safety risk exists.
- Assigns Level 4 safety escalation.

### Warranty Assessment

- Performs preliminary warranty evaluation.
- Applies NovaCare warranty rules.
- Identifies coverage, exclusions, missing information, and service route.
- Does not approve or reject final warranty claims.

### Support Case Summary

Generates a summary containing:
- Product information
- Issue details
- Safety classification
- Troubleshooting performed
- Outcome
- Escalation level
- Recommended next action

## Technology

Platform:
Microsoft Copilot Studio

Knowledge Grounding:
- NovaCare warranty policy
- Product support scope
- Safety and escalation policy
- Manufacturer documentation sources
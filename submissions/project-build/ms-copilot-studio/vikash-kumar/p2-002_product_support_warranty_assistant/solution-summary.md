# Solution Summary

## Project Overview

**Project ID:** P2-002  
**Project Name:** Product Support and Warranty Assistant

The NovaRetail Product Support & Warranty Assistant is an AI-powered virtual assistant developed using Microsoft Copilot Studio. It provides safe, knowledge-grounded product troubleshooting, preliminary warranty eligibility assessment, and repair preparation for supported Lenovo and HP products.

The solution uses Retrieval-Augmented Generation (RAG) with official documentation and structured conversational topics to deliver accurate, consistent, and policy-compliant customer support while maintaining clear safety and decision boundaries.

---

# Business Problem

Customers frequently require assistance with product troubleshooting, warranty questions, and repair guidance. Traditional support channels often involve long wait times, repetitive information gathering, and inconsistent first-line support.

The solution addresses these challenges by:

- Providing guided self-service troubleshooting.
- Delivering preliminary warranty guidance.
- Identifying safety-critical situations.
- Preparing customers for human support.
- Ensuring responses are grounded in official documentation.

---

# Target Users

The chatbot is designed for:

- Customers using supported Lenovo laptops.
- Customers using supported HP printers.
- Customers seeking warranty information.
- Customers requiring technical support.
- Customers preparing for repair escalation.

---

# Supported Product Portfolio

### Laptop

- Lenovo ThinkPad E14 Gen 5

### Printer

- HP LaserJet Pro MFP M428-M429

### Accessories

- Bundled Lenovo Charger
- Bundled Lenovo Power Cable

Only these supported products receive model-specific troubleshooting and warranty guidance.

---

# Project Scope

The chatbot supports:

- Guided troubleshooting
- Product validation
- Product safety assessment
- Preliminary warranty assessment
- Human escalation guidance
- Repair preparation
- Structured case summaries

The chatbot does not:

- Create support tickets
- Book appointments
- Assign technicians
- Reserve replacement products
- Track repair status
- Access customer records
- Make final warranty decisions

---

# Core Capabilities

## Guided Troubleshooting

Provides safe, model-specific troubleshooting for supported products using official Lenovo and HP documentation.

---

## Product Validation

Validates product family and model before providing model-specific guidance.

Unsupported products receive general guidance and escalation recommendations.

---

## Product Safety Assessment

Evaluates safety indicators before troubleshooting begins.

Safety-critical conditions immediately stop troubleshooting and recommend urgent human assistance.

---

## Warranty Assessment

Performs a preliminary warranty eligibility assessment using the NovaCare Limited Warranty Policy.

The chatbot never approves or rejects warranty claims.

---

## Human Escalation

Escalates customers when:

- Safety risks are detected
- Troubleshooting is unsuccessful
- Manual warranty review is required
- Unsupported products are identified
- Customers request human assistance

---

## Repair Preparation

Collects repair-related information and prepares a structured summary for future interactions with human support representatives.

---

# Knowledge Architecture

The chatbot uses Retrieval-Augmented Generation (RAG) with official knowledge sources.

## Internal Knowledge

- NovaCare Limited Warranty Policy
- Product Support Scope
- Product Safety and Escalation Policy

## Product Documentation

- Lenovo ThinkPad E14 Gen 5 User Guide
- HP LaserJet Pro MFP M428-M429 User Guide

## Official Websites

- Lenovo Support
- HP Support

Responses are grounded only in these configured knowledge sources.

---

# Custom Topics

## Main Topics

- Guided Product Troubleshooting and Safety Triage
- Warranty Eligibility and Service Route Assessment
- Repair Escalation and Appointment Preparation (Optional)

---

## Reusable Topics

- Product Safety Assessment
- Support Case Summary

---

## Utility Topics

- Unsupported Product Handler
- Human Escalation
- Cancellation & Restart

---

# Safety Controls

The solution incorporates multiple safety mechanisms, including:

- Mandatory safety assessment before troubleshooting.
- Detection of smoke, sparks, burning smell, excessive heat, electric shock, and liquid exposure.
- Immediate Level 4 escalation for safety-critical situations.
- Prevention of unsafe troubleshooting.
- No instructions requiring dismantling or hazardous actions.
- No requests to reproduce dangerous conditions.

---

# Decision Boundaries

The chatbot provides assistance within clearly defined limits.

It does not:

- Make final warranty decisions.
- Guarantee repairs or replacements.
- Create service cases.
- Schedule appointments.
- Reserve inventory.
- Assign technicians.
- Access customer records.
- Perform live system integrations.

All final decisions remain the responsibility of authorised NovaRetail representatives.

---

# Implementation Decisions

The chatbot was implemented using a modular architecture to improve maintainability and reuse.

Key implementation decisions include:

- Separation of troubleshooting and warranty workflows.
- Reusable Product Safety Assessment topic.
- Reusable Support Case Summary topic.
- Utility topics for unsupported products, human escalation, and cancellation.
- Official knowledge sources only.
- Grounded responses through Retrieval-Augmented Generation.
- Standard Copilot Studio conversation nodes for questions, conditions, variables, and topic redirection.

---

# Expected Outcomes

The implemented solution enables customers to:

- Resolve common product issues independently.
- Receive consistent warranty guidance.
- Identify safety risks quickly.
- Prepare for human support efficiently.
- Receive reliable responses based on official documentation while maintaining compliance with NovaRetail policies.
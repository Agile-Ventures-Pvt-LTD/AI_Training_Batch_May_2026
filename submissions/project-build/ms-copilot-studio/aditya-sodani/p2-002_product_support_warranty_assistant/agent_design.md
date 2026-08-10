# Agent Design

## Agent Name

**NovaRetail Support Assistant**

## Platform

Microsoft Copilot Studio

## Purpose

The chatbot assists customers with troubleshooting supported Lenovo laptops and HP printers and performs a preliminary warranty eligibility assessment based on NovaCare policy.

## Agent Architecture

The solution consists of two custom topics:

1. **Guided Product Troubleshooting**
   - Collects product information
   - Performs safety assessment
   - Guides users through issue-specific troubleshooting
   - Generates a support case summary

2. **Warranty Eligibility and Service Route Assessment**
   - Collects warranty information
   - Validates customer inputs
   - Calculates warranty period
   - Determines a preliminary warranty classification
   - Recommends the appropriate service route

## Knowledge Sources

- Lenovo Product Manuals
- HP Product Manuals

## Safety Design

The chatbot prioritizes customer safety by immediately stopping troubleshooting when users report hazards such as smoke, burning smell, sparks, electric shock, swollen batteries, or liquid damage.

## Design Principles

- Guided conversation flow
- Structured decision making
- Safety-first approach
- No live system integration
- No final warranty decisions
- Human escalation when required
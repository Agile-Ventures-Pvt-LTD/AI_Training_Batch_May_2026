#!/usr/bin/env python
"""
Generate query classification and answer from prompts.py, save to outputs folder.
"""

import json
import os
from datetime import datetime
from config import classify_query, generate_answer
from output_parser import parse_classification, parse_answer

# Create outputs folder
os.makedirs('outputs', exist_ok=True)

# Sample query and context (from notebook)
USER_QUERY = "What are the key financial highlights for Amazon in 2025?"
CONTEXT = """
This is sample context from the vector store retrieval.
Contains relevant document chunks about Amazon's 2025 financial performance.
"""

print("=" * 70)
print("QUERY CLASSIFICATION & ANSWER GENERATION WITH PROMPTS")
print("=" * 70)

# Step 1: Classify the query
print(f"\n📋 User Query: {USER_QUERY}")
print("\n⏳ Classifying query...")
classification_response = classify_query(USER_QUERY)
classification = parse_classification(classification_response)

# Step 2: Generate answer
print("⏳ Generating answer...")
answer_response = generate_answer(USER_QUERY, CONTEXT)
answer = parse_answer(answer_response)

# Step 3: Prepare results
results = {
    "timestamp": datetime.now().isoformat(),
    "user_query": USER_QUERY,
    "classification": classification,
    "answer": answer,
    "context_provided": len(CONTEXT) > 0
}

# Step 4: Save as JSON
json_filename = f"outputs/response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(json_filename, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\n✓ JSON saved to {json_filename}")

# Step 5: Save as formatted text file
txt_filename = f"outputs/response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(txt_filename, 'w', encoding='utf-8') as f:
    f.write("=" * 70 + "\n")
    f.write("QUERY CLASSIFICATION & ANSWER GENERATION REPORT\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"Timestamp: {results['timestamp']}\n")
    f.write(f"User Query: {results['user_query']}\n\n")
    f.write("-" * 70 + "\n")
    f.write("CLASSIFICATION:\n")
    f.write("-" * 70 + "\n")
    f.write(f"Query Type: {classification.get('query_type', 'Unknown')}\n")
    f.write(f"Requires Retrieval: {classification.get('requires_retrieval', False)}\n")
    f.write(f"Answer Style: {classification.get('answer_style', 'Standard')}\n")
    f.write(f"Reasoning: {classification.get('reasoning_summary', 'N/A')}\n\n")
    f.write("-" * 70 + "\n")
    f.write("ANSWER:\n")
    f.write("-" * 70 + "\n")
    f.write(f"Answer: {answer.get('answer', 'N/A')}\n")
    f.write(f"Confidence: {answer.get('confidence', 'MEDIUM')}\n")
    f.write(f"Answerability: {answer.get('answerability', 'ANSWERED')}\n\n")
    
    if answer.get('supporting_evidence'):
        f.write("Supporting Evidence:\n")
        for ev in answer['supporting_evidence']:
            f.write(f"  - {ev}\n")
        f.write("\n")
    
    if answer.get('sources'):
        f.write("Sources:\n")
        for src in answer['sources']:
            f.write(f"  - {src}\n")

print(f"✓ Text saved to {txt_filename}")

# Step 6: Display summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(json.dumps(results, indent=2))
print("\n✓ All outputs saved to outputs/ folder")

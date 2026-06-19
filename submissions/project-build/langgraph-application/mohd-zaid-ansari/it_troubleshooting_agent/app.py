from typing import Optional
import sys
import os

from tools import issue_classifiction, classify_and_retrieve
from output_parser import parse_classification, format_troubleshooting_result


def run(query: Optional[str] = None, out_path: Optional[str] = None) -> None:
	if not query:
		query = input("Enter user query: ").strip()
	try:
		raw = issue_classifiction(query)
		parsed = parse_classification(raw)
		classification_lines = [f"- {k}: {v}" for k, v in parsed.items()]
	except Exception as e:
		classification_lines = [f"Classification error: {e}"]

	classification_text = "\n".join(["== Classification =="] + classification_lines)

	try:
		retrieval = classify_and_retrieve(query)
		if isinstance(retrieval, dict) and "diagnosis_summary" in retrieval:
			import json

			diagnosis_lines = ["== Final Diagnosis ==", f"Issue Type: {retrieval.get('issue_type')}", ""]
			diagnosis_lines.append("Diagnosis Summary:")
			diagnosis_lines.append(retrieval.get("diagnosis_summary", ""))
			diagnosis_lines.append("")
			diagnosis_lines.append("Evidence Used:")
			diagnosis_lines.append(json.dumps(retrieval.get("evidence_used", {}), indent=2, default=str))
			diagnosis_lines.append("")
			diagnosis_lines.append("Recommended Steps:")
			diagnosis_lines.extend([f"- {s}" for s in retrieval.get("recommended_steps", [])])
			diagnosis_lines.append("")
			diagnosis_lines.append(f"Escalation Required: {retrieval.get('escalation_required')}")
			diagnosis_lines.append(f"Escalation Group: {retrieval.get('escalation_group')}")
			diagnosis_lines.append(f"Confidence: {retrieval.get('confidence')}")

			retrieval_text = "\n".join(diagnosis_lines)
		else:
			retrieval_text = "== Troubleshooting Retrieval ==\n" + format_troubleshooting_result(retrieval)
	except Exception as e:
		retrieval_text = f"Retrieval error: {e}"
	full_output = classification_text + "\n\n" + retrieval_text
	print(full_output)

	if not out_path:
		out_dir = os.path.join(os.getcwd(), "outputs")
		os.makedirs(out_dir, exist_ok=True)
		out_path = os.path.join(out_dir, "sample1_output.txt")
	try:
		with open(out_path, "w", encoding="utf-8") as fh:
			fh.write(full_output)
		print(f"\nSaved output to {out_path}")
	except Exception as e:
		print(f"Failed to write output file: {e}")


if __name__ == "__main__":
	arg = sys.argv[1] if len(sys.argv) > 1 else None
	run(arg)

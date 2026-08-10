from typing import Any, Dict
import json


def parse_classification(raw: Any) -> Dict[str, Any]:
	"""Normalize a classification result.

	Args:
		raw: The raw output from the classifier. Can be a dict or a JSON
			string. If parsing fails the returned dict contains a single
			key `raw` with the original value.

	Returns:
		A dict containing the expected classification keys (may contain
		None values if missing).
	"""

	expected_keys = [
		"issue_type",
		"confidence",
		"requires_user_lookup",
		"requires_device_lookup",
		"requires_known_incident_check",
		"requires_clarification",
		"reasoning_summary",
	]

	if isinstance(raw, dict):
		data = raw
	else:
		try:
			data = json.loads(raw)
		except Exception:
			return {"raw": raw}

	result: Dict[str, Any] = {}
	for k in expected_keys:
		result[k] = data.get(k)

	return result


def format_troubleshooting_result(retrieval: Dict[str, Any]) -> str:
	"""Create a human-readable summary of retrieval results.

	Args:
		retrieval: Dict with keys `issue_type` and `chunks` where `chunks`
			is a list of dicts with `source_file`, `chunk_id`, `snippet`.

	Returns:
		A newline-separated string suitable for terminal output.
	"""

	if not isinstance(retrieval, dict):
		return str(retrieval)

	issue = retrieval.get("issue_type", "UNKNOWN")
	chunks = retrieval.get("chunks", []) or []

	lines = [f"Issue Type: {issue}", f"Chunks found: {len(chunks)}"]

	for i, c in enumerate(chunks, start=1):
		src = c.get("source_file", "<unknown>")
		cid = c.get("chunk_id", "<no-id>")
		snippet = c.get("snippet", "")
		lines.append(f"{i}. {src} ({cid}) — {snippet}")

	return "\n".join(lines)


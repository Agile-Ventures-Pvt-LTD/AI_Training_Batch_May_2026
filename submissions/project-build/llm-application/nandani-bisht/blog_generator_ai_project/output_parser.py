import json

def parse_json_response(text):
	"""Attempt to parse model output as JSON. Returns dict or raw text on failure."""
	try:
		return json.loads(text)
	except Exception:
		# fallback: try to extract first JSON object in text
		start = text.find("{")
		end = text.rfind("}")
		if start != -1 and end != -1 and end > start:
			try:
				return json.loads(text[start:end+1])
			except Exception:
				pass
	return {"raw": text}


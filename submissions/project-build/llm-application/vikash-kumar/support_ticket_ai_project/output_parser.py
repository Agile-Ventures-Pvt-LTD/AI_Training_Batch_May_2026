import json


def parse_json_response(response: str):

    try:
        return json.loads(response)

    except json.JSONDecodeError:

        start = response.find("{")
        end = response.rfind("}")

        if start != -1 and end != -1:

            possible_json = response[
                start:end + 1
            ]

            try:
                return json.loads(
                    possible_json
                )

            except Exception:
                pass

        raise ValueError(
            "Model returned invalid JSON."
        )
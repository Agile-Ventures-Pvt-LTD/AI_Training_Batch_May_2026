import json
from pathlib import Path

from groq_client import create_client
from validator import validate_env_vars, validate_blog_package, process_blog_response


OUTPUT_PATH = Path(__file__).resolve().parent / "Outputs" / "sample_blog_output.json"


def load_json_file(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Sample output file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def process_llm_response(response_text: str, output_folder: str = "Outputs") -> dict:

    return process_blog_response(response_text, output_folder)


def main() -> int:
    try:
        validate_env_vars(["GROQ_API_KEY"])
        create_client()

        print("Environment validation successful.")

        blog_package = load_json_file(OUTPUT_PATH)
        validate_blog_package(blog_package)
        print("Sample blog output validation successful.")

    except Exception as error:
        print("Error:", error)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

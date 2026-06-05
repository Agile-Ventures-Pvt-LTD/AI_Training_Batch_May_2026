import json
import os
from typing import Any
from pathlib import Path
from datetime import datetime

REQUIRED_BLOG_PACKAGE_KEYS = {
    "blog_intent_analysis": dict,
    "input_summary": dict,
    "blog_outline": dict,
    "final_blog": str,
    "seo_metadata": dict,
    "linkedin_post": dict,
    "quality_review": dict,
    "hallucination_check": dict,
    "generation_metadata": dict,
}

REQUIRED_GENERATION_METADATA_KEYS = {
    "model_used": str,
    "temperature": (float, int),
    "total_steps_completed": int,
}


def validate_env_vars(required_vars: list[str]) -> None:
    missing = [name for name in required_vars if not os.getenv(name)]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variable(s): {', '.join(missing)}. "
            "Please add them to a .env file or your environment before running the app."
        )


def validate_blog_package(data: Any) -> None:
    if not isinstance(data, dict):
        raise ValueError("Blog package must be a JSON object.")

    missing_keys = [key for key in REQUIRED_BLOG_PACKAGE_KEYS if key not in data]
    if missing_keys:
        raise ValueError(
            f"Blog package is missing required top-level key(s): {', '.join(missing_keys)}."
        )

    for key, expected_type in REQUIRED_BLOG_PACKAGE_KEYS.items():
        if not isinstance(data[key], expected_type):
            raise ValueError(
                f"Invalid type for '{key}': expected {expected_type.__name__ if isinstance(expected_type, type) else expected_type}, "
                f"but got {type(data[key]).__name__}."
            )

    if not isinstance(data["generation_metadata"], dict):
        raise ValueError("generation_metadata must be an object.")

    missing_meta = [key for key in REQUIRED_GENERATION_METADATA_KEYS if key not in data["generation_metadata"]]
    if missing_meta:
        raise ValueError(
            f"generation_metadata is missing required key(s): {', '.join(missing_meta)}."
        )

    for key, expected_type in REQUIRED_GENERATION_METADATA_KEYS.items():
        value = data["generation_metadata"][key]
        if not isinstance(value, expected_type):
            raise ValueError(
                f"Invalid type for generation_metadata['{key}']: expected {expected_type.__name__ if isinstance(expected_type, type) else expected_type}, "
                f"but got {type(value).__name__}."
            )


def parse_and_validate_json(text: str) -> dict[str, Any]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Response text is not valid JSON.") from exc

    validate_blog_package(data)
    return data


def process_blog_response(response_text: str, output_folder: str = "Outputs") -> dict[str, Any]:
    """
    Process LLM response: validate structure, parse JSON, and save to output folder.
    
    Args:
        response_text: Raw LLM response string containing JSON blog package
        output_folder: Directory to save the processed blog (default: "Outputs")
        
    Returns:
        Parsed and validated blog package dictionary
        
    Raises:
        ValueError: If JSON is invalid or structure doesn't match schema
        EnvironmentError: If output folder cannot be created
    """
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    blog_package = parse_and_validate_json(response_text)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_path / f"blog_output_{timestamp}.json"
    
    try:
        with output_file.open("w", encoding="utf-8") as file:
            json.dump(blog_package, file, indent=2, ensure_ascii=False)
    except IOError as exc:
        raise EnvironmentError(f"Failed to save blog output to {output_file}: {exc}") from exc
    
    print(f"Blog package validated and saved to: {output_file}")
    return blog_package

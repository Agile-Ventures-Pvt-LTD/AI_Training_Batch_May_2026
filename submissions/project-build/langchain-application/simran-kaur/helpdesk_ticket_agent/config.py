from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent


def _resolve_path(path_value: str) -> Path:
    path = Path(path_value).expanduser()
    if not path.is_absolute():
        path = BASE_DIR / path
    return path.resolve()


def load_config() -> dict[str, Path | str | None]:
    load_dotenv(BASE_DIR / ".env")

    db_path_value = os.getenv("DB_PATH")
    if not db_path_value:
        raise ValueError("DB_PATH is not configured.")

    db_path = _resolve_path(db_path_value)
    if not db_path.is_file():
        raise FileNotFoundError(
            f"SQLite database not found at '{db_path}'. "
            "Check DB_PATH and make sure helpdesk_agent.db is present."
        )

    return {
        "db_path": db_path,
        "groq_api_key": os.getenv("GROQ_API_KEY") or None,
        "groq_model": os.getenv("GROQ_MODEL") or None,
        # deterministic reference time used for SLA calculations (ISO format)
        "training_reference_time": os.getenv("TRAINING_REFERENCE_TIME") or "2026-06-12T09:00:00",
    }

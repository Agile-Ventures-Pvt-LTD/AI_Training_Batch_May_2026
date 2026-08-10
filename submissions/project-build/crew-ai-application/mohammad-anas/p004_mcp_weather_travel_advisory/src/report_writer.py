import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
try:
    from src.schemas import TravelReport
except ModuleNotFoundError:
    from schemas import TravelReport

load_dotenv()

logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(os.getenv("OUTPUT_PATH", "outputs"))
OUTPUT_FILE = OUTPUT_DIR / "travel_advisory_report.json"


def save_report(report: TravelReport) -> dict:
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        with OUTPUT_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                report.model_dump(mode="json"),
                file,
                indent=4,
                ensure_ascii=False,
            )

        logger.info("Travel advisory saved to %s", OUTPUT_FILE)

        return {
            "success": True,
            "saved_path": str(OUTPUT_FILE),
        }

    except Exception:
        logger.exception("Failed to save travel advisory report")

        return {
            "success": False,
            "message": "Unable to save travel advisory report.",
        }
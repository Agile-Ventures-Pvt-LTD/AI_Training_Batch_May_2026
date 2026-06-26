import pandas as pd
from crewai.tools import tool

import config


@tool("read_job_description_tool")
def read_job_description_tool() -> dict:
    """Read the job description."""

    try:
        jd_path = (
            config.DATASET_PATH
            / "job_description"
            / "jd_ai_engineer.md"
        )

        return {
            "success": True,
            "content": jd_path.read_text(encoding="utf-8"),
            "source_file": jd_path.name,
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
        }


@tool("read_resume_tool")
def read_resume_tool(
    resume_file: str,
) -> dict:
    """Read a candidate resume."""

    try:
        resume_path = (
            config.DATASET_PATH
            / "resumes"
            / resume_file
        )

        return {
            "success": True,
            "content": resume_path.read_text(encoding="utf-8"),
            "source_file": resume_path.name,
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
        }


@tool("candidate_index_lookup_tool")
def candidate_index_lookup_tool(
    candidate_id: str,
) -> dict:
    """Find a candidate in the index."""

    try:
        index_path = (
            config.DATASET_PATH
            / "metadata"
            / "candidate_index.csv"
        )

        df = pd.read_csv(index_path)

        row = df.loc[
            df["candidate_id"] == candidate_id
        ]

        if row.empty:
            return {
                "found": False,
                "message": "Candidate not found.",
            }

        row = row.iloc[0]

        return {
            "found": True,
            "candidate_id": row["candidate_id"],
            "candidate_name": row["candidate_name"],
            "resume_file": row["resume_file"],
        }

    except Exception as e:
        return {
            "found": False,
            "message": str(e),
        }


@tool("batch_candidate_loader_tool")
def batch_candidate_loader_tool() -> list[dict]:
    """Load all candidates."""

    try:
        index_path = (
            config.DATASET_PATH
            / "metadata"
            / "candidate_index.csv"
        )

        df = pd.read_csv(index_path)

        return df.to_dict("records")

    except Exception:
        return []
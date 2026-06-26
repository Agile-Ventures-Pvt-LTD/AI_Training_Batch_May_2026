import argparse

import pandas as pd

import config
from crew import resume_screening_crew


def get_resume_file(candidate_id: str) -> str:
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
        raise ValueError(
            f"{candidate_id} not found."
        )

    return row.iloc[0]["resume_file"]


def run_candidate(candidate_id: str):
    result = resume_screening_crew.kickoff(
        inputs={
            "candidate_id": candidate_id,
            "resume_file": get_resume_file(candidate_id),
            "jd_path": str(
                config.DATASET_PATH
                / "job_description"
                / "jd_ai_engineer.md"
            ),
        }
    )

    print(result)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--candidate-id",
        required=True,
    )

    args = parser.parse_args()

    run_candidate(args.candidate_id)
    run_candidate()


if __name__ == "__main__":
    main()
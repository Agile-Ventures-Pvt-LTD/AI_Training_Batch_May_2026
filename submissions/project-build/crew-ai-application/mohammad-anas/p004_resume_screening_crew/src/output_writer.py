import json

import config


def save_json(
    report: dict,
    candidate_id: str,
) -> str:
    report_dir = (
        config.OUTPUT_PATH
        / "reports"
    )

    report_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        report_dir
        / f"{candidate_id}.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            report,
            f,
            indent=2,
            ensure_ascii=False,
        )

    return str(output_file)


def save_markdown(
    report: dict,
    candidate_id: str,
) -> str:
    report_dir = (
        config.OUTPUT_PATH
        / "reports"
    )

    report_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        report_dir
        / f"{candidate_id}.md"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as f:
        f.write(f"# Candidate Screening Report\n\n")
        f.write(f"Candidate: {report['candidate_name']}\n\n")
        f.write(f"Recommendation: {report['recommendation']}\n\n")
        f.write(f"Score: {report['overall_score']}/{report['max_score']}\n")

    return str(output_file)
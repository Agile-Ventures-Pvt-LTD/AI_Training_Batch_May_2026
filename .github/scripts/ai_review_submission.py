import argparse
import os
from pathlib import Path

from groq import Groq


MAX_FILE_CHARS = 2500
MAX_TOTAL_CHARS = 9000

ALLOWED_EXTENSIONS = {
    ".py",
    ".ipynb",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
}

SKIP_DIRS = {
    ".git",
    ".github",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".ipynb_checkpoints",
}

SKIP_FILES = {
    ".env",
    "credentials.json",
    "secrets.json",
    "token.txt",
    "password.txt",
}


def read_text_file(file_path: Path) -> str:
    try:
        return file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def collect_submission_files(submission_path: Path) -> str:
    if not submission_path.exists():
        return f"Submission folder not found: {submission_path}"

    collected_content = []
    total_chars = 0

    priority_files = []
    other_files = []

    for file_path in submission_path.rglob("*"):
        if not file_path.is_file():
            continue

        if any(skip_dir in file_path.parts for skip_dir in SKIP_DIRS):
            continue

        if file_path.name in SKIP_FILES:
            continue

        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        # Give higher priority to README and source code files
        if file_path.name.lower() == "readme.md" or file_path.suffix.lower() == ".py":
            priority_files.append(file_path)
        else:
            other_files.append(file_path)

    files_to_review = priority_files + other_files

    for file_path in files_to_review:
        if total_chars >= MAX_TOTAL_CHARS:
            break

        content = read_text_file(file_path)

        if not content.strip():
            continue

        # Jupyter notebooks can be very large.
        # Keep only a limited portion for review.
        if file_path.suffix.lower() == ".ipynb":
            content = content[:1500] + "\n\n[Notebook content truncated for AI review]"

        if len(content) > MAX_FILE_CHARS:
            content = content[:MAX_FILE_CHARS] + "\n\n[File truncated for AI review]"

        remaining_chars = MAX_TOTAL_CHARS - total_chars

        if len(content) > remaining_chars:
            content = content[:remaining_chars] + "\n\n[Total review content limit reached]"
        
        collected_content.append(
            f"\n\n--- FILE: {file_path} ---\n\n{content}"
        )

        total_chars += len(content)

    if not collected_content:
        return "No readable files found for AI review."

    return "\n".join(collected_content)


def build_prompt(participant_name: str, submission_path: str, content: str) -> str:
    return f"""
You are reviewing a training participant's coding submission.

Participant name:
{participant_name}

Submission path:
{submission_path}

Your task:
Review the submission in a fair, practical, and constructive way.

Important review rules:
- Use simple and clear feedback.
- Do not be overly harsh.
- Do not assume missing requirements unless clearly visible from the submitted files.
- If something cannot be verified from the submitted files, clearly mention that.
- Do not expose or repeat any API keys, tokens, passwords, or secrets if found.
- Final marks are trainer-confirmed. You are only suggesting marks.
- Use the same marking criteria for assignments and project-build submissions.
- Give practical comments that help the participant improve.

Evaluate using this 50-mark rubric:

1. Solution - 10 marks
   Correctness, completeness, and problem-solving approach.

2. Engineering - 10 marks
   Clean, optimized, readable, modular, and maintainable code.

3. Documentation - 10 marks
   Clear README, setup instructions, explanation of approach, and usage steps.

4. Testing - 10 marks
   Test cases, validation, edge cases, and evidence that the solution was tested.

5. Professionalism - 10 marks
   Deadline discipline, ownership, clear submission structure, communication through README/PR, and following repository instructions.

Total: 50 marks.

Return the review in this exact Markdown format:

# AI Review Report

## Participant
<participant name>

## Submission Path
<submission path>

## Summary
<short summary of the submitted work>

## Scorecard

| Criteria | Marks | Comments |
|---|---:|---|
| Solution | x/10 | comment |
| Engineering | x/10 | comment |
| Documentation | x/10 | comment |
| Testing | x/10 | comment |
| Professionalism | x/10 | comment |

## Suggested Score
x/50

## Strengths
- point 1
- point 2
- point 3

## Improvements Needed
- point 1
- point 2
- point 3

## Trainer Review Notes
Mention what the trainer should manually verify before finalizing marks.

Submitted files:
{content}
"""


def run_ai_review(participant_name: str, submission_path: str, model: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "# AI Review Skipped\n\nGROQ_API_KEY is not configured in GitHub Secrets."

    client = Groq(api_key=api_key)

    submission_folder = Path(submission_path)
    content = collect_submission_files(submission_folder)
    prompt = build_prompt(participant_name, submission_path, content)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a careful code reviewer for a technical training program.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
            max_tokens=1500,
        )

        return response.choices[0].message.content

    except Exception as error:
        return f"""
# AI Review Failed

## Participant
{participant_name}

## Submission Path
{submission_path}

## Reason
The AI review could not be completed because the model/API returned an error.

## Error
{str(error)}"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--participant", required=True)
    parser.add_argument("--submission-path", required=True)
    parser.add_argument("--output", default="ai_review_report.md")
    parser.add_argument("--model", default="llama-3.3-70b-versatile")

    args = parser.parse_args()

    review = run_ai_review(
        participant_name=args.participant,
        submission_path=args.submission_path,
        model=args.model,
    )

    with open(args.output, "w", encoding="utf-8") as file:
        file.write(review)

    print(review)


if __name__ == "__main__":
    main()

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
You are an expert technical evaluator reviewing a training participant's coding submission.

Participant name:
{participant_name}

Submission path:
{submission_path}

Your role:
Act as a strict but fair reviewer. Evaluate the submission as if it is being reviewed for a professional technical training program.

The evaluation must be based only on the submitted files shown below. Do not assume missing work exists elsewhere.

Important review rules:
- Be critical, specific, and evidence-based.
- Do not give high marks for generic, incomplete, or superficial work.
- Do not reward code that only appears complete but is not explained, tested, or maintainable.
- If a file, README, code, explanation, or artifact appears AI-generated, generic, copied, or template-like, reduce marks and explain why.
- Do not claim something is AI-generated with certainty. Instead, say "appears AI-generated or generic" when there are signs.
- Signs of AI-generated or low-ownership work include:
  - Very generic README with no project-specific explanation.
  - Code that is not aligned with the assignment or project requirement.
  - Overly polished explanation but weak or incomplete implementation.
  - Placeholder text, fake screenshots, fake outputs, or unverified claims.
  - No clear understanding of why the solution was designed in a certain way.
  - Missing setup steps, missing environment details, or no execution proof.
  - Code copied from common examples without customization.
  - No tests, no validation, and no explanation of edge cases.
- Penalize missing files, poor folder structure, weak naming, unclear execution steps, and lack of evidence.
- Do not expose or repeat any API keys, tokens, passwords, or secrets if found.
- Final marks are trainer-confirmed. You are only suggesting marks.
- Use the same marking criteria for assignments and project-build submissions.
- Keep feedback professional, direct, and useful.

Evaluate using this strict 50-mark rubric:

1. Solution - 10 marks
   Evaluate correctness, completeness, requirement coverage, and problem-solving.
   Award high marks only if the solution clearly solves the stated problem and the approach is appropriate.

   Scoring guide:
   - 9-10: Complete, correct, well-aligned with the problem, handles expected scenarios.
   - 7-8: Mostly correct, minor gaps or missing edge cases.
   - 5-6: Partially correct, important gaps in logic or completeness.
   - 3-4: Weak solution, unclear logic, major missing parts.
   - 0-2: Not working, irrelevant, mostly placeholder, or cannot be evaluated.

2. Engineering - 10 marks
   Evaluate code quality, structure, readability, modularity, maintainability, and efficiency.
   Award high marks only if the code is clean, organized, and practical.

   Scoring guide:
   - 9-10: Clean, modular, readable, maintainable, good naming, low duplication.
   - 7-8: Good code with minor structure or maintainability issues.
   - 5-6: Works partially but has poor structure, repetition, or weak organization.
   - 3-4: Difficult to maintain, poorly organized, fragile, or hardcoded.
   - 0-2: Very poor code quality, mostly copied, broken, or not meaningful.

3. Documentation - 10 marks
   Evaluate README quality, setup steps, usage instructions, explanation of approach, and clarity.
   Award high marks only if another person can understand and run the submission using the documentation.

   Scoring guide:
   - 9-10: Clear README, setup, commands, assumptions, approach, and expected output.
   - 7-8: Good documentation with minor missing details.
   - 5-6: Basic documentation, but incomplete or not fully useful.
   - 3-4: Weak README, unclear steps, generic explanation.
   - 0-2: Missing README, unusable documentation, or mostly generic/AI-like text.

4. Testing - 10 marks
   Evaluate test cases, validation, edge cases, sample inputs/outputs, and proof that the solution was tested.
   Award high marks only when real validation evidence exists.

   Scoring guide:
   - 9-10: Meaningful tests, edge cases, validation steps, and clear execution evidence.
   - 7-8: Some tests or validation are present but not comprehensive.
   - 5-6: Basic manual validation only; limited test coverage.
   - 3-4: Very weak validation; claims testing but no real evidence.
   - 0-2: No tests, no validation, no sample output, or cannot verify correctness.

5. Professionalism - 10 marks
   Evaluate ownership, submission discipline, folder structure, naming, completeness, communication quality, and adherence to repository instructions.
   Award high marks only if the submission looks intentional, organized, and professionally submitted.

   Scoring guide:
   - 9-10: Clean submission, correct folder, complete artifacts, clear ownership, follows instructions.
   - 7-8: Mostly professional with minor issues.
   - 5-6: Acceptable but some missing artifacts, unclear organization, or weak ownership.
   - 3-4: Poorly organized, incomplete, careless, or hard to review.
   - 0-2: Wrong folder, missing major items, unclear ownership, or mostly placeholder work.

Additional penalty guidance:
- If code is present but README is missing or unusable, Documentation should be 0-3.
- If no tests or validation evidence is present, Testing should usually be 0-4.
- If the submission appears AI-generated or generic without participant-specific understanding, reduce relevant categories by 2-5 marks.
- If the code does not run or setup is impossible to understand, reduce Solution, Engineering, Documentation, and Testing.
- If the submission contains exposed secrets, credentials, API keys, or sensitive data, strongly penalize Professionalism and Engineering.
- If the submission has only explanation but no meaningful implementation, Solution and Engineering should be low.
- If the submission has code but no explanation of how to run it, Documentation should be low.
- If the work is incomplete but well structured, give credit only for the parts that can be verified.

Total: 50 marks.

Return the review in this exact Markdown format:

# AI Review Report

## Participant
<participant name>

## Submission Path
<submission path>

## Summary
<short summary of what was submitted and whether it appears complete>

## Scorecard

| Criteria | Marks | Comments |
|---|---:|---|
| Solution | x/10 | Specific reason for the score |
| Engineering | x/10 | Specific reason for the score |
| Documentation | x/10 | Specific reason for the score |
| Testing | x/10 | Specific reason for the score |
| Professionalism | x/10 | Specific reason for the score |

## Suggested Score
x/50

## Evidence-Based Observations
- Mention specific files, folders, or missing items that affected the score.
- Mention whether the submission appears complete or incomplete.
- Mention whether the work appears customized or generic.

## Possible AI-Generated / Generic Content Concerns
State one of the following:
- No major concern observed.
- Some content appears generic or AI-generated because <reason>.
- Strong concern: submission appears heavily AI-generated, copied, or template-like because <reason>.

Do not make absolute claims. Use evidence-based language.

## Strengths
- point 1
- point 2
- point 3

## Improvements Needed
- point 1
- point 2
- point 3

## Trainer Review Notes
Mention what the trainer should manually verify before finalizing marks, especially:
- Whether the code actually runs.
- Whether the participant submitted before the deadline.
- Whether the participant demonstrated ownership during discussion or viva.
- Whether the assignment/project requirement was fully met.
- Whether any AI-generated content concern should be validated manually.

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

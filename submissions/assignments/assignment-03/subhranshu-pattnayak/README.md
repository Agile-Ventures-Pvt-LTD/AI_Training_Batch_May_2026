# Hypothetical Questions Evaluation

This project evaluates whether HyDE-style hypothetical-question retrieval improves question answering over a standard vector-search baseline for Tesla annual-report data.

The repository contains two notebook workflows:

- `hypothetical_generator.ipynb` generates hypothetical questions for each source chunk, cleans them, and stores them in a HyDE Chroma collection.
- `main.ipynb` compares baseline retrieval against HyDE retrieval on four benchmark questions and writes the evaluation outputs.

## What Has Been Done

- Built a persistent Chroma vector database at `tesla_db/`.
- Created two Chroma collections:
  - `tesla-10k-2019-to-2023` for the original Tesla 10-K chunks.
  - `tesla-10k-2019-to-2023-hyde` for generated hypothetical questions mapped back to parent chunks.
- Generated HyDE questions and saved cleaned records in `data/hyde_questions_clean.json`.
- Ran four benchmark questions, `HQ1` through `HQ4`, comparing:
  - baseline similarity retrieval from the original chunk collection.
  - HyDE retrieval through hypothetical questions.
- Saved detailed per-question outputs in `outputs/HQ1.json` through `outputs/HQ4.json`.
- Completed the overall comparison in:
  - `outputs/comparison.md`
  - `outputs/comparison.json`

Overall result: HyDE is the stronger default retrieval path for this benchmark, winning 3 of 4 questions. Baseline retrieval is still useful when the query already uses direct disclosure keywords, as in the cybersecurity-focused HQ4.

## Project Structure

```text
.
|-- README.md
|-- pyproject.toml
|-- uv.lock
|-- .python-version
|-- .gitignore
|-- main.py
|-- hypothetical_generator.ipynb
|-- main.ipynb
|-- data/
|   |-- hyde_questions.jsonl
|   |-- hyde_questions_clean.json
|   `-- missing_chunks.txt
|-- tesla_db/
|   |-- chroma.sqlite3
|   `-- <chroma index files>
|-- backup_db/
|   `-- tesla_db/
`-- outputs/
    |-- HQ1.json
    |-- HQ2.json
    |-- HQ3.json
    |-- HQ4.json
    |-- comparison.md
    |-- comparison.json
    `-- failures.log
```

## Important Files

`hypothetical_generator.ipynb`

Generates hypothetical questions for document chunks. It uses LLM calls, writes raw records to `data/hyde_questions.jsonl`, cleans them into `data/hyde_questions_clean.json`, and adds them to the Chroma collection `tesla-10k-2019-to-2023-hyde`.

`main.ipynb`

Runs the evaluation. It loads the original Tesla chunk collection and the HyDE collection, defines retrieval functions, generates baseline and HyDE answers, and saves JSON outputs under `outputs/`.

`data/hyde_questions.jsonl`

Raw generated hypothetical-question records. Current file has 3,747 records.

`data/hyde_questions_clean.json`

Cleaned HyDE records used for vector database insertion. Current file has 3,336 chunk records and 9,997 generated questions.

`data/missing_chunks.txt`

Tracks chunks that were missing from the generation or cleaning process. Current file lists `text_3192`.

`tesla_db/`

Persistent Chroma database and index files. The database currently contains two collections and 6,672 embeddings total.

`backup_db/`

Backup copy of the earlier Chroma database.

`outputs/HQ*.json`

Detailed result files for each benchmark question. Each file includes:

- `question_id`
- `query`
- `retrieved_hypothetical_questions`
- `baseline_answer`
- `hyde_answer`
- `baseline_chunks`
- `hyde_chunks`
- `final_answer`
- `comparison_with_baseline`

`outputs/comparison.md`

Human-readable comparison of baseline vs HyDE across all benchmark questions.

`outputs/comparison.json`

Structured comparison summary suitable for loading back into Python or a notebook.

`outputs/failures.log`

Historical log from earlier failed notebook runs. This file is ignored by `.gitignore`; the final `HQ*.json` files and comparison files are complete despite these earlier failures.

## Setup

This project uses Python 3.11 and `uv`.

1. Clone or open the repository.

2. Install dependencies:

```bash
uv sync
```

3. Create a `.env` file in the project root.

Do not commit `.env`; it contains local API keys and is ignored by `.gitignore`.

Required for `main.ipynb`:

```text
GROQ_API_KEY=your_groq_key
```

Used by `hypothetical_generator.ipynb` when generating questions:

```text
GROQ_API_KEY1=your_first_groq_key
GROQ_API_KEY2=your_second_groq_key
GROQ_API_KEY3=your_third_groq_key
GROQ_API_KEY4=your_fourth_groq_key
GROQ_API_KEY5=your_fifth_groq_key
GROQ_API_KEY6=your_sixth_groq_key
GROQ_API_KEY7=your_seventh_groq_key
NVIDIA_API_KEY=your_nvidia_key
```

The existing notebooks already have generated data and database files, so you do not need to regenerate HyDE questions unless you want to rebuild the index.

4. Open the notebooks in VS Code or Jupyter and select the `.venv` Python 3.11 kernel.

## Running the Project

### Option 1: Review Existing Results

No API calls are needed.

Open:

- `outputs/comparison.md` for the narrative comparison.
- `outputs/comparison.json` for structured results.
- `outputs/HQ1.json` through `outputs/HQ4.json` for full per-question details.

### Option 2: Re-run the Evaluation

Use `main.ipynb`.

The notebook:

1. Loads environment variables.
2. Connects to `tesla_db/`.
3. Loads the original Chroma collection.
4. Loads the HyDE Chroma collection.
5. Runs baseline retrieval and HyDE retrieval for four benchmark questions.
6. Generates answers using Groq.
7. Writes output files to `outputs/`.

The benchmark questions are:

- `HQ1`: production, delivery, and scaling risks.
- `HQ2`: product defects, warranty/service obligations, customer trust, and brand risk.
- `HQ3`: future cash flow drivers across capex, working capital, and operating income.
- `HQ4`: technology, cybersecurity, data, or AI operational-risk disclosures.

### Option 3: Rebuild HyDE Questions

Use `hypothetical_generator.ipynb`.

Run this only if you want to regenerate or modify the HyDE question collection. The notebook can make many LLM calls, so confirm your API keys and rate limits first.

The expected flow is:

1. Load the existing Tesla chunk vectorstore.
2. Generate hypothetical questions for source chunks.
3. Save raw records to `data/hyde_questions.jsonl`.
4. Clean records into `data/hyde_questions_clean.json`.
5. Insert generated questions into `tesla-10k-2019-to-2023-hyde`.
6. Test HyDE retrieval.

## Current Evaluation Summary

| Question | Winner | Reason |
|---|---|---|
| HQ1 | HyDE | Retrieved more directly relevant risk-factor passages for production ramp, supply chain, facility construction, logistics, and service capacity. |
| HQ2 | HyDE | Better covered the full chain from product defects to warranty/service costs, customer trust, liability, recalls, and brand harm. |
| HQ3 | HyDE | Used more concrete cash-flow, capex, and working-capital evidence. |
| HQ4 | Baseline | The query already matched cybersecurity disclosure language, so baseline retrieval was slightly more focused. |

## Notes and Caveats

- The notebook's `comparison_with_baseline` field says "chunks," but it records `len()` of the joined context string. Treat those numbers as character counts, not retrieved chunk counts.
- `main.py` is only a small placeholder script and is not the main workflow.
- The project currently depends on notebook execution rather than a CLI.
- The vector database files are part of the working project state. Do not delete `tesla_db/` unless you plan to rebuild the database.

## Dependencies

Dependencies are defined in `pyproject.toml` and pinned in `uv.lock`. Important packages include:

- `chromadb`
- `langchain`
- `langchain-chroma`
- `langchain-community`
- `sentence-transformers`
- `groq`
- `openai`
- `python-dotenv`
- `ipykernel`

Python version: `>=3.11`.

## Submission Checklist

Before submitting this project for evaluation, include the source notebooks, data files, Chroma database, output JSON/Markdown files, `pyproject.toml`, `uv.lock`, and this README.

Do not submit local-only files:

- `.env`
- `.venv/`
- `.ipynb_checkpoints/`
- `outputs/failures.log`
- `data/failed_batches.jsonl`

The evaluator should start with `README.md`, then inspect `main.ipynb`, `hypothetical_generator.ipynb`, `outputs/comparison.md`, and `outputs/comparison.json`.

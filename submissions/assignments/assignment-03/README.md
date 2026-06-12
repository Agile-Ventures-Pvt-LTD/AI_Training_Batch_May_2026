# Assignment 03 - Hypothetical Question 

## Participant Name

Ningthoujam Rohitkumar Singh

## Description

This assignment demonstrates the use of a Large Language Model (LLM) to generate **hypothetical questions (HQs)** from Tesla 10-K annual reports as part of a Retrieval-Augmented Generation (RAG) pipeline.

The system processes document chunks in batches and generates representative questions to improve retrieval and understanding of the data.

---

## Files Included

* main.ipynb / main.py
* requirements.txt
* README.md
* final_output.json

---

## How to Run

1. Create and activate a virtual environment.

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the required API key in a `.env` file.

4. Run the script or notebook:

or

```bash
jupyter notebook Hypothetical_questions_nvedia.ipynb
```

---

## Libraries Used

The required libraries are listed in `requirements.txt`.

---



---

## Output

The program generates a structured JSON file saved as Final_output


The output contains:

* Generated hypothetical questions
* Parent chunk metadata
* Final summarized answer

---

## Notes

* Each batch generates hypothetical questions, not individual chunks.
* Chunk IDs are mapped for structural representation.
* API keys and sensitive credentials are not included in this submission.

---



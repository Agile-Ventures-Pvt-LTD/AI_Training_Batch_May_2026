# Assignment 01

## Participant Name

Rohit Ningthoujam

## Description

This assignment demonstrates various prompt engineering techniques, including Zero-Shot Prompting, Few-Shot Prompting, Chain of Thought (CoT), Tree of Thought (ToT), ReAct, Self-Consistency, and LLM-as-a-Judge evaluation using the Groq API.

## Project Structure

* main.py
* main.ipynb
* prompts.py
* groq_client.py
* outputs/
* final_analysis.md
* requirements.txt

## How to Run

1. Create a virtual environment
2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Set the API key as an environment variable

```bash
set GROQ_API_KEY=your-api-key
```

4. Run the project

```bash
python main.ipynb
```

## Libraries Used

* Python
* Groq API
* python-dotenv
* json

## Output

The generated outputs are stored in the `outputs` folder as JSON files.

## Notes

* API keys are not included in the repository.
*  `.venv` are excluded using `.gitignore`.

# Assignment 01 - Prompt Engineering

## Participant Name
Mohammad Anas

## Description
This assignment evaluates various Prompt Engineering techniques (such as Zero-Shot, Few-Shot, and Rephrase-and-Respond) using the Groq API. The project is designed with a modular architecture, separating the API client (`groq_client.py`), prompt definitions (`prompts.py`), and execution logic (`runner.py`). It enforces structured JSON outputs and includes a detailed analysis of the results.

## How to Run

1. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

2. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up Environment Variables:**
    Create a .env file in the root directory and add your Groq API key:
    ``` bash
    GROQ_API_KEY=your_actual_api_key_here
    ```
4. **Execute the Code:**
    ``` bash
    jupyter notebook assignment_01_solution.ipynb
    ```

## Libraries / Packages Required

1. **groq (>= 1.2.0)**

2. **python-dotenv (>= 1.2.2)**

3. **jupyter (>= 1.1.1)**

## Assumptions Made
1. **It is assumed that the user has a valid Groq API key configured in a .env file.**

2. **The outputs/ directory exists (or is created by the environment) to store the generated JSON files.**

3. **The LLM model used (openai/gpt-oss-120b) is active and accessible via the Groq endpoint.**

## Files Included
1. ```assignment_01_solution.ipynb``` **: Main execution notebook.**

2. ```groq_client.py```**: API connection and LLM calling logic.**

3. ```prompts.py``` **: Repository of all the prompt templates.**

4. ```runner.py``` **: Helper functions to run prompts and save JSON outputs.**

5. ```final_analysis.md``` **: Detailed documentation and evaluation of the prompt techniques.**

6. ```requirements.txt``` **: Project dependencies.**

7. ```README.md``` **: Project documentation.**

## Output Explanation

The system generates structured JSON files for different business and technical cases (e.g., Risk Classification, Technical Requirements). A comprehensive breakdown of the strengths, failure modes, and improvement suggestions for each technique is documented in ```final_analysis.md```.
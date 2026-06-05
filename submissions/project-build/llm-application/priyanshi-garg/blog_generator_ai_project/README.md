### Blog Generator application

The application follow this pipeline:
Step 1: Accept user inputs
Step 2: Validate inputs
Step 3: Classify blog intent
Step 4: Summarize input notes
Step 5: Generate blog outline
Step 6: Generate full blog
Step 7: Generate SEO metadata
Step 8: Generate LinkedIn post
Step 9: Review blog quality
Step 10: Run hallucination checklist
Step 11: Display final blog package
Step 12: Save output to JSON or Markdown

For each step I have created the individual py files that consist of individual prompts

### How to run
Run the following command in terminal:
-python main.py

### Strategy I have applied
- For testing i have created the test.ipynb to check the every prompt is working fine and generate response.
- Then i have created the main.py which is correctly giving the response

### Prompt engineering technique used in the application
- Few shot prompting
- Role based prompting
- Zero shot prompting


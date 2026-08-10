## Case-Study 1
End-to-End Blog Generator Application

## Participant-Name
Nandani Bisht

## Description of the project

## Step 1:Collect these inputs:
Blog Topic
Target Audience
Product/Service Context
Key Points
Tone
Blog Length
SEO Keywords
Call To Action

## step 2: Install dependencies:

```bash
pip install -r requirements.txt
```

 Run the Streamlit app:

```bash
streamlit run app.py
```

## Step 3: Make Multiple Groq Calls
Your workflow should be:

User Input
    ↓
1. Intent Classification
    ↓
2. Input Summary
    ↓
3. Blog Outline
    ↓
4. Full Blog
    ↓
5. SEO Metadata
    ↓
6. LinkedIn Post
    ↓
7. Quality Review
    ↓
8. Hallucination Check
    ↓
Final Output


## Step 4: Use Different Prompting Techniques
Step	Prompting Technique
Intent Classification	Zero-shot
Input Summary	Role Prompting
Outline Generation	Few-shot
Blog Writing	Role + Chain of Thought
SEO Metadata	One-shot
LinkedIn Post	One-shot
Quality Review	Few-shot
Hallucination Check	Zero-shot

## Step 5: Show Everything in Streamlit Tabs
Tab 1 → Intent Analysis
Tab 2 → Input Summary
Tab 3 → Blog Outline
Tab 4 → Final Blog
Tab 5 → SEO Metadata
Tab 6 → LinkedIn Post
Tab 7 → Quality Review
Tab 8 → Hallucination Check

## Step 6: Save Outputs 
save outputs in the sample_blog_output.json




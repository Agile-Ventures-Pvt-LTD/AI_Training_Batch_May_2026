# AI Blog Generation Pipeline

This project is an automated content generation pipeline that uses LLMs to create structured, SEO-optimized blog content along with supporting assets such as summaries, outlines, metadata, LinkedIn posts, and quality reviews.

It is designed for SaaS marketing and content teams who want to streamline blog production using AI while maintaining control, consistency, and quality checks.

---

## What This Project Does

Given a structured input (topic, audience, tone, keywords, etc.), the pipeline:

1. Classifies the intent of the blog request  
2. Generates a structured summary of requirements  
3. Builds a detailed blog outline  
4. Writes a full-length blog (~900 words)  
5. Extracts SEO metadata  
6. Generates a LinkedIn post  
7. Performs quality review  
8. Runs hallucination and consistency checks  
9. Packages everything into a final JSON output  

---

## Key Features

- Modular LLM-based pipeline (step-by-step generation)
- Structured JSON outputs at each stage
- SEO-aware blog generation
- LinkedIn post auto-generation
- Quality and hallucination checks for reliability
- Final consolidated export (`output/final_blog.json`)
- And, Only blog can be review on (`output/blog.md`)

---

## How It Works

### 1. Input Data
You define structured input like:

- Blog topic  
- Target audience  
- Product context  
- Key points  
- Tone and SEO keywords  
- CTA and constraints  

---

### 2. Pipeline Steps

The system runs through multiple LLM stages:

- Intent Classification  
- Summarization  
- Outline Generation  
- Blog Writing  
- SEO Metadata Generation  
- LinkedIn Post Creation  
- Quality Review  
- Hallucination Check  

Each step uses a dedicated prompt module inside the `prompts.py` file.

---

### 3. Output Generation

Final outputs are stored in:

- `output/blog.md` → Human-readable blog  
- `output/final_blog.json` → Structured JSON containing all artifacts  

---

## Example Output Structure

```json
{
  "blog_intent_analysis": {},
  "input_summary": {},
  "blog_outline": {},
  "final_blog": "...",
  "seo_metadata": {},
  "linkedin_post": {},
  "quality_review": {},
  "hallucination_check": {},
  "generation_metadata": {
    "model_used": "openai/gpt-oss-120b",
    "temperature": 0.2,
    "total_steps_completed": 8
  }
}
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Pipeline

```bash
app.ipynb
```
Run all the cells

import json
import os
from datetime import datetime
from validators import validate_inputs
from groq_client import DEFAULT_TEMPERATURE, MODEL_NAME
from steps.classify_intent import classify_intent
from steps.summarize_notes import summarize_notes
from steps.generate_outline import generate_outline
from steps.generate_draft import generate_draft
from steps.seo_metadata import generate_seo_metadata
from steps.linkedin_post import generate_linkedin_post
from steps.quality_review import quality_review
from steps.hallucination_check import hallucination_check
from steps.suggest_improvements import suggest_improvements
from steps.package_outputs import package_outputs


def log_progress(message: str) -> None:
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def run_pipeline(user_inputs: dict):
    # Step 1: Validate inputs
    log_progress("Step 1/11: Validating inputs...")
    validated = validate_inputs(user_inputs)
    log_progress("Step 1/11: Inputs validated.")

    # Step 2: Intent classification
    log_progress("Step 2/11: Classifying blog intent...")
    intent = classify_intent(validated)
    log_progress("Step 2/11: Blog intent classified.")

    # Step 3: Summarization
    log_progress("Step 3/11: Summarizing product context and key points...")
    summary = summarize_notes(validated["product_or_service_context"], validated["key_points"])
    log_progress("Step 3/11: Input summary generated.")

    # Step 4: Outline generation
    log_progress("Step 4/11: Generating blog outline...")
    outline = generate_outline(summary, validated["target_audience"])
    log_progress("Step 4/11: Blog outline generated.")

    # Step 5: Draft blog
    log_progress("Step 5/11: Drafting full blog...")
    draft = generate_draft(outline, validated)
    log_progress("Step 5/11: Blog draft generated.")

    # Step 6: SEO metadata
    log_progress("Step 6/11: Generating SEO metadata...")
    seo = generate_seo_metadata(validated["seo_keywords"])
    log_progress("Step 6/11: SEO metadata generated.")

    # Step 7: LinkedIn post
    log_progress("Step 7/11: Generating LinkedIn post...")
    linkedin_post = generate_linkedin_post(validated["blog_topic"], validated["call_to_action"])
    log_progress("Step 7/11: LinkedIn post generated.")

    # Step 8: Quality review
    log_progress("Step 8/11: Reviewing blog quality...")
    review = quality_review(
        draft,
        validated["brand_guidelines"],
        validated["seo_keywords"],
        validated["call_to_action"],
    )
    log_progress("Step 8/11: Quality review completed.")

    # Step 9: Hallucination check
    log_progress("Step 9/11: Checking hallucination risks...")
    hallucination_report = hallucination_check(
        draft,
        validated["avoid_claims"],
        {
            "blog_topic": validated["blog_topic"],
            "target_audience": validated["target_audience"],
            "product_or_service_context": validated["product_or_service_context"],
            "key_points": validated["key_points"],
            "industry": validated["industry"],
        },
    )
    log_progress("Step 9/11: Hallucination check completed.")

    # Step 10: Improvement suggestions
    log_progress("Step 10/11: Generating final improvement suggestions...")
    improvements = suggest_improvements(draft)
    log_progress("Step 10/11: Improvement suggestions generated.")

    # Step 11: Package outputs
    log_progress("Step 11/11: Packaging final output...")
    output = package_outputs(
        intent, summary, outline, draft, seo,
        linkedin_post, review, hallucination_report, improvements,
        {
            "model_used": MODEL_NAME,
            "temperature": DEFAULT_TEMPERATURE,
            "total_steps_completed": 8,
        },
    )

    # Save to file
    os.makedirs("outputs", exist_ok=True)
    with open(os.path.join("outputs", "sample_blog_output.json"), "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    log_progress("Step 11/11: Output saved to outputs/sample_blog_output.json.")

    return output

if __name__ == "__main__":
    try:
        with open("prompts.json", "r", encoding="utf-8") as file:
            user_inputs = json.load(file)[0]
        result = run_pipeline(user_inputs)
        print("Pipeline completed successfully. Output saved to outputs/sample_blog_output.json")
    except FileNotFoundError:
        print("Error: prompts.json file not found.")
    except json.JSONDecodeError:
        print("Error: prompts.json is malformed.")
    except (EnvironmentError, RuntimeError, ValueError, KeyError) as exc:
        print(f"Error: {exc}")

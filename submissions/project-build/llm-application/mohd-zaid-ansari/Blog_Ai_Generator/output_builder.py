def build_final_output(
    intent,
    summary,
    outline,
    blog,
    seo,
    linkedin,
    review,
    hallucination
):

    return {

        "blog_intent_analysis": intent,

        "input_summary": summary,

        "blog_outline": outline,

        "final_blog": blog,

        "seo_metadata": seo,

        "linkedin_post": linkedin,

        "quality_review": review,

        "hallucination_check": hallucination,

        "generation_metadata": {
            "model_used":
            "llama-3.3-70b-versatile",

            "temperature": 0.3,

            "total_steps_completed": 8
        }
    }
def package_outputs(
    intent,
    summary,
    outline,
    draft,
    seo,
    linkedin_post,
    review,
    hallucination_report,
    improvements,
    generation_metadata,
):
    return {
        "blog_intent_analysis": intent,
        "input_summary": summary,
        "blog_outline": outline,
        "final_blog": draft,
        "seo_metadata": seo,
        "linkedin_post": linkedin_post,
        "quality_review": review,
        "hallucination_check": hallucination_report,
        "final_improvement_suggestions": improvements,
        "generation_metadata": generation_metadata,
    }

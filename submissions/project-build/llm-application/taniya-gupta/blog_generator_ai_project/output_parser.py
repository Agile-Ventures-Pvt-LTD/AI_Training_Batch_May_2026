import json
import re


def parse_json(text):
    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        candidate = match.group(0)
        try:
            return json.loads(candidate)
        except Exception:
            cleaned = re.sub(r",\s*([}\]])", r"\1", candidate)
            try:
                return json.loads(cleaned)
            except Exception:
                return {}

    return {}


def build_final_package(**parts):

    package = {
        "blog_intent_analysis": parts.get("blog_intent_analysis", {}),
        "input_summary": parts.get("input_summary", {}),
        "blog_outline": parts.get("blog_outline", {}),
        "final_blog": parts.get("final_blog", ""),
        "seo_metadata": parts.get("seo_metadata", {}),
        "linkedin_post": parts.get("linkedin_post", {}),
        "quality_review": parts.get("quality_review", {}),
        "hallucination_check": parts.get("hallucination_check", {}),
        "generation_metadata": parts.get("generation_metadata", {}),
    }
    return package

##for check
if __name__ == "__main__":
    sample = '{"blog_intent":"LEAD_GENERATION","reasoning_summary":"based on input"}'
    print(parse_json(sample))

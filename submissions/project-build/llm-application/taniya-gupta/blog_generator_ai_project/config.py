# Groq API Config
GROQ_API_KEY = None 
GROQ_MODEL = "llama-3.3-70b-versatile"

# Model Parameters
DEFAULT_TEMPERATURE = 0.3
DEFAULT_MAX_TOKENS = 2000
SUMMARY_MAX_TOKENS = 1500
OUTLINE_MAX_TOKENS = 1500
BLOG_MAX_TOKENS = 3000
QUALITY_REVIEW_MAX_TOKENS = 1500
SEO_LINKEDIN_MAX_TOKENS = 1500
HALLUCINATION_CHECK_MAX_TOKENS = 1500


SUPPORTED_BLOG_LENGTHS = ["short", "medium", "long"]
MIN_KEY_POINTS = 3
MIN_SEO_KEYWORDS = 2


# Quality Review
QUALITY_SCORE_MIN = 1
QUALITY_SCORE_MAX = 5
QUALITY_CRITERIA = [
    "relevance",
    "clarity",
    "structure",
    "tone_alignment",
    "seo_usage",
    "hallucination_risk",
    "cta_effectiveness"
]

OUTPUT_DIR = "outputs"
OUTPUT_FORMAT = "json"


from typing import List, Dict
from pydantic import BaseModel, field_validator, ValidationError, model_validator

class BlogRequest(BaseModel):
    blog_topic: str
    target_audience: str
    product_or_service_context: str
    key_points: List[str]
    desired_tone: str
    blog_length: str
    seo_keywords: List[str]
    call_to_action: str
    industry: str | None = None
    avoid_claims: List[str] | None = None
    brand_guidelines: str | None = None

    @field_validator("blog_topic", "target_audience", "product_or_service_context", "desired_tone", "call_to_action")
    def not_empty(cls, v, field):
        if not v or not v.strip():
            raise ValueError(f"{field.name.replace('_', ' ').title()} cannot be empty")
        return v.strip()

    @field_validator("key_points")
    def min_key_points(cls, v):
        if len([p for p in v if p.strip()]) < 3:
            raise ValueError("Provide at least 3 meaningful key points")
        return v

    @field_validator("seo_keywords")
    def min_seo(cls, v):
        if len([k for k in v if k.strip()]) < 2:
            raise ValueError("Provide at least 2 SEO keywords")
        return v

    @field_validator("blog_length")
    def allowed_lengths(cls, v):
        allowed = {"short", "medium", "long"}
        v = v.lower().replace(",", "").strip()  # normalize input
        if v.startswith("around"):
            # Check if the string starts with 'around' and contains a number
            try:
                word_count = int(v.replace("around", "").strip().replace("words", "").strip())
                if word_count > 0:
                    return v
                else:
                    raise ValueError("Blog length must be a positive word count or one of short, medium, long")
            except ValueError:
                raise ValueError("Blog length must be a positive word count or one of short, medium, long")
        elif v in allowed:
            return v
        else:
            raise ValueError("Blog length must be short, medium, long or an approximate word count")

    @model_validator(mode="after")
    def overall(cls, values):
        # any cross-field checks can go here
        return values
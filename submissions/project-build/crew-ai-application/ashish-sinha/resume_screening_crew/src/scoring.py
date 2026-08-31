from pydantic import BaseModel, Field

class CategoryScores(BaseModel):
    python_programming: int = Field(0, ge=0, le=5)
    sql_database_skills: int = Field(0, ge=0, le=5)
    api_integration: int = Field(0, ge=0, le=5)
    llm_application_development: int = Field(0, ge=0, le=5)
    agent_frameworks: int = Field(0, ge=0, le=5)
    rag_understanding: int = Field(0, ge=0, le=5)
    testing_and_quality: int = Field(0, ge=0, le=5)
    communication: int = Field(0, ge=0, le=5)

class ScoringEngine:
    Categories = list(CategoryScores.model_fields.keys())
    Max_Score = len(Categories) * 5

    @staticmethod
    def calculate_metrics(scores_dict: dict) -> dict:
        scores = CategoryScores(**scores_dict).model_dump()

        total = sum(scores.values())
        pct = round((total / ScoringEngine.Max_Score) * 100, 2)

        band = "NEEDS_MANUAL_REVIEW"
        if pct >= 80: band = "STRONG_MATCH"
        elif pct >= 60: band = "MODERATE_MATCH"
        elif pct >= 40: band = "WEAK_MATCH"

        zeros = [cat for cat, score in scores.items() if score == 0]
        has_zeros = bool(zeros)

        return {
            "category_scores": scores,
            "overall_score": total,
            "max_score": ScoringEngine.MAX_SCORE,
            "percentage": pct,
            "recommendation": band,
            "flags": {
                "has_zero_scores": has_zeros,
                "zero_score_categories": zeros,
                "manual_review_recommended": has_zeros or (band == "NEEDS_MANUAL_REVIEW")
            }
        }

    @staticmethod
    def verify_evidence_integrity(evidence_list: list, minimum_required: int = 3) -> dict:
        count = len(evidence_list)
        passed = count >= minimum_required
        msg = f"Verified {count} evidence paths." if passed else f"Warning: Only found {count}/{minimum_required} evidence items."
        
        return {"evidence_count": count, "integrity_passed": passed, "message": msg}

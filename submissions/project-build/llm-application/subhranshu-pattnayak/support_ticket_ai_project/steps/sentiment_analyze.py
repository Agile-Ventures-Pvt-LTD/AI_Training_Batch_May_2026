from prompts import sentiment_prompt
from steps.common import checked_llm_json, format_messages


SENTIMENT_KEYS = [
    "sentiment",
    "emotion_signals",
    "sentiment_reasoning_summary",
    "confidence_score",
]


def analyze_sentiment(ticket: dict) -> dict:
    return checked_llm_json(
        format_messages(sentiment_prompt, user_input=ticket),
        SENTIMENT_KEYS,
        "Sentiment analysis",
        max_tokens=1000,
    )

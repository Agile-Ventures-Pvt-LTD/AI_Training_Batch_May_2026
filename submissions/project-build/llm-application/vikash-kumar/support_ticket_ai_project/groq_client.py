from groq import Groq

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential
)

from config import (
    GROQ_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
    MAX_TOKENS
)

from prompts import (
    SUMMARY_PROMPT,
    CLASSIFICATION_PROMPT,
    SENTIMENT_PROMPT,
    PRIORITY_PROMPT,
    SENSITIVE_INFORMATION_PROMPT,
    ROUTING_PROMPT,
    RESPONSE_PROMPT,
    QUALITY_REVIEW_PROMPT
)

from output_parser import (
    parse_json_response
)

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in .env"
    )

client = Groq(
    api_key=GROQ_API_KEY
)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=1,
        min=2,
        max=10
    )
)
def call_groq_model(
    prompt: str,
    temperature: float = TEMPERATURE,
    max_tokens: int = MAX_TOKENS
):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def summarize_ticket(ticket):

    prompt = SUMMARY_PROMPT.format(
        ticket=ticket
    )

    response = call_groq_model(
        prompt
    )

    return parse_json_response(
        response
    )


def classify_ticket(ticket):

    prompt = CLASSIFICATION_PROMPT.format(
        ticket=ticket
    )

    response = call_groq_model(
        prompt
    )

    return parse_json_response(
        response
    )


def analyze_sentiment(ticket):

    prompt = SENTIMENT_PROMPT.format(
        ticket=ticket
    )

    response = call_groq_model(
        prompt
    )

    return parse_json_response(
        response
    )


def detect_priority_and_risk(
    ticket
):

    prompt = PRIORITY_PROMPT.format(
        ticket=ticket
    )

    response = call_groq_model(
        prompt
    )

    return parse_json_response(
        response
    )


def detect_sensitive_information(
    ticket
):

    prompt = SENSITIVE_INFORMATION_PROMPT.format(
        ticket=ticket
    )

    response = call_groq_model(
        prompt
    )

    return parse_json_response(
        response
    )


def recommend_routing(ticket):

    prompt = ROUTING_PROMPT.format(
        ticket=ticket
    )

    response = call_groq_model(
        prompt
    )

    return parse_json_response(
        response
    )


def generate_response(ticket):

    prompt = RESPONSE_PROMPT.format(
        ticket=ticket
    )

    response = call_groq_model(
        prompt,
        temperature=0.4
    )

    return parse_json_response(
        response
    )


def review_response(
    ticket,
    draft_response
):

    prompt = QUALITY_REVIEW_PROMPT.format(
        ticket=ticket,
        response=draft_response
    )

    response = call_groq_model(
        prompt
    )

    return parse_json_response(
        response
    )
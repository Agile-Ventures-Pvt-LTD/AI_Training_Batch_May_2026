VALID_SLA_TIERS = {"standard", "premium", "enterprise"}
VALID_CUSTOMER_TYPES = {"standard", "premium", "enterprise", "trial", "free"}


def validate_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return value.strip()


def validate_optional_text(value: str | None, field_name: str, default: str = "") -> str:
    if value is None:
        return default
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be text.")
    return value.strip()


def validate_length(value: str, field_name: str, max_len: int) -> str:
    if len(value) > max_len:
        raise ValueError(f"{field_name} exceeds {max_len} characters.")
    return value


def validate_choice(value: str, field_name: str, valid_values: set[str]) -> str:
    normalized = validate_non_empty(value, field_name)
    if normalized.lower() not in valid_values:
        allowed = ", ".join(sorted(valid_values))
        raise ValueError(f"{field_name} must be one of: {allowed}.")
    return normalized


def validate_business_rules(value: list[str] | str | None) -> list[str]:
    if value is None:
        return []

    if isinstance(value, str):
        rules = [value.strip()] if value.strip() else []
    elif isinstance(value, list):
        rules = []
        for index, item in enumerate(value, start=1):
            if not isinstance(item, str) or not item.strip():
                raise ValueError(f"Business rule #{index} must be non-empty text.")
            rules.append(item.strip())
    else:
        raise ValueError("Business rules must be a list of text rules.")

    return rules


def validate_inputs(inputs: dict) -> dict:
    if not isinstance(inputs, dict):
        raise ValueError("Inputs must be provided as a dictionary.")

    customer_name = validate_length(
        validate_non_empty(inputs.get("customer_name"), "Customer name"),
        "Customer name",
        120,
    )
    ticket_subject = validate_length(
        validate_non_empty(inputs.get("ticket_subject"), "Ticket subject"),
        "Ticket subject",
        180,
    )
    ticket_body = validate_length(
        validate_non_empty(inputs.get("ticket_body"), "Ticket body"),
        "Ticket body",
        4000,
    )

    return {
        "customer_name": customer_name,
        "customer_type": validate_choice(
            inputs.get("customer_type", "Standard"),
            "Customer type",
            VALID_CUSTOMER_TYPES,
        ),
        "ticket_subject": ticket_subject,
        "ticket_body": ticket_body,
        "product_area": validate_optional_text(inputs.get("product_area"), "Product area", "General"),
        "previous_interaction_history": validate_optional_text(
            inputs.get("previous_interaction_history"),
            "Previous interaction history",
            "No prior interaction history provided.",
        ),
        "sla_tier": validate_choice(inputs.get("sla_tier", "Standard"), "SLA tier", VALID_SLA_TIERS),
        "response_tone": validate_optional_text(
            inputs.get("response_tone"),
            "Response tone",
            "Professional and empathetic",
        ),
        "business_rules": validate_business_rules(inputs.get("business_rules")),
    }

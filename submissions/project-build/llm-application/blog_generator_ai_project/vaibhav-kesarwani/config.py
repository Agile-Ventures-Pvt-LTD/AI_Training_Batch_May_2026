def get_non_empty_string(prompt, error_message):
    """Validate required string inputs."""
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print(error_message)


def get_list_input(prompt, error_message, required=True):
    """
    Validate list inputs entered as comma-separated values.
    """
    while True:
        value = input(prompt).strip()

        if not value:
            if required:
                print(error_message)
                continue
            return []

        items = [item.strip() for item in value.split(",") if item.strip()]

        if items:
            return items

        print(error_message)


def user_input():
    blog_title = get_non_empty_string(
        "Enter the topic of the blog: ",
        "Please provide the blog title."
    )

    target_audience = get_non_empty_string(
        "Enter the target audience: ",
        "Please provide the target audience."
    )

    product_service_context = get_non_empty_string(
        "Enter the product or service context: ",
        "Please provide the product or service context."
    )

    key_points = get_list_input(
        "Enter key points (comma separated): ",
        "Please provide at least one key point."
    )

    desired_tone = get_non_empty_string(
        "Enter the desired tone of the blog: ",
        "Please provide the desired tone."
    )

    blog_length = get_non_empty_string(
        "Enter the length of the blog: ",
        "Please provide the blog length."
    )

    seo_keywords = get_list_input(
        "Enter SEO keywords (comma separated): ",
        "Please provide at least one SEO keyword."
    )

    cta = get_non_empty_string(
        "Enter the Call To Action (CTA): ",
        "Please provide the CTA."
    )

    print("\nThese are optional fields. But it helpfull to generate the blog more appropriate using these fields\n")

    industry = input("Enter the target industry: ").strip()

    avoid_claims = get_list_input(
        "Enter avoid claims (comma separated, optional): ",
        "",
        required=False
    )

    brand_guidelines = input(
        "Enter the brand guidelines: "
    ).strip()

    user_data = {
        "title": blog_title,
        "audience": target_audience,
        "product_service_context": product_service_context,
        "key_points": key_points,             
        "desired_tone": desired_tone,
        "blog_length": blog_length,
        "seo_keywords": seo_keywords,         
        "cta": cta,
        "industry": industry,
        "avoid_claims": avoid_claims,         
        "brand_guidelines": brand_guidelines
    }

    return user_data

data = user_input()
print(data)

data = {
"blog_topic": "How AI can improve customer support operations",
"target_audience": "Customer support leaders, CX heads, and operations managers",
"product_or_service_context": "An AI-powered customer support assistant that helps agents summarize tickets, draft responses, identify escalation risks, and reduce repetitive manual work.",
"key_points": ["Support teams are facing increasing ticket volumes.",
"Agents spend a lot of time reading long customer conversations.",
"AI can summarize tickets and suggest draft replies.",
"AI should assist human agents, not replace them.",
"The solution can help improve consistency and response speed.",
"Sensitive customer data must be handled carefully."
],
"desired_tone": "Professional, practical, and business-oriented",
"blog_length": "Medium, around 900 words",
"seo_keywords": [
"AI customer support",
"support automation",
"customer service AI"
],
"call_to_action": "Book a demo to explore how AI can improve your support operations.",
"industry": "SaaS",
"avoid_claims": [
"Do not claim guaranteed cost reduction.",
"Do not claim full automation of customer support.",
"Do not mention any customer case study."
],
"brand_guidelines": "Use clear business language. Avoid hype. Keep the tone trustworthy and practical."
}
system_message = """You are a helpful assistant
that helps users generate blog posts using the LLM. You will receive a topic from the user and generate a well-structured blog post on that topic. The blog post should include an introduction, main content with subheadings, and a conclusion. Make sure to provide informative and engaging content that is relevant to the given topic.

User must provide the following inputs:
1. Blog topic: The main subject or theme of the blog post.
2. Target audience: The intended readers of the blog post (e.g., researchers, data scientists, sales analysts, etc.).
3. Product/Service Context: A brief description of the product or service that the company offers, which can be used to tailor the blog content.
4. Key Points: Bullet points or rough notes that the user wants to be included in the blog post.
5. Desired Tone: The tone in which the blog should be written (e.g., professional, persuasive, educational, conversational).
6. Blog Length: The desired length of the blog post (e.g., short, medium, long, or an approximate word count).
7. SEO Keywords: A list of keywords that should be included in the blog post for search engine optimization.
8. Call to Action: What the reader should do after reading the blog post (e.g., visit a website, sign up for a newsletter, contact the company, etc.).          
Optional inputs:
1. Industry: The industry in which the company operates (e.g., SaaS, healthcare, finance, education, etc.).
2. Avoided Claims: Any specific claims or statements that the model should avoid making in the blog post.
3. Brand Guidelines: Any specific tone, style, vocabulary, or formatting guidelines that the model should follow when generating the blog post.     
"""
blog_outline_system_message = """
Generate a structured blog outline before generating the full 
blog.
The outline should include:
1. Suggested title
2. Introduction direction
3. 4 to 6 main sections
4. Key message for each section
5. Suggested conclusion
6. Call-to-action placement
Output format:
{
 "title": "",
 "outline": [
 {
 "section_heading": "",
 "section_purpose": "",
 "key_points_to_cover": []
 }
 ],
 "cta_placement": "",
 "estimated_word_count": 0}
 """

Validation_message = """Validate the user inputs based on the following criteria:
 Input Validation:
- Ensure that the blog topic is provided and is not empty.
- Validate that the target audience is provided and is not empty.
- Key points must contain at least 3 meaningful points.
- Blog length must be one of the supported values (Short, Medium, Long).
- SEO keywords must contain at least 2 keywords.
- Call to action cannot be empty.
If validation fails, the application should return a clear error message.
Example:
Please provide at least 3 key points before generating the blog.
 """

user_message_template = """{
 "blog_topic": "How AI can improve customer support operations",
 "target_audience": "Customer support leaders, CX heads, and 
operations managers",
 "product_or_service_context": "An AI-powered customer support 
assistant that helps agents summarize tickets, draft responses, 
identify escalation risks, and reduce repetitive manual work.",
 "key_points": [
 "Support teams are facing increasing ticket volumes.",
 "Agents spend a lot of time reading long customer conversations.",
 "AI can summarize tickets and suggest draft replies.",
 "AI should assist human agents, not replace them.",
 "The solution can help improve consistency and response speed.",
 "Sensitive customer data must be handled carefully."
 ],
 "desired_tone": "Professional, practical, and business-oriented",
 "blog_length": "Medium",
 "seo_keywords": [
 "AI customer support",
 "support automation",
 "customer service AI"
 ],
 "call_to_action": "Book a demo to explore how AI can improve your 
support operations.",
 "industry": "SaaS",
 "avoid_claims": [
 "Do not claim guaranteed cost reduction.",
 "Do not claim full automation of customer support.",
 "Do not mention any customer case study."
 ],
 "brand_guidelines": "Use clear business language. Avoid hype. Keep 
the tone trustworthy and practical."
}
"""

try:
    user_inputs = {user_input.split(":")[0].strip(): user_input.split(":")[1].strip() for user_input in user_message_template.split("\n") if ":" in user_input}
except Exception as e:
    print(f"Error parsing user inputs: {e}")
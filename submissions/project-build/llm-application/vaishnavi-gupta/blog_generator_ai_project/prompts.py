

ONE_SHOT_PROMPT = """
"Generate a blog which should be very clear and include clean, prestigious words for generation of content
for a LinkeIn post about any achievement or milestone, post content should not contain more than 100 words,
and language should be very proper and clear to employees, students, job seekers of any domain."

Example : 
USER_INPUT: Generate a clear and precise caption for a LinkedIn post as I am starting a job
at XYZ company as a software developer. 

OUTPUT: I am happy to share that I am starting a new position at XYZ company as a software
developer, I hope I will learn new skills and give a path to career.  A big thanks to my college faculty,
family and friends for supporting me to achieve this milestone.

Task:
Analyze the user-provided blog request and classify the blog intent.

Input:
{prompt,blog_topic, target_audience, product_or_service_context, key_points, desired_tonr,
blog_length, seo_keywords, call_to_action, industry, avoid_claims, avoid_guidelines}

Rules:
- Do not invent information.
- Base your answer only on the provided input.
- If information is missing, mention it.
- Return valid JSON only.

The outline should include:
- Suggested title
- Introduction direction
- 4 to 6 main sections
- Key message for each section

Output JSON:
{
 "blog_intent": "",
 "target_reader_maturity": "",
 "recommended_content_angle": "",
 "reasoning_summary": ""
}

Do not include any extra text.
"""



ZERO_SHOT_PROMPT = """
"How AI can improve customer support operations."

Task:
Analyze the user-provided blog request and generate a concise, meaning blog with useful and
relevant information.

Input:
{prompt,blog_topic, target_audience, product_or_service_context, key_points, desired_tonr,
blog_length, seo_keywords, call_to_action, industry, avoid_claims, avoid_guidelines}

Rules:
- Do not invent information.
- Base your answer only on the provided input.
- If information is missing, mention it.
- Return valid JSON only.

The outline should include:
- Suggested title
- Introduction direction
- 4 to 6 main sections
- Key message for each section

Output JSON:
{
 
 "clean_summary": "",
 "main_message": "",
 "important_points": [],
 "missing_information": [],
 "possible_risks": []
}

Do not include any extra text.
"""


ZERO_SHOT_PROMPT_02= """
"Generate a caption for LinkedIn post for getting an internship in ISRO, Hyederabad."

Task:
Analyze the user-provided blog request and generate a concise, meaningful blog with useful and
relevant information.

Input:
{prompt,blog_topic, target_audience, product_or_service_context, key_points, desired_tonr,
blog_length, seo_keywords, call_to_action, industry, avoid_claims, avoid_guidelines}

Rules:
- Do not invent information.
- Base your answer only on the provided input.
- If information is missing, mention it.
- Return valid JSON only.

Output JSON:
{
 "linkedin_post": "",
 "hashtags": []
}

Do not include any extra text.
"""




ROLE_SHOT_PROMPT = """
Role:
You are a B2B Content Strategist.

Task:
Acknowledge the role given and generate a blog on how to manage the huge amount of content efficiently.

Input:
{prompt,blog_topic, target_audience, product_or_service_context, key_points, desired_tonr,
blog_length, seo_keywords, call_to_action, industry, avoid_claims, avoid_guidelines}

Rules:
- Do not invent information.
- Base your answer only on the provided input.
- If information is missing, mention it.
- Return valid JSON only.

The outline should include:
- Suggested title
- Introduction direction
- 4 to 6 main sections
- Key message for each section

Output JSON:
{
 
 "clean_summary": "",
 "main_message": "",
 "important_points": [],
 "missing_information": [],
 "possible_risks": []
}

Do not include any extra text.
"""





FEW_SHOT_PROMPT = """

Example_01:
USER_INPUT: "I am happy to share that I am starting a new position at XYZ company as a software
developer, I hope I will learn new skills and give a path to career.  A big thanks to my college faculty,
family and friends for supporting me to achieve this milestone."

OUTPUT : "Moderate"

Example_02:
USER_INPUT: "I feel nice to share that I am starting a new position at XYZ company as a software
engineer, I am going to learn so much new skills and give a path to career.  A big thanks to my college faculty,
family and friends for supporting me to achieve this milestone."

OUTPUT: "Bad"

Task:
Analyze the provided examples and give review on the input given by the user.
Input:
{prompt,blog_topic, target_audience, product_or_service_context, key_points, desired_tonr,
blog_length, seo_keywords, call_to_action, industry, avoid_claims, avoid_guidelines}

Rules:
- Do not invent information.
- Base your answer only on the provided input.
- If information is missing, mention it.
- Return valid JSON only.

The outline should include:
- Suggested title
- Introduction direction
- 4 to 6 main sections
- Key message for each section

Output JSON:
{
 "blog_intent": "",
 "target_reader_maturity": "",
 "recommended_content_angle": "",
 "reasoning_summary": ""
}

Do not include any extra text.
"""



COT_PROMPT = """

Compute ROI step by step for AI recommendation system.

Input:
{prompt,blog_topic, target_audience, product_or_service_context, key_points, desired_tonr,
blog_length, seo_keywords, call_to_action, industry, avoid_claims, avoid_guidelines}

Rules:
- Do not invent information.
- Base your answer only on the provided input.
- If information is missing, mention it.
- Return valid JSON only.

The outline should include:
- Suggested title
- Introduction direction
- 4 to 6 main sections
- Key message for each section

Output JSON:
{
 
 "clean_summary": "",
 "main_message": "",
 "important_points": [],
 "missing_information": [],
 "possible_risks": []
}

Do not include any extra text.
"""



TOT_PROMPT = """

Give multiple ways to generate or design the content.

Input:
{prompt,blog_topic, target_audience, product_or_service_context, key_points, desired_tonr,
blog_length, seo_keywords, call_to_action, industry, avoid_claims, avoid_guidelines}

Rules:
- Do not invent information.
- Base your answer only on the provided input.
- If information is missing, mention it.
- Return valid JSON only.

The outline should include:
- Suggested title
- Introduction direction
- 4 to 6 main sections
- Key message for each section

Output JSON:
{
 
 "clean_summary": "",
 "main_message": "",
 "important_points": [],
 "missing_information": [],
 "possible_risks": []
}

Do not include any extra text.

"""


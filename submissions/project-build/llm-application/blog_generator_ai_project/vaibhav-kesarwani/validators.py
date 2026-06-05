from prompts import (
    system_blog_review, user_blog_review_template,
    system_hallucination_control, user_hallucination_control_template,

)
from groq_client import call_groq
import json

def validator(data, blog):
    review_prompt = [
        {"role" : "system", "content" : system_blog_review},
        {"role" : "user", "content" : user_blog_review_template.format(
            data=data,
            blog=blog
        )}
    ]

    blog_review = call_groq(prompt=review_prompt)

    print(json.loads(blog_review))

def hallucination_control(blog, data):
    hallucination_control_prompt = [
        {"role" : "system", "content" : system_hallucination_control},
        {"role" : "user", "content" : user_hallucination_control_template.format(
            blog=blog,
            data=data
        )}
    ]

    blog_hallucination_control = call_groq(prompt=hallucination_control_prompt)

    print(json.loads(blog_hallucination_control))
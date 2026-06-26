from groq import Groq
import os
from dotenv import load_dotenv
import requests
load_dotenv()


try:

    def get_groq_client(system_prompt, user_input, model, temperature):
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content

except Exception as e:
    print(f"Missing API key: {e}")


# import time
# import random

# def call_api_with_retry(get_groq_client, max_retries=5, base_delay=1, max_delay=60):
#     for attempt in range(max_retries):
#         try:
#             response = get_groq_client()
#             response.raise_for_status() # Raise an exception for bad status codes
#             return response
#         except requests.exceptions.HTTPError as e:
#             if e.response.status_code == 429:
#                 retry_after = e.response.headers.get('Retry-After')
#                 if retry_after:
#                     wait_time = int(retry_after)
#                     print(f"Rate limited. Waiting {wait_time} seconds as per Retry-After header.")
#                 else:
#                     jitter = random.uniform(0, 0.5 * base_delay * (2 ** attempt)) # Add some jitter
#                     wait_time = min(max_delay, base_delay * (2 ** attempt) + jitter)
#                     print(f"Rate limited. Waiting {wait_time:.2f} seconds (attempt {attempt+1}/{max_retries}).")

#                 time.sleep(wait_time)
#             else:
#                 raise # Re-raise other HTTP errors
#         except Exception as e:
#             print(f"An unexpected error occurred: {e}")
#             raise

#     raise Exception(f"API call failed after {max_retries} attempts due to rate limiting.")
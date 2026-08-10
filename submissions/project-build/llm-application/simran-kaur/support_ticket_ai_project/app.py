from groq_client import call_llm
import json
from prompts import validate_system_message,user_prompt,summary_system_message,classify_system_message,sentiment_system_message,priority_system_message,sensitive_info_system_message,suggest_routing_system_message,draft_customer_response_system_message,response_quality_review,Final_ticket_system_message,user_input_example1,class_assistant_output_example1,user_input_example2,class_assistant_output_example2,sentiment_assistant_output_example1,sentiment_assistant_output_example2,privacy_assistant_output_example1,privacy_assistant_output_example2



# response = call_llm(
#     system_prompt=validate_system_message,
#     user_prompt=user_prompt
# )

print("-----------------------------VALIDATE INPUT----------------------------")

validate_prompt=[
    {"role": "system", "content":validate_system_message },
    {"role": "user", "content": user_prompt}
]

validate_response= call_llm(validate_prompt)

print(validate_response)



print("-------------------------------SUMMARY---------------------------------")

summary_prompt=[
    {"role": "system", "content":summary_system_message },
    {"role": "user", "content": user_prompt}
]

summary_response= call_llm(summary_prompt)



print(summary_response)


print("-----------------------------------CLASSIFY------------------------------")




classify_prompt=[
    {"role": "system", "content":classify_system_message },
    {"role": "user", "content": user_input_example1 },
    {"role": "assistant", "content": class_assistant_output_example1},
    {"role": "user", "content":user_input_example2 },
    {"role": "assistant", "content": class_assistant_output_example2},
    {"role": "user", "content":user_prompt }
]

classify_response= call_llm(classify_prompt)


print(classify_response)


print("-----------------------------Sentiment----------------------------------")

sentiment_prompt=[
    {"role": "system", "content":classify_system_message },
    {"role": "user", "content": user_input_example1 },
    {"role": "assistant", "content": sentiment_assistant_output_example1},
    {"role": "user", "content":user_input_example2 },
    {"role": "assistant", "content": sentiment_assistant_output_example2},
    {"role": "user", "content":user_prompt }
]

sentiment_response= call_llm(sentiment_prompt)


print(sentiment_response)


print("--------------------------------PRIVACY-----------------------------------")


privacy_prompt=[
    {"role": "system", "content":classify_system_message },
    {"role": "user", "content": user_input_example1 },
    {"role": "assistant", "content": privacy_assistant_output_example1},
    {"role": "user", "content":user_input_example2 },
    {"role": "assistant", "content": privacy_assistant_output_example2},
    {"role": "user", "content":user_prompt }
]

privacy_response= call_llm(sentiment_prompt)


print(privacy_response)






print("---------------------------------SENSITIVE INFO-------------------------------")

sensitive_info_prompt=[
    {"role": "system", "content":sensitive_info_system_message },
    {"role": "user", "content": user_prompt}
]

summary_response= call_llm(sensitive_info_prompt)



print(summary_response)

print("---------------------------------INTERNAL ROUTING-------------------------------")

routing_prompt=[
    {"role": "system", "content":suggest_routing_system_message},
    {"role": "user", "content": user_prompt}
]

routing_response= call_llm(routing_prompt)



print(routing_response)


print("-------------------------------DRAFT  RESPONSE--------------------------------------")

draft_prompt=[
    {"role": "system", "content":draft_customer_response_system_message},
    {"role": "user", "content": user_prompt}
]

draft_response= call_llm(draft_prompt)



print(draft_response)

print("-------------------------------Response Quality Review------------------------------")



response_quality_prompt=[
    {"role": "system", "content":response_quality_review},
    {"role": "user", "content": user_prompt}
]

quality_response= call_llm(response_quality_prompt)



print(quality_response)


print("-------------------------------Final_response------------------------------")

final_prompt=[
    {"role": "system", "content":Final_ticket_system_message},
    {"role": "user", "content": user_prompt}
]

final_response= call_llm(final_prompt)



print(final_response)


print("------------------------------- CONVERT TO JSON-----------------------------------")

with open(
    "outputs/sample_ticket_output.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        final_response,
        f,
        indent=2,
        ensure_ascii=False
    )


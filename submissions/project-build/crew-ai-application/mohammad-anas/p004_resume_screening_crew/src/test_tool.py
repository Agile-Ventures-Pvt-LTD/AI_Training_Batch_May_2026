from agents import llm

response = llm.call(
    [
        {
            "role": "user",
            "content": "Reply only with OK",
        }
    ]
)

print(response)

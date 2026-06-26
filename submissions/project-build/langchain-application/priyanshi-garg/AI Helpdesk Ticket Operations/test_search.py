# from tools import search_tickets

# result = search_tickets.invoke(
#     {
#         "status": "Open"
#     }
# )

# print(result)


# from langchain.agents import create_agent

# print("SUCCESS")

from tools import search_tickets

result = search_tickets.invoke(
    {
        "status": "Open",
        "priority": "High"
    }
)

print(result)
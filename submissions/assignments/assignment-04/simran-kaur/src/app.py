
# #===========================For Modern Agent===========================

# from src.agents.modern_agent import run_agent

# while True:

#     query = input("\nQuestion: ")

#     if query.lower() == "exit":
#         break

#     answer = run_agent(query)

#     print("\nAnswer:")
#     print(answer)

# run ```python -m src.app``` to execute


#===========================For Legacy Agent===========================

from src.agents.legacy_agent import run_agent

while True:

    query = input("\nQuestion: ")

    if query.lower() == "exit":
        break

    answer = run_agent(query)

    print("\nAnswer:")
    print(answer)
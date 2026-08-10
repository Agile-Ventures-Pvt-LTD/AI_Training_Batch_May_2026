

from prebuilt_agent import run_agent
import pprint
import json
from output_parser import output_formatter_func

while True:
    try:
        query = input("\nQuestion: ")

        if query.lower() == "exit":
            break

        response = run_agent(query)

        print(response)

        output_formatter_func(response)

    except Exception as e:
        print("ERROR:", e)



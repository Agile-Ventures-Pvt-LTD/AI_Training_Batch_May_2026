from src.guardrails import input_guard,output_guard

def run_pipeline(query:str):
   validated_query=input_guard(query)
   validated_response=output_guard(validated_query)
   return validated_response


def main():

    input_user=input("Enter your query: ")
    output_agent=run_pipeline(input_user)
    print("output:",output_agent)


if __name__ == "__main__":
    main()

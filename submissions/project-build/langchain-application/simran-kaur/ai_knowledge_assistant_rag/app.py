from chains import get_retrieved_output,generate_output, query_classification
def main():
    """
    Runs the main interactive loop for the Q&A system.

    This function initializes the conversation history, continuously prompts
    the user for queries, processes the queries using the `respond` function,
    and displays the assistant's responses. It also maintains the
    conversation history for context.

    Args:
        None

    Returns:
        None
    """

    conversation_history = [
        {'role': 'system', 'content': 'You are a helpful assistant who answers queries on financial documents'}
    ]


    while True:
        
        user_query = input("User (type q to quit): ")

        
        if user_query == 'q':
            break


        print("=================CLASSIFY QUERY===================")

        classify_query=query_classification(user_query)
        print(classify_query)

        
        retrieved_answer = get_retrieved_output(user_query)

        print("================final output=======================")
        answer=generate_output(retrieved_answer,user_query)
        print(answer)


        
        # conversation_history.append({'role': 'user', 'content': user_query})
        # conversation_history.append({'role': 'assistant', 'content': answer})

        # # 2.5 Display the assistant's answer.
        # # Print the assistant's answer to the console.
        # print(f"Assistant: {answer}")

        # print("----- Below is the conversation history -----")
        # print(conversation_history)

if __name__ == "__main__":
    main()


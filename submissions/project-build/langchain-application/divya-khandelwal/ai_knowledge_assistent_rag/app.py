import os
import json
from dotenv import load_dotenv
from groq import Groq
from retriever import retriver
from promtps import final_system_prompt,user_template
from vector_store import create_db


def main():
    load_dotenv()

    os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
    client = Groq()

    

    retriever = retriver()

    user_query = input("Please enter your question: ")
    model_name = 'llama-3.3-70b-versatile'

    relevant_document_chunks = retriever.invoke(user_query)
    context_list = [d.page_content for d in relevant_document_chunks]
    context_for_query = "\n---\n".join(context_list)

    prompt = [
        {'role': 'system', 'content': final_system_prompt},
        {'role': 'user', 'content': user_template.format(
            context=context_for_query,
            question=user_query
            )
        }
    ]


    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=prompt,
            temperature=0
        )

        prediction = response.choices[0].message.content.strip()

    except Exception as e:
        prediction = f'Sorry, I encountered the following error: \n {e}'

    # Save response into JSON file
    output = {
        "question": user_query,
        "response": prediction
    }

    with open("outputs/ benchmark_result.json", "a", encoding="utf-8") as file:
        json.dump(
            output,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Response saved to json")


if __name__=="__main__":
    main()
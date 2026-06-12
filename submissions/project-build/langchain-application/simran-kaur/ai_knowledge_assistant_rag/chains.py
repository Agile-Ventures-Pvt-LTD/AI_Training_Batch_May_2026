from dotenv import load_dotenv
from retriever import get_retriever
from vector_store import load_vectorstore
from prompts import qna_system_message,qna_user_message_template,classification_system_prompt,citation_system_message

load_dotenv()

import os

os.environ['GROQ_API_KEY'] =os.getenv("GROQ_API_KEY")
os.environ['GROQ_MODEL'] =os.getenv('GROQ_MODEL')
os.environ['TOP_K']=os.getenv('TOP_K')


from groq import Groq

client = Groq(api_key=os.environ['GROQ_API_KEY'])


#-----------------------------classification of query---------------

def query_classification(user_query):

    prompt = [
        {'role': 'system', 'content': classification_system_prompt},
        {'role': 'user', 'content': user_query
        }
    ]
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=prompt,
            temperature=0
        )

        prediction = response.choices[0].message.content
    except Exception as e:
        prediction = f'Sorry, I encountered the following error: \n {e}'

    print(prediction)
    return prediction
    

# ------------------------RAG + LLM Final output---------------------


def get_retrieved_output(user_query):
    vectorstore=load_vectorstore()

    retriever=get_retriever(vectorstore)

    relevant_document_chunks = retriever.invoke(user_query)
    context_list = [d.page_content for d in relevant_document_chunks]
    context_for_query = "\n---\n".join(context_list)
    return context_for_query




def generate_output(context_for_query,user_query):
    prompt = [
        {'role': 'system', 'content': qna_system_message},
        {'role': 'user', 'content': qna_user_message_template.format(
            context=context_for_query,
            question=user_query
            )
        }
    ]
    try:
        response = client.chat.completions.create(
            model=os.environ['GROQ_MODEL'],
            messages=prompt,
            temperature=0
        )

        prediction = response.choices[0].message.content
    except Exception as e:
        prediction = f'Sorry, I encountered the following error: \n {e}'

    return prediction

#----------------------citations-----------------------------
# def get_citation(answer):
    
#     prompt = [
#         {'role': 'system', 'content': citation_system_message},
#         {'role': 'user', 'content': answer
#         }
#     ]
#     try:
#         response = client.chat.completions.create(
#             model=os.environ['GROQ_MODEL'],
#             messages=prompt,
#             temperature=0
#         )

#         prediction = response.choices[0].message.content
#     except Exception as e:
#         prediction = f'Sorry, I encountered the following error: \n {e}'

#     print(prediction)

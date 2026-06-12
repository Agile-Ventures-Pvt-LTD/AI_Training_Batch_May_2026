import streamlit as st

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from logger import log_query

from prompts import Grounded_Answer_Prompt

load_dotenv()



st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="^_^",
    layout="wide"
)

st.title("^_^ Enterprise Knowledge Assistant")



if "chat_history" not in st.session_state:
    st.session_state.chat_history = []



@st.cache_resource
def load_vectorstore():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory="vector_db",
        embedding_function=embeddings
    )

    return vectorstore



@st.cache_resource
def load_llm():

    return ChatGroq(
        model="llama-3.1-8b-instant"
    )


vectorstore = load_vectorstore()

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

llm = load_llm()



with st.sidebar:

    st.header("📊 System Information")

    st.success("Vector Database Loaded")

    st.write(
        f"Chunks in DB: {vectorstore._collection.count()}"
    )

    st.write("Retriever")
    st.code("Chroma")

    st.write("Embedding Model")
    st.code("all-MiniLM-L6-v2")

    st.write("LLM")
    st.code("llama-3.1-8b-instant")



for msg in st.session_state.chat_history:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])



query = st.chat_input(
    "Ask a question..."
)



if query:

    

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):
        st.markdown(query)

    

    history_text = "\n".join(
        [
            f"{msg['role']}: {msg['content']}"
            for msg in st.session_state.chat_history[-6:]
        ]
    )

    

    docs = retriever.invoke(query)

    st.write("Number of docs retrieved:", len(docs))

    

    with st.expander("🔍 Retrieved Chunks"):

        for i, doc in enumerate(docs):

            st.markdown(f"### Chunk {i+1}")

            st.write(doc.metadata)

            st.write(
                doc.page_content[:1000]
            )

            st.divider()

 

    context = "\n\n".join(
        [
            doc.page_content
            for doc in docs
        ]
    )

    st.write("Context Length:", len(context))

   

    with st.expander(
        " Context Sent To LLM"
    ):
        st.text(context[:5000])

   

    prompt = Grounded_Answer_Prompt.format(
        context=context,
        history=history_text,
        query=query
    )

   

    with st.spinner("Thinking..."):

        response = llm.invoke(prompt)

        answer = response.content

    

    with st.chat_message("assistant"):

        st.markdown(answer)

        with st.expander(
            "📚 Sources Used"
        ):

            seen = set()
            source = "Amazon-2025-Annual-Report.pdf"

            for doc in docs:

                source = doc.metadata.get(
                    "source",
                    "Unknown"
                )

                page = doc.metadata.get(
                    "page",
                    "Unknown"
                )

                key = (source, page)

                if key not in seen:

                    st.write(
                        f"📄 {source} | Page {page}"
                    )

                    seen.add(key)

    
        log_query(
            query,
            answer,
            source
        )
  

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
import streamlit as st

from src.app import ask_question


st.set_page_config(
    page_title="E-Commerce SQL Agent",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 E-Commerce SQL Agent")

st.caption(
    "Ask questions in natural language."
)

question = st.chat_input(
    "Ask a question..."
)

if question:

    with st.chat_message("user"):
        st.write(question)

    result = ask_question(question)

    with st.chat_message("assistant"):

        st.subheader("Generated SQL")

        st.code(
            result["sql_query"],
            language="sql"
        )

        st.subheader("Answer")

        st.write(
            result["answer"]
        )
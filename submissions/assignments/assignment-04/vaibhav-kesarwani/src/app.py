# For the Terminal CLI

# from src.agents.modern_agent import modern_agent 
# # from src.agents.legacy_agent import legacy_agent 

# while True: 
#     question = input("\nAsk: ") 
#     if question.lower() in ["quit", "exit", "stop"]: 
#         break 
    
#     response = modern_agent(question) 
#     print("\nAnswer:") 
#     print(response)

# For the Web App

import streamlit as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.agents.modern_agent import modern_agent

st.set_page_config(
    page_title="E-Commerce Agent",
    layout="wide"
)

st.title("E-Commerce Database Agent")
st.markdown(
    "Ask business questions about customers, products, orders, and sales."
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask your question...")

if question:
    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing database..."):
            try:
                answer = modern_agent(question)

            except Exception as e:
                answer = f"Error: {str(e)}"

            st.markdown(answer)

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
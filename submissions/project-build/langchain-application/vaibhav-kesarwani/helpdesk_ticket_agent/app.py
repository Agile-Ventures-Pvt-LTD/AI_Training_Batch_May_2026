# from agent import helpdesk_agent

# while True: 
#     question = input("\nAsk: ") 
#     if question.lower() in ["quit", "exit", "stop"]: 
#         break 
    
#     response = helpdesk_agent(question) 
#     print("\nAnswer:") 
#     print(response)

import streamlit as st
from agent import helpdesk_agent

st.set_page_config(page_title="Helpdesk Agent")

st.title("Helpdesk Agent")
st.markdown("This is an AI agent which reduce operational effort by using tools to inspect ticket data, reason over ticket priority, remember user preferences, and assist with ticket updates.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask a question..."):
    with st.chat_message("user"):
        st.write(prompt)

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    response = helpdesk_agent(prompt)

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": str(response)}
    )
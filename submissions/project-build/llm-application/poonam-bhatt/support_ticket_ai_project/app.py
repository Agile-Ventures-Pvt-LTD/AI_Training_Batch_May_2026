import streamlit as st
from groq_client import parse_json_safe
import json

from output_parser import run_pipeline

import prompts 

st.set_page_config(page_title="Support AI System", layout="wide")

st.title("AI Support Ticket Intelligence System")


subject = st.text_input("Ticket Subject")
body = st.text_area("Ticket Body")
tone = st.selectbox("Response Tone", ["professional", "empathetic", "formal", "concise"])

run_btn = st.button("Process Ticket")


if run_btn:

    ticket = {
        "subject": subject,
        "body": body,
        "response_tone": tone,
        "history": ""
    }

    if not subject or not body:
        st.error("Subject and Body are required!")
    elif len(body) < 30:
        st.error("Ticket body must be at least 30 characters!")
    else:

        with st.spinner("Analyzing ticket using Groq AI..."):

            result = run_pipeline(ticket)

          
            file_path = parse_json_safe(result)

        st.success("Ticket processed successfully!")

        st.subheader(" Final Output")
        st.json(result)

        st.download_button(
            "Download JSON",
            data=json.dumps(result, indent=4),
            file_name="ticket_result.json",
            mime="application/json"
        )
        result = run_pipeline(ticket)
        file_path = parse_json_safe(result)
        
        

        st.info(f"Saved locally at: {file_path}")

        st.success("Ticket processed successfully!")




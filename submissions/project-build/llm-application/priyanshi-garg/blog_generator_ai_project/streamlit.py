import streamlit as st

st.form(
    page_title="Blog Generation App using Lama",
    page_icon='☕',
    layout='centered',
    initial_sidebar_state='collapsed'
)

st.header("Blog Generation App ☕")

# Input fields for topic, word count, and style selection
input_text = st.text_input("Enter the blog topic")

col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('No of Words')

with col2:
    blog_style = st.selectbox(
        'Writing the blog for',
        ('Researchers', 'Data Scientist', 'Sales Analyst', 'Sales Professional', 'Data Analyst', 'Common People'),
        index=0
    )

submit = st.button("Generate")
import os
import json
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from config import GROQ_API_KEY
from groq_client import call_groq
from prompts import (
    intent_classification_prompt,
    summarization_prompt,
    outline_prompt,
    blog_prompt,
    seo_prompt,
    linkedin_prompt,
    quality_review_prompt,
    hallucination_prompt,
)
from validators import validate_inputs
from output_parser import parse_json_response


if not GROQ_API_KEY:
    st.error(
        "GROQ_API_KEY is not set."
    )
    st.stop()

st.set_page_config(page_title="AI Blog Generator", layout="wide")
st.title(" AI Blog Generator")
st.markdown("Generate professional blog posts with AI-powered content intelligence")

with st.sidebar:
    st.markdown("Pipeline Stages")
    st.markdown("""
    1. Intent Classification - Analyze blog purpose
    2. Summarization - Clarify key inputs
    3. Outline - Structure the blog
    4. Blog Writing - Generate full content
    5. SEO Optimization - Add SEO metadata
    6. Social Media - Create LinkedIn post
    7. Quality Review - Assess content quality
    8. Hallucination Check - Verify facts
    """)
    

st.markdown("Blog Details")
with st.form("blog_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        blog_topic = st.text_input("Blog Topic", placeholder="write your blog topic here")
        target_audience = st.text_input("Target Audience", placeholder="Saas marketers, IT professionals")
        tone = st.selectbox("Tone", ["Proffessional", "Practical"])
    
    with col2:
        blog_length = st.selectbox("Blog Length *", ["Short (400-600)", "Medium (800-1k)", "Long (1200+)"])
        seo_keywords_raw = st.text_input("SEO Keywords", placeholder="AI customer support,support automation")
        call_to_action = st.text_input("Call To Action ", placeholder="Book a product demo")
    
    product_context = st.text_area("Product / Service Context", placeholder="Describe your product or service")
    key_points_raw = st.text_area("Key Points (one per line)", placeholder="Point 1\nPoint 2\nPoint 3")
    
    submit = st.form_submit_button("Generate Blog", use_container_width=True)

if submit:
    key_points = [k.strip() for k in key_points_raw.splitlines() if k.strip()]
    seo_keywords = [k.strip() for k in seo_keywords_raw.split(",") if k.strip()]

    data = {
        "blog_topic": blog_topic,
        "target_audience": target_audience,
        "product_context": product_context,
        "key_points": key_points,
        "tone": tone,
        "blog_length": blog_length,
        "seo_keywords": seo_keywords,
        "call_to_action": call_to_action,
    }


    errors = validate_inputs(data)
    if errors:
        st.error(" Validation Errors:\n" + "\n".join(f"• {e}" for e in errors))
    else:
        tabs = st.tabs([
            "Intent",
            "Summary",
            "Outline",
            "Blog",
            "SEO",
            "LinkedIn",
            "Quality",
            "Fact-Check",
        ])

        all_results = {"inputs": data}

        # Stage1: Intent Classification
        with tabs[0]:
            with st.spinner("analzing intent..."):
                try:
                    intent_resp = call_groq(intent_classification_prompt(json.dumps(data)))
                    intent_parsed = parse_json_response(intent_resp)
                    all_results["intent"] = intent_parsed
                    st.json(intent_parsed)
                except Exception as e:
                    st.error(f"Error in intent classification: {e}")
                    intent_parsed = {}

        # Stage 2: Summarization
        with tabs[1]:
            with st.spinner("Summarizing inputs..."):
                try:
                    summary_resp = call_groq(summarization_prompt(json.dumps(data)))
                    summary_parsed = parse_json_response(summary_resp)
                    all_results["summary"] = summary_parsed
                    st.json(summary_parsed)
                except Exception as e:
                    st.error(f"Error in the summarization: {e}")
                    summary_parsed = {}

        # Stage 3: Outline
        with tabs[2]:
            with st.spinner("Creating blog outline..."):
                try:
                    outline_data = {**data, **intent_parsed, **summary_parsed}
                    outline_resp = call_groq(outline_prompt(json.dumps(outline_data)))
                    outline_parsed = parse_json_response(outline_resp)
                    all_results["outline"] = outline_parsed
                    st.json(outline_parsed)
                except Exception as e:
                    st.error(f"Error in outline generation: {e}")
                    outline_parsed = {}

        # Stage 4: Blog Writing
        with tabs[3]:
            with st.spinner("Writing blog content..."):
                try:
                    blog_data = {**data, **outline_parsed}
                    blog_resp = call_groq(blog_prompt(json.dumps(blog_data)), temperature=0.2)
                    blog_parsed = parse_json_response(blog_resp)
                    all_results["blog"] = blog_parsed
                    if "blog" in blog_parsed:
                        st.markdown(blog_parsed["blog"])
                    else:
                        st.json(blog_parsed)
                except Exception as e:
                    st.error(f"Error in blog writing: {e}")
                    blog_parsed = {}

        # Stage 5: SEO metadata
        with tabs[4]:
            with st.spinner("Generating SEO metadata..."):
                try:
                    seo_data = {
                        "title": outline_parsed.get("title", blog_topic),
                        "blog_excerpt": blog_parsed.get("blog", "")[:500] if "blog" in blog_parsed else "",
                        "keywords": seo_keywords,
                    }
                    seo_resp = call_groq(seo_prompt(json.dumps(seo_data)))
                    seo_parsed = parse_json_response(seo_resp)
                    all_results["seo"] = seo_parsed
                    st.json(seo_parsed)
                except Exception as e:
                    st.error(f"Error in SEO generation: {e}")
                    seo_parsed = {}

        # Stage 6: LinkedIn Post
        with tabs[5]:
            with st.spinner("Creating LinkedIn post..."):
                try:
                    linkedin_data = {
                        "title": outline_parsed.get("title", blog_topic),
                        "summary": summary_parsed.get("main_message", ""),
                        "seo_title": seo_parsed.get("seo_title", blog_topic),
                    }
                    linkedin_resp = call_groq(linkedin_prompt(json.dumps(linkedin_data)))
                    linkedin_parsed = parse_json_response(linkedin_resp)
                    all_results["linkedin"] = linkedin_parsed
                    st.json(linkedin_parsed)
                except Exception as e:
                    st.error(f"Error in LinkedIn generation: {e}")
                    linkedin_parsed = {}

        # Stage 7: Quality Review
        with tabs[6]:
            with st.spinner("Reviewing content quality..."):
                try:
                    quality_data = {
                        "title": outline_parsed.get("title", blog_topic),
                        "blog": blog_parsed.get("blog", ""),
                        "tone": tone,
                    }
                    quality_resp = call_groq(quality_review_prompt(json.dumps(quality_data)))
                    quality_parsed = parse_json_response(quality_resp)
                    all_results["quality"] = quality_parsed
                    st.json(quality_parsed)
                except Exception as e:
                    st.error(f"Error in quality review: {e}")
                    quality_parsed = {}

        # Stage 8: Hallucination Check
        with tabs[7]:
            with st.spinner("Fact-checking content..."):
                try:
                    hallucination_data = {"blog": blog_parsed.get("blog", "")}
                    hallucination_resp = call_groq(
                        hallucination_prompt(json.dumps(hallucination_data))
                    )
                    hallucination_parsed = parse_json_response(hallucination_resp)
                    all_results["hallucination_check"] = hallucination_parsed
                    st.json(hallucination_parsed)
                except Exception as e:
                    st.error(f"Error in fact-checking: {e}")
                    hallucination_parsed = {}

        # Save results
        st.markdown("Download Results")
        os.makedirs("outputs", exist_ok=True)
        out_path = os.path.join("outputs", "sample_blog_output.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)

        st.success("Blog generation complete!")
        st.info(f"Results saved to: `{out_path}`")

        # Download button
        json_str = json.dumps(all_results, ensure_ascii=False, indent=2)
        st.download_button(
            label=" Download JSON",
            data=json_str,
            file_name="blog_output.json",
            mime="application/json",
        )
        


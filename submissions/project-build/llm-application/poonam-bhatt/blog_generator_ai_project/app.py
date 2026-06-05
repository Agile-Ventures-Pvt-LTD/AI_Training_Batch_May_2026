import streamlit as st
import json

from output_parser import run_pipeline
from validators import validate_blog_input
from groq_client import parse_json_safe

st.set_page_config(
    page_title="AI Blog Generator",
    page_icon="📝",
    layout="wide"
)

st.title(" AI Blog Generator")



blog_topic = st.text_input(
    "Blog Topic *"
)

target_audience = st.text_input(
    "Target Audience *"
)

product_context = st.text_area(
    "Product / Service Context *"
)

key_points = st.text_area(
    "Key Points (one per line, minimum 3) *"
)

desired_tone = st.selectbox(
    "Desired Tone *",
    [
        "Professional",
        "Persuasive",
        "Educational",
        "Conversational"
    ]
)

blog_length = st.selectbox(
    "Blog Length *",
    [
        "short",
        "medium",
        "long"
    ]
)

seo_keywords = st.text_input(
    "SEO Keywords (comma separated) *"
)

call_to_action = st.text_input(
    "Call To Action *"
)

industry = st.text_input(
    "Industry (Optional)"
)

avoided_claims = st.text_area(
    "Avoided Claims (Optional)"
)

brand_guidelines = st.text_area(
    "Brand Guidelines (Optional)"
)

# ==========================
# Generate Button
# ==========================

if st.button(" Generate Blog Package"):

    blog_data = {
        "blog_topic": blog_topic,
        "target_audience": target_audience,
        "product_context": product_context,
        "key_points": [
            point.strip()
            for point in key_points.split("\n")
            if point.strip()
        ],
        "desired_tone": desired_tone,
        "blog_length": blog_length,
        "seo_keywords": [
            keyword.strip()
            for keyword in seo_keywords.split(",")
            if keyword.strip()
        ],
        "call_to_action": call_to_action,
        "industry": industry,
        "avoided_claims": avoided_claims,
        "brand_guidelines": brand_guidelines
    }

    # ==========================
    # FR-2 Validation
    # ==========================

    validation_errors = validate_blog_input(blog_data)

    if validation_errors:

        st.error("Validation Failed")

        for error in validation_errors:
            st.warning(error)

    else:

        with st.spinner("Generating blog package..."):

            result = run_pipeline(blog_data)

        # ==========================
        # Save JSON
        # ==========================

        file_path = save_json(result)

        st.success("Blog package generated successfully!")

        # ==========================
        # Display Results
        # ==========================

        st.subheader(" Final Output Package")

        st.json(result)

        st.subheader(" Final Blog")

        if (
            isinstance(result.get("final_blog"), dict)
            and "blog_content" in result["final_blog"]
        ):
            st.markdown(
                result["final_blog"]["blog_content"]
            )

        st.subheader(" Saved File")

        st.info(file_path)

        # Download JSON

        json_string = json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )

        st.download_button(
            label="⬇ Download JSON",
            data=json_string,
            file_name="blog_output.json",
            mime="application/json"
        )
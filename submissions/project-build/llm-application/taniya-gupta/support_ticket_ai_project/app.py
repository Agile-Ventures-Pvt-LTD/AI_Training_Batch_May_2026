import streamlit as st
import json
import os
from datetime import datetime
from groq_client import call_groq_model
from validators import validate_ticket_input
from output_parser import parse_json
from prompts import (
    ticket_summarization_prompt,
    ticket_classification_prompt,
    ticket_sentiment_prompt,
    priority_and_risk_prompt,
    sensitive_information_prompt,
    routing_recommendation_prompt,
    draft_response_prompt,
    quality_review_prompt
)
import config




st.set_page_config(page_title="Support Ticket AI Assistant", layout="wide")
st.title("AI Support Ticket Intelligence System")

if not os.path.exists(config.OUTPUT_DIR):
    os.makedirs(config.OUTPUT_DIR)

# Main input section
st.markdown("### Enter Ticket Details")

col1, col2 = st.columns(2)

with col1:
    customer_name = st.text_input("Customer Name")
    customer_type = st.selectbox("Customer Type", ["Free", "Paid", "Premium", "Enterprise", ""])
    ticket_subject = st.text_input("Ticket Subject *")

with col2:
    product_area = st.text_input("Product Area", placeholder="e.g., Billing, Login, Dashboard, API, reports, subscription")
    sla_tier = st.selectbox("SLA Tier", ["Standard", "Premium", "Enterprise", ""])
    response_tone = st.selectbox("Response Tone *", ["Professional", "empathetic", "Formal", "Concise"])

ticket_body = st.text_area(
    "Ticket Body *",
    placeholder="Paste the full customer message here...",
    height=120
)

previous_interaction_history = st.text_area(
    "Previous Interaction History (Optional)",
    placeholder="Any prior messages or context...",
    height=80
)


# Validate input
if st.button("Analyze Ticket", use_container_width=True):
    ticket_data = {
        "customer_name": customer_name,
        "customer_type": customer_type,
        "ticket_subject": ticket_subject,
        "ticket_body": ticket_body,
        "product_area": product_area,
        "previous_interaction_history": previous_interaction_history,
        "sla_tier": sla_tier,
        "response_tone": response_tone,
    }
    
    # validate
    errors = validate_ticket_input(ticket_data)
    if errors:
        st.error("Validation Errors:\n" + "\n".join([f"• {e}" for e in errors]))
    else:
        st.session_state.ticket_input = ticket_data
        
       
                # Step 1: Ticket Summarization
    summary_prompt = ticket_summarization_prompt.format(
                    ticket_subject=ticket_subject,
                    ticket_body=ticket_body,
                    previous_interaction_history=previous_interaction_history or "None",
                    customer_type=customer_type or "Not specified",
                    product_area=product_area or "Not specified",
                    sla_tier=sla_tier or "Not specified",
                    response_tone=response_tone
                )
    summary_response = call_groq_model(summary_prompt, temperature=config.SUMMARY_TEMPERATURE, max_tokens=config.SUMMARY_MAX_TOKENS)
    ticket_summary = parse_json(summary_response)
                
                # Step 2: Ticket Classification
    classification_prompt = ticket_classification_prompt.format(
                    ticket_subject=ticket_subject,
                    ticket_body=ticket_body,
                    product_area=product_area or "Not specified",
                    customer_type=customer_type or "Not specified",
                    sla_tier=sla_tier or "Not specified"
                )
    classification_response = call_groq_model(classification_prompt, temperature=config.CLASSIFICATION_TEMPERATURE, max_tokens=config.CLASSIFICATION_MAX_TOKENS)
    classification = parse_json(classification_response)
                
                # Step 3: Sentiment Analysis
    sentiment_prompt = ticket_sentiment_prompt.format(
                    ticket_subject=ticket_subject,
                    ticket_body=ticket_body,
                    previous_interaction_history=previous_interaction_history or "None"
                )
    sentiment_response = call_groq_model(sentiment_prompt, temperature=config.CLASSIFICATION_TEMPERATURE, max_tokens=config.CLASSIFICATION_MAX_TOKENS)
    sentiment_analysis = parse_json(sentiment_response)
                
                # Step 4: Priority and Risk
    risk_prompt = priority_and_risk_prompt.format(
                    ticket_subject=ticket_subject,
                    ticket_body=ticket_body,
                    customer_type=customer_type or "Not specified",
                    sla_tier=sla_tier or "Not specified",
                    previous_interaction_history=previous_interaction_history or "None"
                )
    risk_response = call_groq_model(risk_prompt, temperature=config.RISK_TEMPERATURE, max_tokens=config.RISK_MAX_TOKENS)
    priority_and_risk = parse_json(risk_response)
                
                # Step 5: Sensitive Information
    sensitive_prompt = sensitive_information_prompt.format(
                    ticket_subject=ticket_subject,
                    ticket_body=ticket_body
                )
    sensitive_response = call_groq_model(sensitive_prompt, temperature=config.CLASSIFICATION_TEMPERATURE, max_tokens=config.CLASSIFICATION_MAX_TOKENS)
    sensitive_info = parse_json(sensitive_response)
                
                # Step 6: Routing Recommendation
    routing_prompt = routing_recommendation_prompt.format(
                    ticket_subject=ticket_subject,
                    ticket_body=ticket_body,
                    primary_category=classification.get("primary_category", ""),
                    secondary_categories=", ".join(classification.get("secondary_categories", [])),
                    priority=priority_and_risk.get("priority", ""),
                    escalation_risk=priority_and_risk.get("escalation_risk", "")
                )
    routing_response = call_groq_model(routing_prompt, temperature=config.CLASSIFICATION_TEMPERATURE, max_tokens=config.CLASSIFICATION_MAX_TOKENS)
    routing = parse_json(routing_response)
                
                # Step 7: Draft Response
    response_prompt = draft_response_prompt.format(
                    customer_name=customer_name or "Customer",
                    ticket_subject=ticket_subject,
                    ticket_body=ticket_body,
                    primary_category=classification.get("primary_category", ""),
                    priority=priority_and_risk.get("priority", ""),
                    escalation_risk=priority_and_risk.get("escalation_risk", ""),
                    response_tone=response_tone
                )
    response_response = call_groq_model(response_prompt, temperature=config.RESPONSE_TEMPERATURE, max_tokens=config.RESPONSE_MAX_TOKENS)
    draft_response = parse_json(response_response)
                
                # Step 8: Quality Review
    review_prompt = quality_review_prompt.format(
                    draft_response=draft_response.get("draft_response", ""),
                    response_tone=response_tone
                )
    review_response = call_groq_model(review_prompt, temperature=config.CLASSIFICATION_TEMPERATURE, max_tokens=config.CLASSIFICATION_MAX_TOKENS)
    quality_review = parse_json(review_response)
                
                # Build final output
    final_output = {
                    "ticket_summary": ticket_summary,
                    "classification": classification,
                    "sentiment_analysis": sentiment_analysis,
                    "priority_and_risk": priority_and_risk,
                    "sensitive_information_check": sensitive_info,
                    "routing_recommendation": routing,
                    "draft_customer_response": draft_response,
                    "response_quality_review": quality_review,
                    "generation_metadata": {
                        "model_used": config.GROQ_MODEL,
                        "temperature": config.RESPONSE_TEMPERATURE,
                        "total_steps_completed": 8
                    }
                }
                
    st.session_state.analysis_result = final_output
    st.success("Analysis complete!")
                
    
# Display results
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    
    st.markdown("---")
    st.markdown("### Analysis Results")
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Full Output",
        "Summary",
        "Classification & Sentiment",
        "Priority & Risk",
        "Response",
        "Export"
    ])
    
    with tab5:
        st.markdown("#### Ticket Summary")
        summary = result.get("ticket_summary", {})
        
        st.markdown(f"**Summary:** {summary.get('short_summary', 'N/A')}")
        st.markdown(f"**Customer Problem:** {summary.get('customer_problem', 'N/A')}")
        st.markdown(f"**Business Impact:** {summary.get('business_impact', 'N/A')}")
        st.markdown(f"**Requested Action:** {summary.get('customer_requested_action', 'N/A')}")
            
        if summary.get('important_context'):
                st.markdown("**Important Context:**")
                for item in summary.get('important_context', []):
                    st.markdown(f"• {item}")
            
        if summary.get('missing_information'):
                st.markdown("**Missing Information:**")
                for item in summary.get('missing_information', []):
                    st.markdown(f"• {item}")
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Classification")
            classification = result["classification"]
            st.metric("Primary Category", classification.get('primary_category', 'N/A'))
            st.write(f"**Confidence:** {classification.get('confidence_score', 0):.2f}")
            st.write(f"**Reasoning:** {classification.get('category_reasoning_summary', 'N/A')}")
            if classification.get('secondary_categories'):
                st.write(f"**Secondary Categories:** {', '.join(classification.get('secondary_categories', []))}")
        
        with col2:
            st.markdown("#### Sentiment Analysis")
            sentiment = result["sentiment_analysis"]
            st.metric("Sentiment", sentiment.get('sentiment', 'N/A'))
            st.write(f"**Confidence:** {sentiment.get('confidence_score', 0):.2f}")
            st.write(f"**Analysis:** {sentiment.get('sentiment_reasoning_summary', 'N/A')}")
            if sentiment.get('emotion_signals'):
                st.write("**Emotion Signals:**")
                for signal in sentiment.get('emotion_signals', []):
                    st.write(f"• {signal}")
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Priority & Risk")
            risk = result["priority_and_risk"]
            st.metric("Priority", risk.get('priority', 'N/A'))
            st.metric("Escalation Risk", risk.get('escalation_risk', 'N/A'))
            st.write(f"**Recommended SLA Action:** {risk.get('recommended_sla_action', 'N/A')}")
        
        with col2:
            st.markdown("#### Sensitive Information")
            sensitive = result["sensitive_information_check"]
            detected = " Yes" if sensitive.get('sensitive_information_detected') else " No"
            st.write(f"**Detected:** {detected}")
            if sensitive.get('sensitive_categories'):
                st.write(f"**Categories:** {', '.join(sensitive.get('sensitive_categories', []))}")
            if sensitive.get('handling_recommendations'):
                st.write("**Handling Recommendations:**")
                for rec in sensitive.get('handling_recommendations', []):
                    st.write(f"• {rec}")
    
    with tab4:
        st.markdown("#### Routing Recommendation")
        routing = result["routing_recommendation"]
        st.metric("Recommended Team", routing.get('recommended_team', 'N/A'))
        st.write(f"**Reason:** {routing.get('routing_reason', 'N/A')}")
        st.write(f"**Internal Note:** {routing.get('internal_note', 'N/A')}")
        
        st.markdown("#### Draft Customer Response")
        draft = result["draft_customer_response"]
        st.text_area("Response:", value=draft.get('draft_response', ''), height=150, disabled=True)
        
        st.markdown("**Response Strategy:** " + draft.get('response_strategy', 'N/A'))
        
        if draft.get('information_needed_before_sending'):
            st.markdown("**Information Needed Before Sending:**")
            for info in draft.get('information_needed_before_sending', []):
                st.markdown(f"• {info}")
        
        st.markdown("#### Response Quality Review")
        review = result["response_quality_review"]
        import json


        scores_data = review.get('scores', {})
        if isinstance(scores_data, str):
            try:
                scores_data = json.loads(scores_data)
            except json.JSONDecodeError:
                scores_data = {}
        elif not isinstance(scores_data, dict):
            scores_data = {}

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Empathy", scores_data.get('empathy', 0), "/ 5")
            st.metric("Correctness", scores_data.get('correctness', 0), "/ 5")
        with col2:
            st.metric("Actionability", scores_data.get('actionability', 0), "/ 5")
            st.metric("Policy Safety", scores_data.get('policy_safety', 0), "/ 5")
        with col3:
            st.metric("Tone Alignment", scores_data.get('tone_alignment', 0), "/ 5")
            st.metric("Completeness", scores_data.get('completeness', 0), "/ 5")

        st.write(f"**Summary:** {review.get('final_review_summary', 'N/A')}")

    
    with tab1:
        st.json(result)
    
    with tab6:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(" Save as JSON", use_container_width=True):
                filename = f"ticket_analysis_{timestamp}.json"
                filepath = os.path.join(config.OUTPUT_DIR, filename)
                with open(filepath, 'w') as f:
                    json.dump(result, f, indent=2)
                st.success(f" Saved to {filepath}")
        
        with col2:
            json_str = json.dumps(result, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"ticket_analysis_{timestamp}.json",
                mime="application/json",
                use_container_width=True
            )
        

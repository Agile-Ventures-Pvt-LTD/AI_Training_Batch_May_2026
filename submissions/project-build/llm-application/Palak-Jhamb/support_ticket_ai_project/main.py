def main():
    print("Enter Details:-")
    Customer_Name=input("Enter your name: ")
    Customer_Type=input("Enter your type (free/paid/enterprise/premium):")  
    Ticket_Subject=input("Subject: ")
    Ticket_Body=input("Explain your problem: ")
    Product_Area=input("Enter Product Area: ")
    Previous_Interaction_History=input("Previous Interaction Details: ")
    SLA_Tier=input("Enter tier(Standard/premium/enterprise): ")
    Response_Tone=input("Enter Response Tone (Professional/empathetic/concise/formal): ")
    Business_Rules=input("Enter specific rules to be considered: ")

    import json
    from groq_client import GroqClient
    client=GroqClient()
    from pathlib import Path
    

#validation

    input_data={
        "Customer_Name":Customer_Name,
        "Customer_Type":Customer_Type,
        "Ticket_Subject":Ticket_Subject,
        "Ticket_Body":Ticket_Body,
        "Product_Area":Product_Area,
        "Previous_Interaction_History":Previous_Interaction_History,
        "SLA_Tier":SLA_Tier,
        "Response_Tone":Response_Tone,
        "Business_Rules":Business_Rules
    }


    from prompts import Validation_system, Validation_user
    raw_response = client.generate(
    system_prompt=Validation_system,
    user_prompt=Validation_user.format(input=input_data)
    )

    if raw_response == "Validated" :
        pass
    else:
        print(raw_response)
        return 
    
    

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "validation.json"

    with open(output_file, "w") as f:
        json.dump(raw_response, f, indent=4)



#summary

    from prompts import summarization_system, summarization_user 
    raw_response_summary = client.generate(
    system_prompt=summarization_system,
    user_prompt=summarization_user.format(input=input_data)
    )
    
    
    output_dir = Path("outputs")

    output_file = output_dir / "summary.json"

    with open(output_file, "w") as f:
        json.dump(raw_response_summary, f, indent=4)



#classification

    from prompts import classification_system, classification_user 
    raw_response_classification = client.generate(
    system_prompt=classification_system,
    user_prompt=classification_user.format(input=input_data)
    )
    
    
    output_dir = Path("outputs")

    output_file = output_dir / "classification.json"

    with open(output_file, "w") as f:
        json.dump(raw_response_classification, f, indent=4)



#Sentiment and Customer Emotion Detection


    from prompts import sentiment_system,sentiment_user  
    raw_response_sentiments = client.generate(
    system_prompt=sentiment_system,
    user_prompt=sentiment_user.format(input=input_data)
    )
    
    
    output_dir = Path("outputs")

    output_file = output_dir / "sentiments.json"

    with open(output_file, "w") as f:
        json.dump(raw_response_sentiments, f, indent=4)


# Priority and Escalation Risk Detection

    from prompts import risk_system, risk_user  
    raw_response_risk = client.generate(
    system_prompt=risk_system,
    user_prompt=risk_user.format(input=input_data)
    )
    
    
    output_dir = Path("outputs")

    output_file = output_dir / "risk.json"

    with open(output_file, "w") as f:
        json.dump(raw_response_risk, f, indent=4)


#Sensitive Information Detection

    from prompts import sensitive_info_detection_system, sensitive_info_detection_user  
    raw_response_sensitive_info_detection = client.generate(
    system_prompt=sensitive_info_detection_system,
    user_prompt=sensitive_info_detection_user.format(input=input_data)
    )
    
    
    output_dir = Path("outputs")

    output_file = output_dir / "sensitive_info.json"

    with open(output_file, "w") as f:
        json.dump(raw_response_sensitive_info_detection, f, indent=4)


# Suggested Internal Routing
    from prompts import Internal_Routing_system,Internal_Routing_user  
    raw_response_internal_routing = client.generate(
    system_prompt=Internal_Routing_system,
    user_prompt=Internal_Routing_user.format(input=input_data)
    )
    
    
    output_dir = Path("outputs")
    
    output_file = output_dir / "internal_routing.json"

    with open(output_file, "w") as f:
        json.dump(raw_response_internal_routing, f, indent=4)



#Draft Customer Response Generation

    from prompts import draft_customer_response_generation_user,draft_customer_response_generation_system  
    raw_response_draft = client.generate(
    system_prompt=draft_customer_response_generation_system,
    user_prompt=draft_customer_response_generation_user.format(input=input_data)
    )
    
    
    output_dir = Path("outputs")
    

    output_file = output_dir / "draft.json"

    with open(output_file, "w") as f:
        json.dump(raw_response_draft, f, indent=4)


# Response Quality Review

    from prompts import Quality_system,Quality_user  
    raw_response_quality = client.generate(
    system_prompt=Quality_system,
    user_prompt=Quality_user.format(input=raw_response_draft)
    )
    
    
    output_dir = Path("outputs")

    output_file = output_dir / "quality.json"

    with open(output_file, "w") as f:
        json.dump(raw_response_quality, f, indent=4)

    from output_parser import merge_json_files
    final_json=merge_json_files()
    print(final_json)

if __name__ == "__main__":
    main()

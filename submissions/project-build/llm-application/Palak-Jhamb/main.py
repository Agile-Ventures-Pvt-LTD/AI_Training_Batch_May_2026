def main():
    Blog_Topic=input("Enter Blog Title: ") 
    Target_Audience=input("Specify Target Audience: ")
    Product_Service_Context= input("Specify Product / Service Context: ")
    Key_Points= input("Key Ponits for Blog: ")
    Desired_Tone= input("Desired Tone: ") 
    Blog_Length= input("Blog Length: ")
    SEO_Keywords= input("SEO Keywords: ")
    Call_to_Action= input("Call to Action: ")
    Industry= input("Industry: ")
    Avoided_Claims= input("Avoided Claims: ")
    Brand_Guidelines=input("Brand Guidelines: ") 


    # from validators import Validation
    # Validation(Blog_Topic, Target_Audience, Product_Service_Context, Key_Points, Desired_Tone, Blog_Length,SEO_Keywords,Call_to_Action,Industry, Avoided_Claims,Brand_Guidelines)
#input validation
    input_data={
        "Blog_topic":Blog_Topic,
        "Target_Audience":Target_Audience,
        "Product_Service_Context":Product_Service_Context,
        "Key_Points":Key_Points,
        "Desired_Tone":Desired_Tone,
        "Blog_Length":Blog_Length,
        "SEO_Keywords":SEO_Keywords,
        "Call_to_Action":Call_to_Action,
        "Industry":Industry,
        "Avoided_Claims":Avoided_Claims,
        "Brand_Guidelines":Brand_Guidelines

    }
    import json
   
    from prompts import Blog_intent_system, Blog_intent_user,Blog_summrization_system,Blog_summrization_user
    from groq_client import GroqClient
    client=GroqClient()
    from pathlib import Path
    from prompts import Validation_system, Validation_user

#validation
    raw_response = client.generate(
    system_prompt=Validation_system,
    user_prompt=Validation_user.format(input=input_data)
    )

    if raw_response:
        pass
    else:
        print(raw_response)
        return
    
    

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "validation.json"

    with open(output_file, "w") as f:
        json.dump(raw_response, f, indent=4)


# intend
    raw_response = client.generate(
    system_prompt=Blog_intent_system,
    user_prompt=Blog_intent_user.format(Blog_Topic=Blog_Topic, Target_Audience=Target_Audience)
    )

    print("Intend of blog:",raw_response)

    
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "intend.json"

    with open(output_file, "w") as f:
        json.dump(raw_response, f, indent=4)



#summarization
    
    raw_response_summary = client.generate(
    system_prompt=Blog_summrization_system,
    user_prompt=Blog_summrization_system.format(context=input_data)
    )

    print("summary of blog:",raw_response_summary)

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "summary.json"

    with open(output_file, "w") as f:
        json.dump(raw_response_summary, f, indent=4)


# outline Generation
    from prompts import Outline_system,Outline_user
    raw_response_outline = client.generate(
    system_prompt=Outline_system,
    user_prompt=Outline_user.format(context=input_data)
    )

    print("Outline  of blog:",raw_response_outline)

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "outline.json"

    with open(output_file, "w") as f:
        json.dump(raw_response_outline, f, indent=4)



#blog generation

    from prompts import Blog_generation_system,Blog_generation_user
    raw_response_blog = client.generate(
    system_prompt=Blog_generation_system,
    user_prompt=Blog_generation_user.format(outline=raw_response_outline,summary=raw_response_summary)
    )

    print("blog:",raw_response_blog)

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "Blog.json"

    with open(output_file, "w") as f:
        json.dump(raw_response, f, indent=4)

#seo and linkedin post
    from prompts import seo_linkedin_system,seo_linkedin_user
    raw_response_seo_linkedin = client.generate(
    system_prompt=seo_linkedin_system,
    user_prompt=seo_linkedin_user.format(context=raw_response_blog)
    )

    print("blog:",raw_response_seo_linkedin)

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "SEO_Linkedin.json"

    with open(output_file, "w") as f:
        json.dump(raw_response, f, indent=4)


if __name__ == "__main__":
    main()

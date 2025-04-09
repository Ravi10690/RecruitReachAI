import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from RecruitReach_AI.prompts.prompt import base_prompt
from RecruitReach_AI.src.models.llm_manager import get_llm
from load_jd import load_jds_from_file
from resume_text import load_resume
from company_research import research_company
from Extract_details import extract_details_from_jd
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables from .env file
load_dotenv()

def generate_email(job_description, 
                   company_info, 
                   resume,
                   recruiter_email,
                   job_position,
                   job_source,
                   company_name,
                   feedback=None):
    # Initialize the LLM with the API key from the environment
    llm = get_llm()

    # Create base prompt template
    prompt_messages = [("system", base_prompt)]
    
    # Add feedback to prompt if provided
    if feedback:
        prompt_messages.append(("system", f"Please regenerate the email with the following feedback: {feedback}"))
    
    prompt_messages.append(("human", "generate the email"))
    
    chat_prompt = ChatPromptTemplate(prompt_messages)
    chain = chat_prompt | llm
    
    # Create input dictionary
    input_dict = {
        "job_description": job_description,
        "company_overview": company_info,
        "resume_details": resume,
        "recruiter_email": recruiter_email,
        "job_position": job_position,
        "job_source": job_source,
        "company_name": company_name
    }
    
    # Add feedback to input if provided
    if feedback:
        input_dict["feedback"] = feedback
    
    response = chain.invoke(input_dict)

    
    # Generate the email content using the LLM
    return response.content



if __name__ == "__main__":
    job_desc = load_jds_from_file("JD.txt")
    resume = load_resume()
    extracted_details = extract_details_from_jd(job_desc)
    company_name = extracted_details.company_name if extracted_details.company_name else input("Enter the company name: ")
    recruiter_email = extracted_details.recruiter_email if extracted_details.recruiter_email else input("Enter the recruiter's email: ")
    job_position = extracted_details.job_position if extracted_details.job_position else input("Enter the job position: ")
    job_source = input("Enter the job source: ")
    company_info = research_company(company_name)

    print(generate_email(job_desc,
                          company_info,
                          resume,
                          recruiter_email,
                          job_position,
                          job_source,
                          company_name))


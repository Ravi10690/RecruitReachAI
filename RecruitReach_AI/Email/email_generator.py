
from RecruitReach_AI.prompts.prompt import base_prompt
from RecruitReach_AI.models.llm_manager import get_llm
from RecruitReach_AI.Resume.resume_parser import load_resume
from RecruitReach_AI.Comapny_Reserch.company_research import research_company
from RecruitReach_AI.Comapny_Reserch.extractComapnyDetails import extract_details_from_jd
from RecruitReach_AI.schema.schema import GenerateEmail
from langchain_core.prompts import ChatPromptTemplate


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
    chain = chat_prompt | llm.with_structured_output(GenerateEmail)
    
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

    return {"subject": response.subject, "body": response.body}



if __name__ == "__main__":
    job_desc = """𝐇𝐢𝐫𝐢𝐧𝐠 𝐔𝐩𝐝𝐚𝐭𝐞𝐬 with PW (PhysicsWallah)

𝐏𝐨𝐬𝐢𝐭𝐢𝐨𝐧- MIS Associate 
𝐑𝐨𝐥𝐞- Individual Contributor
𝐃𝐞𝐩𝐚𝐫𝐭𝐦𝐞𝐧𝐭- MIS
𝐃𝐞𝐬𝐢𝐠𝐧𝐚𝐭𝐢𝐨𝐧- Associate
𝐉𝐨𝐢𝐧𝐢𝐧𝐠- Immediate (within 7 days)
𝐄𝐱𝐩𝐞𝐫𝐢𝐞𝐧𝐜𝐞 𝐑𝐞𝐪𝐮𝐢𝐫𝐞𝐝- Minimum of 2 years in MIS (SQL, Tableau, Microsoft office)

𝐋𝐨𝐜𝐚𝐭𝐢𝐨𝐧𝐬:
📍 Rohtak Haryana Vidyapeeth

𝐑𝐞𝐜𝐫𝐮𝐢𝐭𝐞𝐫 𝐃𝐞𝐭𝐚𝐢𝐥𝐬: Ms Samridhi Goyal (samridhi.goyal@pw.live)

Interested candidates can directly mail CV at samridhi.goyal@pw.live"""
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


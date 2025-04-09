import os
from dotenv import load_dotenv
from models.llmManager import get_llm
from models import JobDetails
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from load_jd import load_jds_from_file

# Load environment variables from .env file
load_dotenv(override=True)

def extract_details_from_jd(job_description):
    # Initialize the ChatOpenAI
    # Define a prompt for extracting details
    prompt = (
        """
        Given the following job description, please extract the company name, "
        "recruiter email, and job position. Return the results in a structured format"
        if you are not sure about any of these details then leave them blank.
        """
    )
    
    prompt_template = ChatPromptTemplate([("system" , prompt),
                                          ("human", "{job_description}")])
    

    llm = get_llm()
    # Generate the extracted details using the ChatOpenAI
    llm_structure = llm.with_structured_output(schema=JobDetails)

    chain = prompt_template | llm_structure 

    return chain.invoke({"job_description": job_description})


if __name__ == "__main__":
    # Call the function to extract details from the job description
    job_description = load_jds_from_file("JD.txt")
    extracted_details = extract_details_from_jd(job_description)
    print(f"Extracted Details: {extracted_details}")


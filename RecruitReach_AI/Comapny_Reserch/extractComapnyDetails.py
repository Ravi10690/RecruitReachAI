from RecruitReach_AI.models.llm_manager import get_llm
from RecruitReach_AI.schema.schema import JobDetails
from langchain_core.prompts import ChatPromptTemplate

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
    pass


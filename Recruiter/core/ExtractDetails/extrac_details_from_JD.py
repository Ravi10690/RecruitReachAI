
from Recruiter.services.llm.llm_service import LLMService
from Recruiter.prompts.company_research_prompts import JOB_DETAILS_EXTRACTION_PROMPT
from Recruiter.models.schemas import JobDetails
from Recruiter.utils.config.config_manager import ConfigManager

def extract_details_from_job_description(job_description: str, api_key: str) -> JobDetails:
    """
    Extract details from a job description.
    
    Args:
        job_description: Job description text.
        
    Returns:
        JobDetails object containing extracted information.
    """
    # Use the prompt for extracting details
    prompt = JOB_DETAILS_EXTRACTION_PROMPT
    llm_service = LLMService(api_key=api_key)
    
    try:
        # Generate extracted details
        result = llm_service.generate_with_template(
            template=prompt,
            input_variables={"job_description": job_description},
            output_schema=JobDetails
        )
        return result
    except Exception as e:
        print(f"Error extracting details from job description: {str(e)}")
        return JobDetails()
    

if __name__ == '__main__':
    # Example
    config_manager = ConfigManager()
    api_key = config_manager.get_value("openai", "OPENAI_API_KEY")
    job_description = "We are looking for a software engineer with experience in Python and machine learning."
    details = extract_details_from_job_description(job_description, api_key)
    print(details)


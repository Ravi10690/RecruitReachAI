"""
Company Researcher for RecruitReach.

This module provides functionality for researching companies and extracting
information from job descriptions.
"""

from typing import Optional, Dict, Any, Literal

from Recruiter.services.llm.llm_service import LLMService
from Recruiter.prompts.company_research_prompts import (
    COMPANY_RESEARCH_PROMPT,
)

from Recruiter.utils.config.config_manager import ConfigManager
from Recruiter.utils.web_search.search_utils import (
    get_company_info_bs4,
    get_company_info_agent
)


class CompanyResearcher:
    """
    Researcher for company information.
    
    This class provides methods for researching companies and extracting
    information from job descriptions.
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        search_method: Literal["llm", "bs4", "agent"] = "llm"  # Changed default to "llm"
    ):
        """
        Initialize the company researcher.
        
        Args:
            api_key: OpenAI API key. If not provided, will try to get from config.
            search_method: Method to use for company research. Options are:
                - "llm": Use LLM directly
                - "bs4": Use BeautifulSoup and googlesearch
                - "agent": Use Agent with WebSearchTool
        """
        self.llm_service = LLMService(api_key=api_key)
        self.api_key = api_key
        self.search_method = search_method
    
    def research_company(self, company_name: str) -> Dict[str, Any]:
        """
        Research a company and get information about it.
        
        Args:
            company_name: Name of the company to research.
            
        Returns:
            Dictionary containing company information.
        """
        try:
            if self.search_method == "llm":
                return self.research_company_llm(company_name)
            elif self.search_method == "bs4":
                return get_company_info_bs4(company_name)
            elif self.search_method == "agent":
                return get_company_info_agent(company_name, self.api_key)
            else:
                raise ValueError("Invalid search method specified.")
                
        except (ValueError, KeyError) as e:
            print(f"Error researching company: {str(e)}")
            return {"error": f"Unable to retrieve information about {company_name}. Please try again later."}
        except Exception as e:
            # Catch-all for unexpected errors; consider logging for debugging
            print(f"Unexpected error researching company: {str(e)}")
            return {"error": f"An unexpected error occurred while retrieving information about {company_name}."}
    
    def research_company_llm(self, company_name: str) -> str:
        """
        Research a company and get information about it.
        
        Args:
            company: Name of the company to research.
            
        Returns:
            Information about the company.
        """
        try:
            # Use LLM directly with prompt
            prompt = COMPANY_RESEARCH_PROMPT.format(company_name=company_name)
            company_info = self.llm_service.generate_text(prompt)
            return company_info
            
        except Exception as e:
            print(f"Error researching company: {str(e)}")
            return f"Unable to retrieve information about {company_name}. Please try again later."

if __name__ == "__main__":
    # Example usage
    config = ConfigManager()
    openai_api_key = config.get_value("openai", "OPENAI_API_KEY")
    researcher = CompanyResearcher(api_key=openai_api_key, search_method="agent")
    company_name = "OpenAI"
    company_info = researcher.research_company(company_name)
    print(company_info)




















    # def extract_details_from_job_description(self, job_description: str) -> JobDetails:
    #     """
    #     Extract details from a job description.
        
    #     Args:
    #         job_description: Job description text.
            
    #     Returns:
    #         JobDetails object containing extracted information.
    #     """
    #     # Use the prompt for extracting details
    #     prompt = JOB_DETAILS_EXTRACTION_PROMPT
        
    #     try:
    #         # Generate extracted details
    #         result = self.llm_service.generate_with_template(
    #             template=prompt,
    #             input_variables={"job_description": job_description},
    #             output_schema=JobDetails
    #         )
    #         return result
    #     except Exception as e:
    #         print(f"Error extracting details from job description: {str(e)}")
    #         return JobDetails()

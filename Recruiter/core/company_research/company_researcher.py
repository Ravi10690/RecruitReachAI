"""
Company Researcher for RecruitReach.

This module provides functionality for researching companies and extracting
information from job descriptions.
"""

import os
from typing import Optional, Dict, Any, Literal

from Recruiter.services.llm.llm_service import LLMService
from Recruiter.models.schemas import JobDetails
from Recruiter.prompts.company_research_prompts import (
    COMPANY_RESEARCH_PROMPT,
    JOB_DETAILS_EXTRACTION_PROMPT
)
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
        search_method: Literal["llm", "bs4", "agent"] = "agent"
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
    
    def research_company(self, company_name: str) -> str:
        """
        Research a company and get information about it.
        
        Args:
            company_name: Name of the company to research.
            
        Returns:
            Information about the company.
        """
        try:
            # Use the selected search method
            if self.search_method == "llm":
                # Use LLM directly with prompt
                prompt = COMPANY_RESEARCH_PROMPT.format(company_name=company_name)
                company_info = self.llm_service.generate_text(prompt)
            elif self.search_method == "bs4":
                # Use BeautifulSoup and googlesearch
                company_info = get_company_info_bs4(company_name)
            elif self.search_method == "agent":
                # Use Agent with WebSearchTool
                company_info = get_company_info_agent(company_name, self.api_key)
            else:
                raise ValueError(f"Invalid search method: {self.search_method}")
            
            # If web search failed, fall back to LLM
            if not company_info:
                print(f"Web search failed for {company_name}, falling back to LLM")
                prompt = COMPANY_RESEARCH_PROMPT.format(company_name=company_name)
                company_info = self.llm_service.generate_text(prompt)
                
            return company_info
        except Exception as e:
            print(f"Error researching company: {str(e)}")
            return f"Unable to retrieve information about {company_name}. Please try again later."
    
    def extract_details_from_job_description(self, job_description: str) -> JobDetails:
        """
        Extract details from a job description.
        
        Args:
            job_description: Job description text.
            
        Returns:
            JobDetails object containing extracted information.
        """
        # Use the prompt for extracting details
        prompt = JOB_DETAILS_EXTRACTION_PROMPT
        
        try:
            # Generate extracted details
            result = self.llm_service.generate_with_template(
                template=prompt,
                input_variables={"job_description": job_description},
                output_schema=JobDetails
            )
            return result
        except Exception as e:
            print(f"Error extracting details from job description: {str(e)}")
            return JobDetails()

"""
Email Generator for RecruitReach2.

This module provides functionality for generating personalized emails
for job applications.
"""

from typing import Dict, Any, Optional

from Recruiter.services.llm.llm_service import LLMService
from Recruiter.models.schemas import EmailContent
from Recruiter.prompts.email_prompts import (
    EMAIL_GENERATION_PROMPT,
    EMAIL_FEEDBACK_PROMPT
)


class EmailGenerator:
    """
    Generator for personalized emails.
    
    This class provides methods for generating personalized emails for
    job applications based on resume data, job descriptions, and company information.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the email generator.
        
        Args:
            api_key: OpenAI API key. If not provided, will try to get from config.
        """
        self.llm_service = LLMService(api_key=api_key)
    
    def generate_email(
        self,
        job_description: str,
        company_info: str,
        resume: str,
        recruiter_email: str,
        job_position: str,
        job_source: str,
        company_name: str,
        feedback: Optional[str] = None
    ) -> EmailContent:
        """
        Generate a personalized email for a job application.
        
        Args:
            job_description: Job description text.
            company_info: Information about the company.
            resume: Resume text.
            recruiter_email: Email address of the recruiter.
            job_position: Position being applied for.
            job_source: Source of the job posting.
            company_name: Name of the company.
            feedback: Optional feedback for regeneration.
            
        Returns:
            EmailContent object containing the generated email.
        """
        # Get the base prompt for email generation
        base_prompt = EMAIL_GENERATION_PROMPT
        
        # Add feedback to prompt if provided
        if feedback:
            feedback_section = EMAIL_FEEDBACK_PROMPT.format(feedback=feedback)
            base_prompt += feedback_section
        
        # Create input variables for the template
        input_variables = {
            "company_name": company_name,
            "recruiter_email": recruiter_email,
            "job_position": job_position,
            "job_source": job_source,
            "resume_details": resume,
            "job_description": job_description,
            "company_overview": company_info
        }
        
        try:
            # Generate email content
            result = self.llm_service.generate_with_template(
                template=base_prompt,
                input_variables=input_variables,
                output_schema=EmailContent
            )
            return result
        except Exception as e:
            print(f"Error generating email: {str(e)}")
            raise

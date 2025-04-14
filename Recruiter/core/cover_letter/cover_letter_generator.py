"""
Cover Letter Generator for RecruitReach2.

This module provides functionality for generating personalized cover letters
for job applications.
"""

from typing import Dict, Any, Optional

from Recruiter.services.llm.llm_service import LLMService
from Recruiter.models.schemas import CoverLetterContent
from Recruiter.prompts.cover_letter_prompts import (
    COVER_LETTER_GENERATION_PROMPT,
    COVER_LETTER_FEEDBACK_PROMPT
)


class CoverLetterGenerator:
    """
    Generator for personalized cover letters.
    
    This class provides methods for generating personalized cover letters for
    job applications based on resume data, job descriptions, and company information.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the cover letter generator.
        
        Args:
            api_key: OpenAI API key. If not provided, will try to get from config.
        """
        self.llm_service = LLMService(api_key=api_key)
    
    def generate_cover_letter(
        self,
        job_description: str,
        company_info: str,
        resume: str,
        job_position: str,
        company_name: str,
        feedback: Optional[str] = None
    ) -> CoverLetterContent:
        """
        Generate a personalized cover letter for a job application.
        
        Args:
            job_description: Job description text.
            company_info: Information about the company.
            resume: Resume text.
            job_position: Position being applied for.
            company_name: Name of the company.
            feedback: Optional feedback for regeneration.
            
        Returns:
            CoverLetterContent object containing the generated cover letter.
        """
        # Get the base prompt for cover letter generation
        base_prompt = COVER_LETTER_GENERATION_PROMPT
        
        # Add feedback to prompt if provided
        if feedback:
            feedback_section = COVER_LETTER_FEEDBACK_PROMPT.format(feedback=feedback)
            base_prompt += feedback_section
        
        # Create input variables for the template
        input_variables = {
            "resume_data": resume,
            "job_description": job_description,
            "company_info": company_info,
            "position": job_position,
            "company_name": company_name
        }
        
        try:
            # Generate cover letter content
            result = self.llm_service.generate_with_template(
                template=base_prompt,
                input_variables=input_variables,
                output_schema=CoverLetterContent
            )
            return result
        except Exception as e:
            print(f"Error generating cover letter: {str(e)}")
            raise

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
            # print(result)
            # return EmailContent(
            #     subject='Application for Analytics Professional Role in Payment Integrity at Optum',
            #     body_text='Dear Hiring Manager,\n\nI hope this message finds you well. My name is Ravi Ahuja, and I am reaching out to express my interest in the Analytics Professional position in the Payment Integrity - Stats and Modeling Data Analytics team at Optum, as advertised on LinkedIn.\n\nWith a strong background in data science and machine learning, currently working as an Associate Data Scientist at Cerebrumx Labs, I have developed and implemented advanced statistical models and AI-driven solutions that have significantly improved operational efficiencies and predictive accuracy. My experience with Python, statistical modeling, and large-scale data analytics aligns well with the requirements of this role, particularly in fraud detection and predictive modeling.\n\nI am particularly excited about the opportunity to contribute to Optum’s mission of improving health outcomes through innovative analytics and technology. I admire Optum’s commitment to leveraging data to drive healthcare optimization and its culture of collaboration and continuous learning.\n\nI have attached my resume for your review and would welcome the opportunity to discuss how my skills and experience can benefit your team. Please let me know a convenient time for a call or meeting.\n\nThank you for considering my application. I look forward to your response.\n\nBest regards,\n\nRavi Ahuja\nEmail: raviahuja1998@gmail.com\nPhone: +91 98829-29426\nLinkedIn: linkedin.com/RaviAhuja\nGitHub: github.com/RaviAhuja',
            #     body_html='<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8" />\n<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n<title>Application Email</title>\n</head>\n<body style="margin:0; padding:20px; background-color:#F4F6F7; font-family: Arial, Helvetica, sans-serif; color:#333333;">\n  <table role="presentation" style="max-width:600px; margin:0 auto; background:#ffffff; border-radius:8px; padding:20px;">\n    <tr>\n      <td>\n        <h2 style="color:#2E86C1; font-size:24px; font-weight:bold; margin-bottom:20px;">Dear Hiring Manager,</h2>\n        <p style="font-size:16px; line-height:1.5; margin-bottom:16px;">I hope this message finds you well. My name is <strong>Ravi Ahuja</strong>, and I am reaching out to express my interest in the <strong>Analytics Professional</strong> position in the <em>Payment Integrity - Stats and Modeling Data Analytics team</em> at <strong>Optum</strong>, as advertised on LinkedIn.</p>\n        <p style="font-size:16px; line-height:1.5; margin-bottom:16px;">With a strong background in data science and machine learning, currently working as an Associate Data Scientist at Cerebrumx Labs, I have developed and implemented advanced statistical models and AI-driven solutions that have significantly improved operational efficiencies and predictive accuracy. My experience with Python, statistical modeling, and large-scale data analytics aligns well with the requirements of this role, particularly in fraud detection and predictive modeling.</p>\n        <p style="font-size:16px; line-height:1.5; margin-bottom:16px;">I am particularly excited about the opportunity to contribute to Optum’s mission of improving health outcomes through innovative analytics and technology. I admire Optum’s commitment to leveraging data to drive healthcare optimization and its culture of collaboration and continuous learning.</p>\n        <p style="font-size:16px; line-height:1.5; margin-bottom:24px;">I have attached my resume for your review and would welcome the opportunity to discuss how my skills and experience can benefit your team. Please let me know a convenient time for a call or meeting.</p>\n        <a href="mailto:Extraitem123@gmail.com?subject=Scheduling%20a%20Call%20Regarding%20Analytics%20Professional%20Role" style="display:inline-block; background-color:#F39C12; color:#ffffff; text-decoration:none; padding:12px 24px; border-radius:4px; font-weight:bold; font-size:16px;">Schedule a Call</a>\n        <p style="font-size:16px; line-height:1.5; margin-top:32px;">Thank you for considering my application. I look forward to your response.</p>\n        <p style="font-size:16px; line-height:1.5; margin-top:8px;">Best regards,<br /><strong>Ravi Ahuja</strong><br />Email: <a href="mailto:raviahuja1998@gmail.com" style="color:#2E86C1; text-decoration:none;">raviahuja1998@gmail.com</a><br />Phone: +91 98829-29426<br />LinkedIn: <a href="https://linkedin.com/RaviAhuja" style="color:#2E86C1; text-decoration:none;">linkedin.com/RaviAhuja</a><br />GitHub: <a href="https://github.com/RaviAhuja" style="color:#2E86C1; text-decoration:none;">github.com/RaviAhuja</a></p>\n      </td>\n    </tr>\n  </table>\n</body>\n</html>'
            # )
        except Exception as e:
            print(f"Error generating email: {str(e)}")
            raise

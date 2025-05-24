"""
Company Research Prompts for RecruitReach.

This module contains prompts used for company research and job description analysis.
"""

# Prompt for researching a company
COMPANY_RESEARCH_PROMPT = """
You are a helpful assistant that provides information about companies.
Please provide a comprehensive overview of {company_name}.
Include information such as:

1. Company background and history
2. Industry and main products/services
3. Company culture and values
4. Recent news or developments
5. Market position and competitors

Provide a well-structured and detailed response that would be useful for someone
preparing for a job application or interview.
"""

OPENAI_WEB_SERACH_PROMPT = """
You are a helpful assistant that provides information about companies.
Please provide a comprehensive overview of company.
Include information such as:

1. Company background and history
2. Industry and main products/services
3. Company culture and values
4. Recent news or developments
5. Market position and competitors

Provide a well-structured and detailed response that would be useful for someone
preparing for a job application or interview.
"""

# Prompt for extracting details from a job description
JOB_DETAILS_EXTRACTION_PROMPT = """
You are a detail-oriented assistant tasked with extracting specific information from job descriptions.
Please analyze the following job description and extract these key details:

1. Company Name: The official name of the company (if clearly stated)
2. Recruiter Email: Any email address provided for applications or contact
3. Job Position: The exact title of the position being offered

Rules:
- If any detail is not explicitly mentioned or unclear, leave it blank
- For company name, only extract if it's clearly the official company name
- For recruiter email, look for email addresses in the format user@domain.com
- For job position, extract the exact title as stated in the description

Job Description:
{job_description}

Please return the results in a structured format matching these fields:
- company_name: (string)
- recruiter_email: (string)
- job_position: (string)
"""

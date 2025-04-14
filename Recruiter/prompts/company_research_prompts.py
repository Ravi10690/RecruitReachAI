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
Please provide a comprehensive overview of cpmpany.
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
Given the following job description, please extract the company name,
recruiter email, and job position. Return the results in a structured format.
double check the details of comapny name does not look like the company name leave it blank
If you are not sure about any of these details, leave them blank.
{job_description}
"""

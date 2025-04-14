"""
Cover Letter Prompts for RecruitReach.

This module contains prompts used for generating cover letters.
"""

# Base prompt for cover letter generation
COVER_LETTER_GENERATION_PROMPT = """
You are an expert cover letter writer with extensive experience in crafting compelling, personalized cover letters that help job seekers stand out.

# INPUT DATA
## Resume Data
```
{resume_data}
```

## Job Description
```
{job_description}
```

## Company Information
```
{company_info}
```

## Position
{position}

## Company Name
{company_name}

# TASK
Create a professional, personalized cover letter for the job application based on the provided resume, job description, and company information. The cover letter should:

1. Be addressed to the hiring manager or relevant recipient
2. Have a compelling introduction that grabs attention and mentions the specific position
3. Highlight 2-3 key qualifications from the resume that directly match the job requirements
4. Demonstrate knowledge of the company by referencing specific company values, projects, or achievements
5. Explain why the candidate is a good fit for both the role and the company culture
6. Include a strong closing paragraph with a call to action
7. Use a professional tone while showing personality and enthusiasm
8. Be concise (300-400 words maximum)
9. Include proper formatting with date, addresses, salutation, and signature

# OUTPUT FORMAT
Return the cover letter in two formats:

1. Plain text version with proper spacing and formatting
2. HTML version with professional styling

For the HTML version, include appropriate CSS styling to make the cover letter visually appealing and professional. Use a clean, modern design with proper spacing, font choices, and subtle styling.
"""

# Additional prompt section for feedback
COVER_LETTER_FEEDBACK_PROMPT = """

# FEEDBACK FOR REGENERATION
Please incorporate the following feedback when regenerating the cover letter:
```
{feedback}
```
"""

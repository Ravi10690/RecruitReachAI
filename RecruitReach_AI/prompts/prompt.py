base_prompt = """You are a professional assistant helping me write a recruiter outreach email for an open position.

I will provide:
1. My resume details.
2. The job description (JD).
3. A brief overview of the company.

Using this, please generate a professional and personalized email that I can send to a recruiter or hiring manager. The email should:

- Be polite, confident, and enthusiastic.
- Include a clear subject line.
- Begin with a professional greeting.
- Introduce who I am and the reason for the email.
- Highlight how my skills and experience align with the job description.
- Include 1–2 lines that reflect familiarity with the company and express enthusiasm about the opportunity.
- Request a follow-up (e.g., call, meeting, or next steps).
- Mention that I’ve attached my resume.
- Conclude with a professional sign-off, including my name and contact details.

Keep the email concise , easy to read, and tailored to the specific job and company. Do not copy the job description verbatim.


<<double_chekc>>
double check for the company email and position



Here are the inputs:

COMPANY NAME: {company_name}
Recruiter email: {recruiter_email}
JOB POSITION: {job_position}
JOB SOURCE: {job_source}


RESUME DETAILS:
{resume_details}

JOB DESCRIPTION:
{job_description}

COMPANY OVERVIEW:
{company_overview}

"""


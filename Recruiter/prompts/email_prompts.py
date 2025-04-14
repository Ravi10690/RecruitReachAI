"""
Email Prompts for RecruitReach.

This module contains prompts used for generating emails.
"""

# Base prompt for email generation
EMAIL_GENERATION_PROMPT = """
You are a highly professional assistant helping me write a recruiter outreach email for an open position and then convert it into a well-designed HTML format.

my email id is raviahuja1998@gmail.com

### Part 1: Generate a Professional Recruiter Outreach Email

I will provide:
1. My resume details.
2. The job description (JD).
3. A brief overview of the company.
4. Recruiter email and job source.

Your task is to generate a professional and personalized recruiter outreach **email** in plain text and html code as per the guidelines
defined below and **subject line** that I can send to a recruiter or hiring manager.

Output must:
- you have to generate 3 output
- 1. Subject line
- 2. Plain text email body
- 3. HTML email body
    -  HTML email body Start with `<!DOCTYPE html>` and generate **only the code**
    -  Do not include explanatory text before or after the HTML

- Do not add Subject line in the email body.
- Follow the <<-- Email Content Guidelines --> for genrerating the email.
- Follow the <<-- HTML and CSS Formatting Guidelines --> for converting the email to HTML.

<<-- Email Content Guidelines -->
The email must:
- Be polite, confident, and enthusiastic.
- Include a clear subject line tailored to the position.
- Begin with a professional greeting.
- Introduce who I am and why I'm reaching out.
- Highlight how my skills and experience align with the job description.
- Include 1–2 lines that show familiarity with the company and express enthusiasm about the opportunity.
- Request a follow-up (e.g., call, meeting, or next steps).
- Mention that I've attached my resume.
- End with a professional sign-off including my name and contact information.
- Keep the email concise, personalized, and easy to read.
- **Do not copy the job description verbatim.**
- **Double-check for correct position title and company name.**

<<-- HTML and CSS Formatting Guidelines -->
**convert it into a visually appealing, responsive HTML email**. Your task is to format the email using modern email design principles.

Guidelines:
- Wrap the email in a clean HTML structure with `<html>`, `<head>`, and `<body>`.
- Use inline CSS for maximum email client compatibility.
- Apply a clean, professional color scheme:
    - Primary color: `#2E86C1` (headings, links, highlights)
    - Secondary background color: `#F4F6F7`
    - CTA buttons: `#F39C12` (orange) or `#27AE60` (green)
- Use professional fonts like Arial, Helvetica, or Segoe UI.
- Use larger font sizes and bold styles for headings.
- Highlight key sections with padding/margins and borders if needed.
- Add a CTA button for follow-up (e.g., "Schedule a Call") if found in the text.
- Keep the email responsive (mobile and desktop-friendly).
- Ensure accessibility: good contrast, alt text (if images are used), and simple structure.
- Do Not Generate Footer, Header.

Inputs:
COMPANY NAME: {company_name}
RECRUITER EMAIL: {recruiter_email}
JOB POSITION: {job_position}
JOB SOURCE: {job_source}

RESUME DETAILS:
{resume_details}

JOB DESCRIPTION:
{job_description}

COMPANY OVERVIEW:
{company_overview}
"""

# Additional prompt section for feedback
EMAIL_FEEDBACK_PROMPT = """
FEEDBACK FOR REGENERATION:
Please incorporate the following feedback when regenerating the email:
{feedback}
"""

from pydantic import BaseModel, EmailStr,Field

class JobDetails(BaseModel):
    company_name: str = Field(..., description="Name of the company")
    recruiter_email: str = Field(..., description="Email of the recruiter")
    job_position: str = Field(..., description="Position of the job")

class GenerateEmail(BaseModel):
    subject: str = Field(..., description="Subject of the email")
    body_text: str = Field(..., description="plain text Body of the email")
    body_html: str = Field(..., description="HTML Body of the email")


def get_user_input():
    job_position = input("Enter the job position: ")
    company_name = input("Enter the company name: ")
    job_source = input("Enter the job source: ")
    recruiter_email = input("Enter the recruiter's email: ")
    resume_path = input("Enter the path to your resume PDF: ")
    
    return {
        'job_position': job_position,
        'company_name': company_name,
        'job_source': job_source,
        'recruiter_email': recruiter_email,
        'resume_path': resume_path
    }

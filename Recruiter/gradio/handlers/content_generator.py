"""Content generation handler for emails and cover letters."""

from typing import Dict, Optional, Any, Tuple
import tempfile
import gradio as gr

from Recruiter.utils.config.config_manager import ConfigManager
from Recruiter.core.company_research.company_researcher import CompanyResearcher
from Recruiter.core.email.email_generator import EmailGenerator
from Recruiter.core.cover_letter.cover_letter_generator import CoverLetterGenerator
from Recruiter.gradio.handlers.file_handler import process_resume

def extract_details(api_key: str, job_desc: str) -> Tuple[str, str, str]:
    """
    Extract details from job description.
    
    Args:
        api_key: OpenAI API key
        job_desc: Job description text
        
    Returns:
        Tuple of (company_name, recruiter_email, job_position)
        
    Raises:
        gr.Error: If extraction fails
    """
    if not api_key:
        raise gr.Error("OpenAI API key is required to extract details.")
    
    if not job_desc:
        raise gr.Error("Please provide a job description.")
    
    try:
        company_researcher = CompanyResearcher(api_key=api_key)
        details = company_researcher.extract_details_from_job_description(job_desc)
        return (
            details.company_name,
            details.recruiter_email,
            details.job_position
        )
    except Exception as e:
        raise gr.Error(f"Error extracting details: {str(e)}")

def generate_content(
    api_key: str,
    generation_type: str,
    job_desc: str,
    company_name: str,
    job_position: str,
    resume_choice: str,
    resume_file: Optional[tempfile._TemporaryFileWrapper],
    recruiter_email: Optional[str] = None,
    job_source: Optional[str] = None,
    feedback: Optional[str] = None
) -> Dict[str, str]:
    """
    Generate email or cover letter content.
    
    Args:
        api_key: OpenAI API key
        generation_type: Type of content to generate ("Email" or "Cover Letter")
        job_desc: Job description
        company_name: Name of the company
        job_position: Job position title
        resume_choice: Choice between default or uploaded resume
        resume_file: Optional uploaded resume file
        recruiter_email: Optional recruiter email (required for email generation)
        job_source: Optional job source (required for email generation)
        feedback: Optional feedback for regeneration
        
    Returns:
        Dictionary containing generated content
        
    Raises:
        gr.Error: If required fields are missing or generation fails
    """
    # Validate required fields
    if not api_key:
        raise gr.Error("⚠️ OpenAI API key is required. Please add it in the Settings section.")
    
    if not job_desc:
        raise gr.Error("⚠️ Please provide a job description in the Job Description section.")
    
    if not company_name:
        raise gr.Error("⚠️ Company Name is required in the Job Details section.")
    
    if not job_position:
        raise gr.Error("⚠️ Job Position is required in the Job Details section.")
    
    # Additional validation for Email generation
    if generation_type == "Email":
        if not recruiter_email:
            raise gr.Error("⚠️ Recruiter Email is required for email generation.")
        if not job_source:
            raise gr.Error("⚠️ Job Source is required (e.g., LinkedIn, Company Website).")
    
    try:
        # Process resume
        resume, resume_filename = process_resume(resume_choice, resume_file)
        
        # Research company
        company_researcher = CompanyResearcher(api_key=api_key)
        company_info = company_researcher.research_company(company_name)
        if generation_type == "Email":
            # Generate email
            email_generator = EmailGenerator(api_key=api_key)
            email_content = email_generator.generate_email(
                job_desc,
                company_info,
                resume,
                recruiter_email,
                job_position,
                job_source,
                company_name,
                feedback=feedback
            )
            
            return {
                "subject": email_content.subject,
                "text": email_content.body_text,
                "html": email_content.body_html
            }
        else:
            # Generate cover letter
            cover_letter_generator = CoverLetterGenerator(api_key=api_key)
            cover_letter_content = cover_letter_generator.generate_cover_letter(
                job_desc,
                company_info,
                resume,
                job_position,
                company_name,
                feedback=feedback
            )
            
            return {
                "text": cover_letter_content.content_text,
                "html": cover_letter_content.content_html
            }
    except Exception as e:
        raise gr.Error(f"Error generating content: {str(e)}")


if __name__ == "__main__":
    api_key = ConfigManager().get_value("openai","OPENAI_API_KEY")
    print(generate_content(api_key, generation_type="Email", job_desc="""
About the job
About BaaziGames:



Baazi Games, India’s premier online gaming network, has been revolutionizing the industry since2014 with indigenous platforms like PokerBaazi, CardBaazi, and SportsBaazi. With over 12 million users, Baazi Games has emerged as a tech-driven powerhouse blending innovation with real-money gaming.


What you’ll do 
you will be at postion of Data Scientist, where you will be responsible for:
Analyse large datasets related to player behaviour, transactions, and gameplay to uncover actionable insights.
Develop predictive models and machine learning algorithms for user engagement, retention, and fraud detection.
Collaborate with data engineers and product teams to define and enhance key metrics for measuring user activity and overall platform health.
Create dashboards and reports to monitor real-time performance, ensuring data-driven decision-making across teams.
Design A/B tests and conduct cohort analysis to measure the effectiveness of new game features and player-targeting strategies.
Continuously research and implement new techniques to enhance player segmentation and game optimization.
Act as a subject matter expert in data analysis, providing guidance to internal teams on best practices and methodologies.
Synthesize complex data into easy-to-understand insights for non-technical stakeholders.


Qualifications



Proficiency in SQL, Python, and statistical modelling techniques.
Experience working with large datasets and querying data to derive insights.
Familiarity with machine learning algorithms and predictive modelling.
Strong background in statistics and experience with A/B testing, cohort analysis, and player segmentation.
Excellent communication skills and ability to present data-driven insights to both technical and non-technical audiences.
Previous experience in the gaming or entertainment industry is a plus but not mandatory.
Familiarity with cloud data platforms like AWS Athena, Redshift, or similar tools.


What Makes You a True Baazigar? 
A True Baazigar isn’t just about taking chances; it's about playing to win. You’re customer-focused, always thinking, "How can I make their experience better?" You take ownership of every move and aren’t afraid of challenges. You trust data and technology to guide your decisions, and you’re committed to delivering game-winning solutions. Ready to roll the dice and make things happen? The world’s your playing field! 

 
Perks of Being a Baazigar 
 
All in at PokerBaazi – Here’s what you get: 
Competitive salary and growth opportunities 
Instant Recognition Programs and Achiever’s Awards 
Learning & Development reimbursements up to 10% of your CTC 
Flexi Benefits and customized perk options 
Farmhouse Workstation with a pet-friendly office 
Full ownership and autonomy from Day 1 
Inclusive Maternity and Paternity benefits 
 Ready to Go All In? 
If you're driven by high-stakes challenges, love building seamless gaming experiences, and thrive at the intersection of tech and thrill—then this is your table. Join the PokerBaazi crew and bring your A-game. 

mail you resume to [sourav@baazigames.com]
Come be a Baazigar. """, job_position="Data Scientist", company_name="Baazi Games", resume_choice="Use Default Resume", resume_file=None, recruiter_email="Extraitem123@gmai.com", job_source="LinkedIn", feedback=None))
    
"""
Email formatter module to convert plain text email content into formatted HTML using LLM.
"""
from RecruitReach_AI.models.llm_manager import get_llm

def format_email_to_html(email_body: str) -> str:
    """
    Convert plain text email content into formatted HTML using LLM.
    
    Args:
        email_body (str): Plain text email content
        
    Returns:
        str: Formatted HTML email content with styling
    """
    # Initialize LLM
    llm = get_llm()
    
    # Create the complete prompt with the email body
    prompt = f"""
    {formatter_prompt}

    Here's the email content to format:
    {email_body}
    
    Please generate the complete HTML code with embedded CSS styling.
    """
    
    # Get HTML formatted email from LLM
    response = llm.invoke(prompt)
    
    return response

if __name__ == "__main__":
    # Example usage
    sample_email = """
    Dear Hiring Manager,

    I am writing to express my strong interest in the Software Engineer position at TechCorp. With my background in Python and machine learning, I believe I would be a valuable addition to your team.

    During my experience at previous companies, I have worked extensively with AWS and Docker, developing scalable solutions for complex problems.

    I look forward to discussing how my skills align with your needs.

    Best regards,
    John Doe
    """
    
    formatted_html = format_email_to_html(sample_email)
    print(formatted_html.content[7:-3])

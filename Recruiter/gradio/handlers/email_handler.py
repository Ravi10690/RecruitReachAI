"""Email sending handler."""

from typing import Optional
import tempfile
import gradio as gr
from Recruiter.services.email_service.email_sender import EmailSenderService
from Recruiter.utils.file_utils.path_manager import PathManager

def send_email(
    sender_email: str,
    sender_name: str,
    app_password: str,
    receiver_email: str,
    subject: str,
    html_body: str,
    resume_choice: str,
    resume_file: Optional[tempfile._TemporaryFileWrapper]
) -> str:
    """
    Send email with resume attachment.
    
    Args:
        sender_email: Sender's email address
        sender_name: Sender's name
        app_password: Email app password
        receiver_email: Recipient's email address
        subject: Email subject
        html_body: HTML content of the email
        resume_choice: Choice between default or uploaded resume
        resume_file: Optional uploaded resume file
        
    Returns:
        Success message if email is sent successfully
        
    Raises:
        gr.Error: If email sending fails
    """
    if not all([sender_email, sender_name, app_password]):
        raise gr.Error("Please configure email settings.")
    
    try:
        # Initialize EmailSenderService
        email_sender = EmailSenderService(
            sender_email=sender_email,
            sender_name=sender_name,
            app_password=app_password
        )
        
        # Get resume attachment
        attachment = None
        attachment_filename = None
        
        if resume_choice == "Use Default Resume":
            path_manager = PathManager()
            attachment = str(path_manager.get_resume_path())
            attachment_filename = "resume.pdf"
        elif resume_file:
            attachment = resume_file.read()
            attachment_filename = resume_file.name
        
        # Send email
        success = email_sender.send_email(
            receiver_email=receiver_email,
            subject=subject,
            html_body=html_body,
            attachment=attachment,
            attachment_filename=attachment_filename
        )
        
        if success:
            return "✅ Email sent successfully!"
        else:
            raise gr.Error("Failed to send email. Please check your email settings.")
    except Exception as e:
        raise gr.Error(f"Error sending email: {str(e)}")

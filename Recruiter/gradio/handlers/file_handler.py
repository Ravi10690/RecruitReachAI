"""File handling utilities."""

from typing import Optional, Tuple, Any
import tempfile
from Recruiter.core.resume.resume_parser import ResumeParser
import gradio as gr

def process_resume(resume_choice: str, resume_file: Optional[tempfile._TemporaryFileWrapper] = None) -> Tuple[Any, str]:
    """
    Process the resume based on choice and file.
    
    Args:
        resume_choice: Choice between default or uploaded resume
        resume_file: Optional uploaded resume file
        
    Returns:
        Tuple containing processed resume and filename
        
    Raises:
        gr.Error: If resume processing fails
    """
    resume_parser = ResumeParser()
    
    if resume_choice == "Use Default Resume":
        try:
            resume = resume_parser.load_default_resume()
            filename = "default_resume.pdf"
        except FileNotFoundError:
            raise gr.Error("⚠️ Default resume not found. Please either upload a resume or ensure the default resume exists.")
    else:
        if resume_file is None:
            raise gr.Error("⚠️ Please upload a resume file (PDF or DOCX) before proceeding.")
        try:
            resume = resume_parser.load_resume_from_bytes(
                resume_file.read(),
                resume_file.name
            )
            filename = resume_file.name
        except Exception as e:
            raise gr.Error(f"⚠️ Error parsing resume: {str(e)}. Please ensure the file is a valid PDF or DOCX document.")
    
    return resume, filename

def load_job_desc_from_file(file: Optional[tempfile._TemporaryFileWrapper]) -> str:
    """
    Load job description from an uploaded file.
    
    Args:
        file: Uploaded file containing job description
        
    Returns:
        String containing the job description
    """
    if file is None:
        return ""
    return file.read().decode()

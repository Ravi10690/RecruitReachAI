"""
Main Streamlit application for RecruitReach2.

This module provides the main Streamlit application for the RecruitReach2 project.
"""

import os
import io
import re
import streamlit as st
from typing import Optional, Dict, Any, Tuple

from PyPDF2 import PdfReader
from docx import Document

from RecruitReachAI.Recruiter.core.resume.resume_parser import ResumeParser
from RecruitReachAI.Recruiter.core.company_research.company_researcher import CompanyResearcher
from RecruitReachAI.Recruiter.core.email.email_generator import EmailGenerator
from RecruitReachAI.Recruiter.core.cover_letter.cover_letter_generator import CoverLetterGenerator
from RecruitReachAI.Recruiter.services.email_service.email_sender import EmailSenderService
from RecruitReachAI.Recruiter.utils.config.config_manager import ConfigManager
from RecruitReachAI.Recruiter.utils.file_utils.path_manager import PathManager


# Email validation regex pattern
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


def is_valid_email(email: str) -> bool:
    """
    Check if an email address is valid.
    
    Args:
        email: Email address to check.
        
    Returns:
        True if the email is valid, False otherwise.
    """
    return bool(re.match(EMAIL_PATTERN, email))


def get_config_values() -> Dict[str, str]:
    """
    Get configuration values from config.toml.
    
    Returns:
        Dictionary containing configuration values.
    """
    try:
        # ConfigManager now automatically loads config.toml if it exists
        config_manager = ConfigManager()
        app_config = config_manager.get_app_config()
        
        return {
            'openai_api_key': app_config.api.openai_api_key if app_config.api else '',
            'sender_email': app_config.email.sender_email if app_config.email else '',
            'sender_name': app_config.email.sender_name if app_config.email else '',
            'app_password': app_config.email.app_password if app_config.email else ''
        }
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")
        return {
            'openai_api_key': '',
            'sender_email': '',
            'sender_name': '',
            'app_password': ''
        }


def initialize_session_state() -> None:
    """Initialize session state variables."""
    # Initialize config values
    if 'config_values' not in st.session_state:
        st.session_state.config_values = get_config_values()
    
    # Initialize config-related session state variables
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = st.session_state.config_values.get('openai_api_key', '')
    if 'sender_email' not in st.session_state:
        st.session_state.sender_email = st.session_state.config_values.get('sender_email', '')
    if 'sender_name' not in st.session_state:
        st.session_state.sender_name = st.session_state.config_values.get('sender_name', '')
    if 'app_password' not in st.session_state:
        st.session_state.app_password = st.session_state.config_values.get('app_password', '')
    
    # Initialize generation type
    if 'generation_type' not in st.session_state:
        st.session_state.generation_type = "email"
    
    # Initialize content-related state
    if 'generated_email' not in st.session_state:
        st.session_state.generated_email = None
    if 'generated_cover_letter' not in st.session_state:
        st.session_state.generated_cover_letter = None
    
    # Initialize input-related state
    if 'extracted_details' not in st.session_state:
        st.session_state.extracted_details = None
    if 'job_desc' not in st.session_state:
        st.session_state.job_desc = None
    if 'company_info' not in st.session_state:
        st.session_state.company_info = None
    if 'resume' not in st.session_state:
        st.session_state.resume = None
    if 'uploaded_resume' not in st.session_state:
        st.session_state.uploaded_resume = None
    if 'resume_choice' not in st.session_state:
        st.session_state.resume_choice = "default"
    if 'company_name' not in st.session_state:
        st.session_state.company_name = None
    if 'recruiter_email' not in st.session_state:
        st.session_state.recruiter_email = None
    if 'job_position' not in st.session_state:
        st.session_state.job_position = None
    if 'job_source' not in st.session_state:
        st.session_state.job_source = None
    if 'resume_filename' not in st.session_state:
        st.session_state.resume_filename = None
    if 'email_subject' not in st.session_state:
        st.session_state.email_subject = None
    
    # Initialize theme state
    if 'theme' not in st.session_state:
        st.session_state.theme = "dark"  # Default theme


def load_css() -> str:
    """
    Load CSS styles for the application.
    
    Returns:
        CSS styles as a string.
    """
    # Define theme colors based on current theme
    if st.session_state.theme == "dark":
        # Dark theme colors
        primary_color = "#4F6AFF"
        secondary_color = "#6E56CF"
        background_color = "#000000"
        card_background = "#2D2D44"
        text_color = "#FFFFFF"
        subtext_color = "#CCCCCC"
        border_color = "#3F3F5F"
        success_color = "#4CAF50"
        error_color = "#FF5252"
        input_background = "#252538"
    else:
        # Light theme colors
        primary_color = "#4F6AFF"
        secondary_color = "#6E56CF"
        background_color = "#F8F9FA"
        card_background = "#FFFFFF"
        text_color = "#333333"
        subtext_color = "#666666"
        border_color = "#E0E0E0"
        success_color = "#4CAF50"
        error_color = "#FF5252"
        input_background = "#F0F2F6"
    
    # CSS template
    css = """
    /* Global Styles */
    .stApp {
        background-color: %s;
        color: %s;
    }
    
    /* Card Styles */
    .card {
        background-color: %s;
        border-radius: 10px;
        border: 1px solid %s;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Button Styles */
    .stButton > button {
        background-color: %s;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: %s;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Input Styles */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: %s;
        color: %s;
        border: 1px solid %s;
        border-radius: 5px;
    }
    
    /* Alert Styles */
    .stAlert {
        border-radius: 5px;
        padding: 10px 15px;
        margin-bottom: 15px;
    }
    
    .success {
        background-color: %s;
        color: white;
    }
    
    .error {
        background-color: %s;
        color: white;
    }
    
    .stInfo {
        background-color: %s;
        color: white;
    }
    
    /* Preview Container */
    .preview-container {
        background-color: %s;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid %s;
    }
    
    .subject-line {
        background-color: %s;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease-out forwards;
    }
    """ % (
        background_color, text_color,
        card_background, border_color,
        primary_color, secondary_color,
        input_background, text_color, border_color,
        success_color, error_color, primary_color,
        card_background, border_color,
        input_background
    )
    
    return css


def main() -> None:
    """Main application function."""
    st.set_page_config(
        page_title="RecruitReach AI",
        page_icon="✉️",
        layout="wide"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Apply CSS styles
    st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)
    
    # Add animation script
    st.markdown("""
    <script>
    document.addEventListener("DOMContentLoaded", function() {
      var cards = document.querySelectorAll(".card");
      for (var i = 0; i < cards.length; i++) {
        cards[i].classList.add("animate-fade-in");
      }
    });
    </script>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.title("⚙️ Configuration")
    
    # Generation type selection
    generation_type = st.sidebar.radio(
        "Select Generation Type:",
        ["Email", "Cover Letter"],
        index=0 if st.session_state.generation_type == "email" else 1
    )
    
    if generation_type == "Email":
        st.session_state.generation_type = "email"
        page_title = "✉️ AI Email Generator for Job Applications"
    else:
        st.session_state.generation_type = "cover_letter"
        page_title = "📝 AI Cover Letter Generator for Job Applications"
    
    # Configuration Section
    st.sidebar.subheader("API Settings")
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        value=st.session_state.openai_api_key,
        type="password",
        help="Enter your OpenAI API key"
    )
    if openai_api_key != st.session_state.openai_api_key:
        st.session_state.openai_api_key = openai_api_key
    
    # Email Configuration (only show if email generation is selected)
    if st.session_state.generation_type == "email":
        st.sidebar.subheader("Email Settings")
        sender_email = st.sidebar.text_input(
            "Sender Email",
            value=st.session_state.sender_email,
            help="Enter your email address"
        )
        if sender_email != st.session_state.sender_email:
            st.session_state.sender_email = sender_email
        
        sender_name = st.sidebar.text_input(
            "Sender Name",
            value=st.session_state.sender_name,
            help="Enter your name"
        )
        if sender_name != st.session_state.sender_name:
            st.session_state.sender_name = sender_name
        
        app_password = st.sidebar.text_input(
            "Email App Password",
            value=st.session_state.app_password,
            type="password",
            help="Enter your email app password"
        )
        if app_password != st.session_state.app_password:
            st.session_state.app_password = app_password
    
    # Add theme toggle in sidebar
    with st.sidebar:
        st.write("")  # Add some space
        theme_col1, theme_col2 = st.columns([1, 1])
        with theme_col1:
            st.write("Theme:")
        with theme_col2:
            if st.button("🌙 Dark" if st.session_state.theme == "light" else "☀️ Light"):
                st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
                st.rerun()
    
    # Main content
    st.title(page_title)
    
    if st.session_state.generation_type == "email":
        st.write("Generate personalized emails for job applications using AI")
    else:
        st.write("Generate professional cover letters for job applications using AI")
    
    # Create three columns for layout with wider middle column
    col1, col2, col3 = st.columns([1, 3, 1.5])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("📄 Resume")
        resume_choice = st.radio("Choose resume option:", ["Use Default Resume", "Upload Resume"], index=None)
        st.session_state.resume_choice = resume_choice
        
        if resume_choice == "Use Default Resume":
            st.markdown('<div class="stInfo">', unsafe_allow_html=True)
            st.info("Using default resume from your profile")
            st.markdown('</div>', unsafe_allow_html=True)
        elif resume_choice == "Upload Resume":
            resume_uploader = st.file_uploader("Upload your resume", type=['pdf', 'docx'], key="resume_upload")
            if resume_uploader is not None:
                try:
                    file_content = resume_uploader.read()
                    # Store the uploaded file content and name
                    st.session_state.uploaded_resume = file_content
                    st.session_state.resume_filename = resume_uploader.name
                    st.markdown('<div class="success">', unsafe_allow_html=True)
                    st.success(f"Resume '{resume_uploader.name}' uploaded successfully!")
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown('<div class="error">', unsafe_allow_html=True)
                    st.error(f"Error uploading resume: {str(e)}")
                    st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("📝 Job Description")
        input_method = st.radio("Choose input method:", ["Text Input", "File Upload"])
        
        job_desc = ""
        if input_method == "Text Input":
            job_desc = st.text_area(
                "Enter the job description:",
                height=150,
                placeholder="Paste the job description here...",
                key="job_description_input"
            )
        else:
            uploaded_file = st.file_uploader("Upload JD file", type=['txt'])
            if uploaded_file:
                try:
                    job_desc = uploaded_file.getvalue().decode()
                    st.markdown('<div class="success">', unsafe_allow_html=True)
                    st.success("File uploaded successfully!")
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown('<div class="error">', unsafe_allow_html=True)
                    st.error(f"Error reading file: {str(e)}")
                    st.markdown('</div>', unsafe_allow_html=True)
        
        # Extract details button
        col_extract1, col_extract2, col_extract3 = st.columns([1, 1, 1])
        with col_extract2:
            if st.button("🔍 Extract Details", type="primary"):
                if not st.session_state.openai_api_key:
                    st.markdown('<div class="error">', unsafe_allow_html=True)
                    st.error("OpenAI API key is required to extract details from job description.")
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.stop()
                
                if job_desc:
                    try:
                        with st.spinner("Extracting details from job description..."):
                            company_researcher = CompanyResearcher(api_key=st.session_state.openai_api_key)
                            st.session_state.extracted_details = company_researcher.extract_details_from_job_description(job_desc)
                            st.markdown('<div class="success">', unsafe_allow_html=True)
                            st.success("Details extracted successfully!")
                            st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown('<div class="error">', unsafe_allow_html=True)
                        st.error(f"Error extracting details: {str(e)}")
                        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("details_form", clear_on_submit=False):
            st.header("🎯 Job Details")
            
            # Use extracted details as default values if available
            company_name = st.text_input(
                "Company Name",
                value=st.session_state.extracted_details.company_name if st.session_state.extracted_details else "",
                placeholder="Enter company name..."
            )
            
            recruiter_email = st.text_input(
                "Recruiter Email",
                value=st.session_state.extracted_details.recruiter_email if st.session_state.extracted_details else "",
                placeholder="Enter recruiter's email..."
            )
            
            job_position = st.text_input(
                "Job Position",
                value=st.session_state.extracted_details.job_position if st.session_state.extracted_details else "",
                placeholder="Enter job position..."
            )
            
            job_source = st.text_input(
                "Job Source",
                placeholder="e.g., LinkedIn, Company Website..."
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Change button text based on generation type
            button_text = "✨ Generate Email" if st.session_state.generation_type == "email" else "✨ Generate Cover Letter"
            generate_button = st.form_submit_button(button_text, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if generate_button:
            # Validate inputs
            if not job_desc:
                st.error("Please provide a job description.")
            elif not company_name:
                st.error("Please enter the company name.")
            elif st.session_state.generation_type == "email" and not recruiter_email:
                st.error("Please enter the recruiter's email.")
            elif st.session_state.generation_type == "email" and not is_valid_email(recruiter_email):
                st.error("Please enter a valid email address.")
            elif not job_position:
                st.error("Please enter the job position.")
            elif st.session_state.generation_type == "email" and not job_source:
                st.error("Please enter the job source.")
            else:
                try:
                    # Load resume
                    with st.spinner("Loading resume..."):
                        resume_parser = ResumeParser()
                        
                        if st.session_state.resume_choice == "Use Default Resume":
                            try:
                                resume = resume_parser.load_default_resume()
                            except FileNotFoundError:
                                st.error("Default resume not found. Please upload a resume.")
                                st.stop()
                        else:
                            if st.session_state.uploaded_resume:
                                try:
                                    resume = resume_parser.load_resume_from_bytes(
                                        st.session_state.uploaded_resume,
                                        st.session_state.resume_filename
                                    )
                                except Exception as e:
                                    st.error(f"Error parsing resume: {str(e)}")
                                    st.stop()
                            else:
                                st.error("Please upload a resume first.")
                                st.stop()
                    
                    # Research company
                    with st.spinner("Researching company..."):
                        if not st.session_state.openai_api_key:
                            st.error("OpenAI API key is required to research company information.")
                            st.stop()
                        
                        company_researcher = CompanyResearcher(api_key=st.session_state.openai_api_key)
                        company_info = company_researcher.research_company(company_name)
                    
                    # Store common variables in session state
                    st.session_state.job_desc = job_desc
                    st.session_state.company_info = company_info
                    st.session_state.resume = resume
                    st.session_state.company_name = company_name
                    st.session_state.job_position = job_position
                    
                    if st.session_state.generation_type == "email":
                        # Generate email
                        with st.spinner("Generating personalized email..."):
                            if not st.session_state.openai_api_key:
                                st.error("OpenAI API key is required to generate emails.")
                                st.stop()
                            
                            email_generator = EmailGenerator(api_key=st.session_state.openai_api_key)
                            email_content = email_generator.generate_email(
                                job_desc,
                                company_info,
                                resume,
                                recruiter_email,
                                job_position,
                                job_source,
                                company_name
                            )
                            
                            # Store email-specific variables
                            st.session_state.recruiter_email = recruiter_email
                            st.session_state.job_source = job_source
                            st.session_state.email_subject = email_content.subject
                            st.session_state.generated_email = {
                                "text": email_content.body_text,
                                "html": email_content.body_html
                            }
                            st.session_state.generated_cover_letter = None
                            
                            st.success("Email generated successfully!")
                    else:
                        # Generate cover letter
                        with st.spinner("Generating professional cover letter..."):
                            if not st.session_state.openai_api_key:
                                st.error("OpenAI API key is required to generate cover letters.")
                                st.stop()
                            
                            cover_letter_generator = CoverLetterGenerator(api_key=st.session_state.openai_api_key)
                            cover_letter_content = cover_letter_generator.generate_cover_letter(
                                job_desc,
                                company_info,
                                resume,
                                job_position,
                                company_name
                            )
                            
                            # Store cover letter in session state
                            st.session_state.generated_cover_letter = {
                                "text": cover_letter_content.content_text,
                                "html": cover_letter_content.content_html
                            }
                            st.session_state.generated_email = None
                            
                            st.success("Cover letter generated successfully!")
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating content: {str(e)}")
    
    # Display generated email
    if st.session_state.generated_email:
        st.markdown('<div class="card animate-fade-in">', unsafe_allow_html=True)
        st.header("📧 Generated Email")
        
        # Create columns for the email display and actions
        email_col1, email_col2 = st.columns([3, 1])
        
        with email_col1:
            # Display email subject and HTML preview in a container
            st.markdown('<div class="preview-container">', unsafe_allow_html=True)
            st.markdown("#### Email Preview")
            
            # Email stats and preview mode selector
            stats_col1, stats_col2 = st.columns([2, 1])
            
            plain_text = st.session_state.generated_email.get("text")
            word_count = len(plain_text.split())
            char_count = len(plain_text)
            
            with stats_col1:
                st.caption(f"📝 {word_count} words | {char_count} characters")
            
            with stats_col2:
                view_mode = st.radio(
                    "View as:",
                    ["Rich HTML", "Plain Text"],
                    horizontal=True,
                    key="preview_mode"
                )
            
            # Subject line
            st.markdown(
                f"""
                <div class="subject-line">
                    <strong>Subject:</strong> {st.session_state.email_subject}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Preview container
            with st.container():
                if view_mode == "Rich HTML":
                    st.markdown("""
                        <div style="padding: 20px; background-color: white; border-radius: 8px; border: 1px solid #ddd;">
                    """, unsafe_allow_html=True)
                    st.components.v1.html(
                        st.session_state.generated_email.get("html"),
                        height=600,
                        scrolling=True
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    # Display plain text in a monospace font
                    st.text_area(
                        "",
                        plain_text,
                        height=600,
                        key="plain_text_preview",
                        help="Plain text version of the email"
                    )
            
            # Keep hidden text areas for copying
            st.markdown(
                f"""
                <div style="display: none;">
                    <textarea id="email_subject">{st.session_state.email_subject}</textarea>
                    <textarea id="email_content">{st.session_state.generated_email}</textarea>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with email_col2:
            st.markdown("### Actions")
            
            # Copy options
            copy_option = st.radio(
                "Copy Format:",
                ["HTML Format", "Plain Text"],
                key="copy_format"
            )
            
            if st.button("📋 Copy to Clipboard"):
                if copy_option == "HTML Format":
                    st.markdown(
                        """
                        <script>
                            var subject = document.getElementById('email_subject').value;
                            var content = document.getElementById('email_content').value;
                            navigator.clipboard.writeText(content);
                        </script>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    # Strip HTML tags for plain text
                    st.markdown(
                        """
                        <script>
                            var subject = document.getElementById('email_subject').value;
                            var content = document.getElementById('email_content').value;
                            var tempDiv = document.createElement('div');
                            tempDiv.innerHTML = content;
                            var plainText = 'Subject: ' + subject + '\\n\\n' + tempDiv.textContent;
                            navigator.clipboard.writeText(plainText);
                        </script>
                        """,
                        unsafe_allow_html=True
                    )
                st.success("Copied to clipboard!")
            
            # Send Email button
            if st.button("📤 Send Email", type="primary"):
                try:
                    # Validate email settings
                    if not all([st.session_state.sender_email, st.session_state.sender_name, st.session_state.app_password]):
                        st.error("Please configure email settings in the sidebar.")
                        st.stop()
                    
                    # Initialize EmailSenderService
                    email_sender = EmailSenderService(
                        sender_email=st.session_state.sender_email,
                        sender_name=st.session_state.sender_name,
                        app_password=st.session_state.app_password
                    )
                    
                    # Get PDF content
                    attachment = None
                    if st.session_state.resume_choice == "Use Default Resume":
                        path_manager = PathManager()
                        attachment = str(path_manager.get_resume_path())
                    elif st.session_state.uploaded_resume:
                        attachment = st.session_state.uploaded_resume
                    
                    # Send email
                    success = email_sender.send_email(
                        receiver_email=st.session_state.recruiter_email,
                        subject=st.session_state.email_subject,
                        html_body=st.session_state.generated_email.get("html"),
                        attachment=attachment,
                        attachment_filename=st.session_state.resume_filename
                    )
                    
                    if success:
                        st.success("✅ Email sent successfully!")
                    else:
                        st.error("Failed to send email. Please check your email settings.")
                except Exception as e:
                    st.error(f"Error sending email: {str(e)}")
            
            # Regenerate with feedback section
            st.markdown("### Feedback")
            feedback = st.text_area(
                "Provide feedback for regeneration:",
                placeholder="What would you like to change in the email?"
            )
            
            if st.button("🔄 Regenerate Email") and feedback:
                try:
                    with st.spinner("Regenerating email with feedback..."):
                        if not st.session_state.openai_api_key:
                            st.error("OpenAI API key is required to regenerate emails.")
                            st.stop()
                        
                        email_generator = EmailGenerator(api_key=st.session_state.openai_api_key)
                        email_content = email_generator.generate_email(
                            st.session_state.job_desc,
                            st.session_state.company_info,
                            st.session_state.resume,
                            st.session_state.recruiter_email,
                            st.session_state.job_position,
                            st.session_state.job_source,
                            st.session_state.company_name,
                            feedback=feedback
                        )
                        
                        st.session_state.email_subject = email_content.subject
                        st.session_state.generated_email = {
                            "text": email_content.body_text,
                            "html": email_content.body_html
                        }
                        
                        st.success("Email regenerated successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error regenerating email: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display generated cover letter
    elif st.session_state.generated_cover_letter:
        st.markdown('<div class="card animate-fade-in">', unsafe_allow_html=True)
        st.header("📝 Generated Cover Letter")
        
        # Create columns for the cover letter display and actions
        cover_letter_col1, cover_letter_col2 = st.columns([3, 1])
        
        with cover_letter_col1:
            # Display cover letter preview in a container
            st.markdown('<div class="preview-container">', unsafe_allow_html=True)
            st.markdown("#### Cover Letter Preview")
            
            # Cover letter stats and preview mode selector
            stats_col1, stats_col2 = st.columns([2, 1])
            
            plain_text = st.session_state.generated_cover_letter.get("text")
            word_count = len(plain_text.split())
            char_count = len(plain_text)
            
            with stats_col1:
                st.caption(f"📝 {word_count} words | {char_count} characters")
            
            with stats_col2:
                view_mode = st.radio(
                    "View as:",
                    ["Rich HTML", "Plain Text"],
                    horizontal=True,
                    key="cover_letter_preview_mode"
                )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Preview container
            with st.container():
                if view_mode == "Rich HTML":
                    st.markdown("""
                        <div style="padding: 20px; background-color: white; border-radius: 8px; border: 1px solid #ddd;">
                    """, unsafe_allow_html=True)
                    st.components.v1.html(
                        st.session_state.generated_cover_letter.get("html"),
                        height=600,
                        scrolling=True
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    # Display plain text in a monospace font
                    st.text_area(
                        "",
                        plain_text,
                        height=600,
                        key="cover_letter_plain_text_preview",
                        help="Plain text version of the cover letter"
                    )
            
            # Keep hidden text areas for copying
            st.markdown(
                f"""
                <div style="display: none;">
                    <textarea id="cover_letter_content_text">{plain_text}</textarea>
                    <textarea id="cover_letter_content_html">{st.session_state.generated_cover_letter.get("html")}</textarea>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with cover_letter_col2:
            st.markdown("### Actions")
            
            # Copy options
            copy_option = st.radio(
                "Copy Format:",
                ["HTML Format", "Plain Text"],
                key="cover_letter_copy_format"
            )
            
            if st.button("📋 Copy to Clipboard", key="copy_cover_letter"):
                if copy_option == "HTML Format":
                    st.markdown(
                        """
                        <script>
                            var content = document.getElementById('cover_letter_content_html').value;
                            navigator.clipboard.writeText(content);
                        </script>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    # Copy plain text
                    st.markdown(
                        """
                        <script>
                            var plainText = document.getElementById('cover_letter_content_text').value;
                            navigator.clipboard.writeText(plainText);
                        </script>
                        """,
                        unsafe_allow_html=True
                    )
                st.success("Copied to clipboard!")
            
            # Download options
            download_format = st.radio(
                "Download Format:",
                ["HTML", "Text"],
                key="cover_letter_download_format"
            )
            
            if download_format == "HTML":
                html_content = st.session_state.generated_cover_letter.get("html")
                st.download_button(
                    label="📥 Download HTML",
                    data=html_content,
                    file_name="cover_letter.html",
                    mime="text/html"
                )
            else:
                text_content = st.session_state.generated_cover_letter.get("text")
                st.download_button(
                    label="📥 Download Text",
                    data=text_content,
                    file_name="cover_letter.txt",
                    mime="text/plain"
                )
            
            # Regenerate with feedback section
            st.markdown("### Feedback")
            feedback = st.text_area(
                "Provide feedback for regeneration:",
                placeholder="What would you like to change in the cover letter?",
                key="cover_letter_feedback"
            )
            
            if st.button("🔄 Regenerate Cover Letter") and feedback:
                try:
                    with st.spinner("Regenerating cover letter with feedback..."):
                        if not st.session_state.openai_api_key:
                            st.error("OpenAI API key is required to regenerate cover letters.")
                            st.stop()
                        
                        cover_letter_generator = CoverLetterGenerator(api_key=st.session_state.openai_api_key)
                        cover_letter_content = cover_letter_generator.generate_cover_letter(
                            st.session_state.job_desc,
                            st.session_state.company_info,
                            st.session_state.resume,
                            st.session_state.job_position,
                            st.session_state.company_name,
                            feedback=feedback
                        )
                        
                        st.session_state.generated_cover_letter = {
                            "text": cover_letter_content.content_text,
                            "html": cover_letter_content.content_html
                        }
                        
                        st.success("Cover letter regenerated successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error regenerating cover letter: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()

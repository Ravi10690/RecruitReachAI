import streamlit as st
from RecruitReachAI.RecruitReach_AI.prompts.prompt import base_prompt
from RecruitReachAI.RecruitReach_AI.models.llm_manager import get_llm
from RecruitReachAI.RecruitReach_AI.Resume.resume_parser import load_resume
from RecruitReachAI.RecruitReach_AI.Comapny_Reserch.company_research import research_company
from RecruitReachAI.RecruitReach_AI.Comapny_Reserch.extractComapnyDetails import extract_details_from_jd
from RecruitReachAI.RecruitReach_AI.Email.email_generator import generate_email
from RecruitReachAI.RecruitReach_AI.Email.email_sender import EmailSender
import re
import io
import html
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from docx import Document

# Email validation regex pattern
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def is_valid_email(email):
    return bool(re.match(EMAIL_PATTERN, email))

def main():
    st.set_page_config(
        page_title="AI Email Generator",
        page_icon="✉️",
        layout="wide"
    )
    
    st.title("✉️ AI Email Generator for Job Applications")
    st.write("Generate personalized emails for job applications using AI")

    # Initialize session states
    if 'extracted_details' not in st.session_state:
        st.session_state.extracted_details = None
    if 'generated_email' not in st.session_state:
        st.session_state.generated_email = None
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

    # Add styles
    st.markdown("""
    <style>
    .job-details-form {
        border: 1px solid #ddd;
        padding: 20px;
        border-radius: 5px;
        background-color: white;
    }
    .email-preview {
        border: 2px solid #4CAF50;
        padding: 20px;
        border-radius: 8px;
        background-color: white;
        font-family: Arial, sans-serif;
        white-space: pre-wrap;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMarkdown {
        background-color: white;
    }
    iframe {
        border: 1px solid #ddd;
        border-radius: 8px;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    textarea {
        font-family: 'Courier New', Courier, monospace !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Create two columns for layout
    col1, col2 = st.columns([3, 2])

    with col1:
        st.header("📝 Job Description")
        input_method = st.radio("Choose input method:", ["Text Input", "File Upload"])
        
        job_desc = ""
        if input_method == "Text Input":
            job_desc = st.text_area("Enter the job description:", height=200, 
                                  placeholder="Paste the job description here...")
        else:
            uploaded_file = st.file_uploader("Upload JD file", type=['txt'])
            if uploaded_file:
                try:
                    job_desc = uploaded_file.getvalue().decode()
                    st.success("File uploaded successfully!")
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")

        # Resume section
        st.header("📄 Resume")
        resume_choice = st.radio("Choose resume option:", ["Use Default Resume", "Upload Resume"],index=None)
        st.session_state.resume_choice = resume_choice
        if resume_choice == "Use Default Resume":
            st.info("Using default resume from your profile")
        elif resume_choice == "Upload Resume":
            resume_uploader = st.file_uploader("Upload your resume", type=['pdf', 'docx'], key="resume_upload")
            if resume_uploader is not None:
                try:
                    file_content = resume_uploader.read()
                    # Store the uploaded file content and name
                    st.session_state.uploaded_resume = file_content
                    st.session_state.resume_filename = resume_uploader.name
                    st.success(f"Resume '{resume_uploader.name}' uploaded successfully!")
                except Exception as e:
                    st.error(f"Error uploading resume: {str(e)}")
        
        # Add some spacing
        st.write("")
        
        # Extract details button in a smaller column
        extract_col1, extract_col2, extract_col3 = st.columns([1, 2, 1])
        with extract_col1:
                if st.button("🔍 Extract Details", type="primary"):
                    if job_desc:
                        try:
                            with st.spinner("Extracting details from job description..."):
                                st.session_state.extracted_details = extract_details_from_jd(job_desc)
                                st.success("Details extracted successfully!")
                        except Exception as e:
                            st.error(f"Error extracting details: {str(e)}")

    with col2:
        # Form for details
        with st.form("details_form", clear_on_submit=False):
            st.markdown('<div class="job-details-form">', unsafe_allow_html=True)
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
            
            st.markdown('</div>', unsafe_allow_html=True)
            generate_button = st.form_submit_button("✨ Generate Email")

            if generate_button:
                # Validate inputs
                if not job_desc:
                    st.error("Please provide a job description.")
                elif not company_name:
                    st.error("Please enter the company name.")
                elif not recruiter_email:
                    st.error("Please enter the recruiter's email.")
                elif not is_valid_email(recruiter_email):
                    st.error("Please enter a valid email address.")
                elif not job_position:
                    st.error("Please enter the job position.")
                elif not job_source:
                    st.error("Please enter the job source.")
                else:
                    try:
                        with st.spinner("Loading resume..."):
                            if st.session_state.resume_choice == "Use Default Resume":
                                resume = load_resume()
                            else:
                                if st.session_state.uploaded_resume:
                                    # Handle different file types
                                    if st.session_state.resume_filename.endswith('.pdf'):
                                        pdf_file = io.BytesIO(st.session_state.uploaded_resume)
                                        pdf_reader = PdfReader(pdf_file)
                                        resume = ""
                                        for page in pdf_reader.pages:
                                            resume += page.extract_text()
                                    elif st.session_state.resume_filename.endswith('.docx'):
                                        docx_file = io.BytesIO(st.session_state.uploaded_resume)
                                        doc = Document(docx_file)
                                        resume = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                                    else:
                                        st.error("Unsupported file type")
                                        return
                                else:
                                    st.error("Please upload a resume first.")
                                    return
                        
                        with st.spinner("Researching company..."):
                            company_info = research_company(company_name)
                        
                        with st.spinner("Generating personalized email..."):
                            email_content = generate_email(
                                job_desc,
                                company_info,
                                resume,
                                recruiter_email,
                                job_position,
                                job_source,
                                company_name
                            )
                            # Store all variables in session state
                            st.session_state.job_desc = job_desc
                            st.session_state.company_info = company_info
                            st.session_state.resume = resume
                            st.session_state.company_name = company_name
                            st.session_state.recruiter_email = recruiter_email
                            st.session_state.job_position = job_position
                            st.session_state.job_source = job_source
                            st.session_state.generated_email = email_content.get("body")
                            st.session_state.email_subject = email_content.get("subject")
                            st.success("Email generated successfully!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error generating email: {str(e)}")

    # Display generated email and actions
    if st.session_state.generated_email:
        st.header("📧 Generated Email")
        
        # Create columns for the email display and actions
        email_col1, email_col2 = st.columns([3, 1])
        
        with email_col1:
            # Display email subject and HTML preview in a container
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
                <div style="margin-bottom: 10px; padding: 10px; background-color: #f8f9fa; border-radius: 4px;">
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
                    email_sender = EmailSender()
                    
                    # Get PDF content
                    pdf_content = None
                    pdf_filename = None
                    if st.session_state.resume_choice == "Use Default Resume":
                        pdf_content = "RecruitReach_AI/data/Ravi_Ahuja_Resume.pdf"
                    elif st.session_state.uploaded_resume:
                        pdf_content = st.session_state.uploaded_resume
                        pdf_filename = st.session_state.resume_filename
                    
                    # Send email
                    success = email_sender.send_email(
                        receiver_email=st.session_state.recruiter_email,
                        html_body=st.session_state.generated_email.get("html"),
                        subject=st.session_state.email_subject,
                        pdf_content=pdf_content
                    )
                    
                    if success:
                        st.success("✅ Email sent successfully!")
                    else:
                        st.error("Failed to send email. Please check your email settings.")
                except Exception as e:
                    st.error(f"Error sending email: {str(e)}")
            
            # Regenerate with feedback section
            st.markdown("### Feedback")
            feedback = st.text_area("Provide feedback for regeneration:", 
                                  placeholder="What would you like to change in the email?")
            
            if st.button("🔄 Regenerate Email") and feedback:
                try:
                    with st.spinner("Regenerating email with feedback..."):
                        # Use variables from session state
                        email_content = generate_email(
                            st.session_state.job_desc,
                            st.session_state.company_info,
                            st.session_state.resume,
                            st.session_state.recruiter_email,
                            st.session_state.job_position,
                            st.session_state.job_source,
                            st.session_state.company_name,
                            feedback=feedback
                        )
                        st.session_state.generated_email = email_content.get("body")
                        st.session_state.email_subject = email_content.get("subject")
                        st.success("Email regenerated successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error regenerating email: {str(e)}")

if __name__ == "__main__":
    main()

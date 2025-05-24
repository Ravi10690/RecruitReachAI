"""Company details component for the Gradio application."""

import gradio as gr
from typing import Dict, Any

def create_company_details_component() -> Dict[str, Any]:
    """
    Create the company details component with company and recruiter information fields.
    
    Returns:
        Dictionary containing the component elements
    """
    with gr.Column(scale=1) as details_column:
        gr.Markdown("### 🎯 Job Details")
        
        company_name = gr.Textbox(
            label="Company Name",
            placeholder="Enter company name...",
            interactive=True
        )
        recruiter_email = gr.Textbox(
            label="Recruiter Email",
            placeholder="Enter recruiter's email...",
            interactive=True
        )
        job_position = gr.Textbox(
            label="Job Position",
            placeholder="Enter job position...",
            interactive=True
        )
        job_source = gr.Dropdown(
            label="Job Source",
            choices=["LinkedIn", "Naukri"],
            value="LinkedIn",
            interactive=True
        )
    
    return {
        "column": details_column,
        "company_name": company_name,
        "recruiter_email": recruiter_email,
        "job_position": job_position,
        "job_source": job_source
    }

def setup_extract_handler(
    components: Dict[str, Any],
    api_key: gr.Textbox,
    job_desc: gr.Textbox
) -> None:
    """
    Set up the extract details button handler.
    
    Args:
        components: Dictionary containing company details components
        api_key: OpenAI API key textbox
        job_desc: Job description textbox
    """
    from Recruiter.gradio.handlers.content_generator import extract_details
    
    components["extract_btn"].click(
        extract_details,
        inputs=[
            api_key,
            job_desc
        ],
        outputs=[
            components["company_name"],
            components["recruiter_email"],
            components["job_position"]
        ]
    )

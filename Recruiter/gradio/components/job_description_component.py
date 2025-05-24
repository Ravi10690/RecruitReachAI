"""Job description component for the Gradio application."""

import gradio as gr
from typing import Dict, Any
from Recruiter.gradio.handlers.file_handler import load_job_desc_from_file

def create_job_description_component() -> Dict[str, Any]:
    """
    Create the job description component with text input and file upload options.
    
    Returns:
        Dictionary containing the component elements
    """
    gr.Markdown("### 📝 Job Description")
    
    with gr.Tabs(elem_classes="tabs") as tabs:
        with gr.Tab("Text Input"):
            job_desc = gr.Textbox(
                label="Enter the job description",
                placeholder="Paste the job description here...",
                lines=20,
                elem_classes="textbox",
                interactive=True
            )
        with gr.Tab("File Upload"):
            job_desc_file = gr.File(
                label="Upload Job Description File",
                file_types=[".txt"]
            )
    
    # Set up file upload handler
    job_desc_file.upload(
        load_job_desc_from_file,
        inputs=[job_desc_file],
        outputs=[job_desc]
    )
    
    return {
        "tabs": tabs,
        "job_desc": job_desc,
        "job_desc_file": job_desc_file
    }

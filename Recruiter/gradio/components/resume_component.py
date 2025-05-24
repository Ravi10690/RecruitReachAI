"""Resume component for the Gradio application."""

import gradio as gr
from typing import Dict, Any

def create_resume_component() -> Dict[str, Any]:
    """
    Create the resume upload component with options for default or custom resume.
    
    Returns:
        Dictionary containing the component elements
    """
    gr.Markdown("### 📄 Resume")
    
    resume_choice = gr.Radio(
        choices=["Use Default Resume", "Upload Resume"],
        label="Choose resume option",
        value="Use Default Resume",
        interactive=True,
        info="Select whether to use the default resume or upload a new one"
    )
    
    resume_file = gr.File(
        label="Upload your resume (PDF or DOCX)",
        file_types=[".pdf", ".docx"],
        visible=False,
        scale=1
    )
    
    resume_note = gr.Markdown(
        "💡 **Note:** Please ensure your resume is in PDF or DOCX format.",
        visible=False
    )
    
    def toggle_resume_upload(choice: str):
        show = choice == "Upload Resume"
        return [gr.update(visible=show), gr.update(visible=show)]
    
    resume_choice.change(
        toggle_resume_upload,
        inputs=[resume_choice],
        outputs=[resume_file,resume_note]
    )
    
    return {
        "choice": resume_choice,
        "file": resume_file
    }

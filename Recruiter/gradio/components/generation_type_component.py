"""Generation type component for the Gradio application."""

import gradio as gr
from typing import Dict, Any

def create_generation_type_component() -> Dict[str, Any]:
    """
    Create the component for selecting the generation type (e.g., Email, Cover Letter).
    
    Returns:
        Dictionary containing the component elements.
        The dictionary will have a key "generation_type" for the gr.Radio component.
    """
    generation_type_radio = gr.Radio(
        choices=["Email", "Cover Letter"],
        label="Select Generation Type",
        value="Email",
        interactive=True,
        info="Choose what you want to generate."
    )
    
    return {
        "generation_type": generation_type_radio
    }
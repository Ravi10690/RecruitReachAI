"""Output feedback component for content regeneration."""

import gradio as gr
from typing import Dict, Any

def create_output_feedback_component() -> Dict[str, Any]:
    """
    Create the output feedback component with feedback input and regenerate button.
    
    Returns:
        Dictionary containing the component elements
    """
    gr.Markdown("### Feedback")
    feedback = gr.Textbox(
        label="Provide feedback for regeneration",
        placeholder="What would you like to change?"
    )
    regenerate_btn = gr.Button("🔄 Regenerate")
    
    return {
        "feedback": feedback,
        "regenerate_btn": regenerate_btn
    }

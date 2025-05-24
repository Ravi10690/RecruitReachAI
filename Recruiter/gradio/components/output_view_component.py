"""Output view component for displaying generated content."""

import gradio as gr
from typing import Dict, Any, Tuple

def create_output_view_component() -> Dict[str, Any]:
    """
    Create the output view component for displaying content in different formats.
    
    Returns:
        Dictionary containing the component elements
    """
    with gr.Column(scale=3) as view_column:
        output_html = gr.HTML(label="Preview")
        output_text = gr.Textbox(
            label="Plain Text",
            lines=10,
            visible=False
        )
        view_mode = gr.Radio(
            choices=["Rich HTML", "Plain Text"],
            label="View as",
            value="Rich HTML"
        )
    
    def toggle_view_mode(mode: str) -> Tuple[gr.update, gr.update]:
        """Toggle between HTML and plain text view modes."""
        return (
            gr.update(visible=mode == "Rich HTML"),
            gr.update(visible=mode == "Plain Text")
        )
    
    view_mode.change(
        toggle_view_mode,
        inputs=[view_mode],
        outputs=[output_html, output_text]
    )
    
    return {
        "column": view_column,
        "html": output_html,
        "text": output_text,
        "view_mode": view_mode
    }

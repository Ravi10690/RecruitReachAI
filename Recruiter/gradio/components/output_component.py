"""Output component for displaying generated content."""

import gradio as gr
from typing import Dict, Any, Tuple

def create_output_component() -> Dict[str, Any]:
    """
    Create the output component for displaying generated content.
    
    Returns:
        Dictionary containing the component elements
    """
    # Generation Type at the top
    gr.Markdown("### Generation Type")
    generation_type = gr.Radio(
        choices=["Email", "Cover Letter"],
        label="Choose what to generate",
        value="Email",
        interactive=True
    )
    
    # Main output section
    with gr.Row() as output_row:
        # Output content column (2/3 width)
        with gr.Column(scale=2):
            gr.Markdown("### Generated Content")
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
        
        # Actions and Feedback column (1/3 width)
        with gr.Column(scale=1):
            # Actions section
            gr.Markdown("### Actions")
            with gr.Row():
                copy_btn = gr.Button("📋 Copy to Clipboard")
                send_btn = gr.Button("📤 Send Email", visible=False)
                download_btn = gr.Button("📥 Download", visible=False)
            
            # Feedback section
            gr.Markdown("### Feedback")
            feedback = gr.Textbox(
                label="Provide feedback for regeneration",
                placeholder="What would you like to change?",
                lines=3
            )
            regenerate_btn = gr.Button("🔄 Regenerate")
    
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
        "generation_type": generation_type,
        "view": {
            "html": output_html,
            "text": output_text,
            "mode": view_mode
        },
        "actions": {
            "copy_btn": copy_btn,
            "send_btn": send_btn,
            "download_btn": download_btn
        },
        "feedback": {
            "feedback": feedback,
            "regenerate_btn": regenerate_btn
        }
    }

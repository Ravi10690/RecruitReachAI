"""Component for viewing generated email or cover letter content."""

import gradio as gr
from typing import Dict, Any, Tuple

def create_content_view_component() -> Dict[str, Any]:
    """
    Create a component for viewing generated content with rich formatting and actions.
    
    Returns:
        Dictionary containing the component elements
    """
    with gr.Column() as content_column:
        # Generation Type selector at top
        gr.Markdown("### 📝 Content Type")
        generation_type = gr.Radio(
            choices=["Email", "Cover Letter"],
            label="Choose what to generate",
            value="Email",
            interactive=True
        )
        
        # Content preview section
        with gr.Row():
            # Main content area (2/3 width)
            with gr.Column(scale=2):
                gr.Markdown("### Preview")
                with gr.Group():
                    # Subject line for emails
                    subject_html = gr.HTML(visible=True)
                    # Main content
                    content_html = gr.HTML()
                    content_text = gr.Textbox(
                        label="Plain Text",
                        lines=15,
                        visible=False
                    )
                
                # View mode toggle
                view_mode = gr.Radio(
                    choices=["Rich HTML", "Plain Text"],
                    label="View as",
                    value="Rich HTML",
                    interactive=True
                )
            
            # Actions sidebar (1/3 width)
            with gr.Column(scale=1):
                gr.Markdown("### Actions")
                with gr.Column():
                    copy_btn = gr.Button("📋 Copy to Clipboard", size="sm")
                    send_btn = gr.Button("📤 Send Email", size="sm", visible=False)
                    download_btn = gr.Button("📥 Download", size="sm", visible=False)
                
                gr.Markdown("### Feedback")
                feedback = gr.Textbox(
                    label="What would you like to change?",
                    placeholder="Provide feedback for regeneration...",
                    lines=3
                )
                regenerate_btn = gr.Button("🔄 Regenerate", size="sm")
    
    def toggle_view_mode(mode: str) -> Tuple[gr.update, gr.update]:
        """Toggle between HTML and plain text view modes."""
        return (
            gr.update(visible=mode == "Rich HTML"),
            gr.update(visible=mode == "Plain Text")
        )
    
    def toggle_email_mode(type: str) -> gr.update:
        """Toggle email-specific elements based on generation type."""
        return gr.update(visible=type == "Email")
    
    # Set up view mode toggle
    view_mode.change(
        toggle_view_mode,
        inputs=[view_mode],
        outputs=[content_html, content_text]
    )
    
    # Set up generation type toggle
    generation_type.change(
        toggle_email_mode,
        inputs=[generation_type],
        outputs=[subject_html]
    )
    
    return {
        "column": content_column,
        "generation_type": generation_type,
        "view": {
            "subject": subject_html,
            "content_html": content_html,
            "content_text": content_text,
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

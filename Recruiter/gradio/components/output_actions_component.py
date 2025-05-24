"""Output actions component for content operations."""

import gradio as gr
from typing import Dict, Any, Tuple

def create_output_actions_component() -> Dict[str, Any]:
    """
    Create the output actions component with copy, send, and download buttons.
    
    Returns:
        Dictionary containing the component elements
    """
    gr.Markdown("### Actions")
    copy_btn = gr.Button("📋 Copy to Clipboard")
    send_btn = gr.Button("📤 Send Email", visible=False)
    download_btn = gr.Button("📥 Download", visible=False)
    
    return {
        "copy_btn": copy_btn,
        "send_btn": send_btn,
        "download_btn": download_btn
    }

def setup_download_handler(
    components: Dict[str, Any],
    view_components: Dict[str, Any]
) -> None:
    """
    Set up the download button handler.
    
    Args:
        components: Dictionary containing action components
        view_components: Dictionary containing view components for content access
    """
    def download_content(text: str, html: str, view_mode: str) -> Tuple[str, str]:
        """Prepare content for download based on view mode."""
        content = html if view_mode == "Rich HTML" else text
        extension = "html" if view_mode == "Rich HTML" else "txt"
        return content, f"content.{extension}"
    
    components["download_btn"].click(
        download_content,
        inputs=[
            view_components["text"],
            view_components["html"],
            view_components["view_mode"]
        ],
        outputs=[gr.File(label="Download")]
    )

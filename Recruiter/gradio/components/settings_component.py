"""Settings component for the Gradio application."""

import gradio as gr
from Recruiter.gradio.utils.config_loader import get_config_values

def create_settings_component() -> dict:
    """
    Create the settings component with API key and email configuration.
    
    Returns:
        Dictionary containing the component elements
    """
    config = get_config_values()
    
    with gr.Accordion("⚙️ Settings", open=False) as settings_accordion:
        api_key = gr.Textbox(
            label="OpenAI API Key",
            value=config['openai_api_key'],
            type="password"
        )
        with gr.Row():
            sender_email = gr.Textbox(
                label="Sender Email",
                value=config['sender_email']
            )
            sender_name = gr.Textbox(
                label="Sender Name",
                value=config['sender_name']
            )
            app_password = gr.Textbox(
                label="Email App Password",
                value=config['app_password'],
                type="password"
            )
    
    return {
        "accordion": settings_accordion,
        "api_key": api_key,
        "sender_email": sender_email,
        "sender_name": sender_name,
        "app_password": app_password
    }

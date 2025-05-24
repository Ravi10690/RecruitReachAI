"""Main Gradio application for RecruitReach AI with Generation Type (Email or Cover Letter)."""

import gradio as gr
import asyncio
import time
from typing import Dict, Any, Optional

from Recruiter.gradio.components.settings_component import create_settings_component
from Recruiter.gradio.components.resume_component import create_resume_component
from Recruiter.gradio.components.job_description_component import create_job_description_component
from Recruiter.gradio.components.company_details_component import create_company_details_component, setup_extract_handler
from Recruiter.gradio.handlers.content_generator import generate_content
from Recruiter.gradio.handlers.email_handler import send_email as send_custom_email


CUSTOM_CSS = """
.input-section {
    min-height: 400px;
    display: flex;
    flex-direction: column;
    margin-bottom: 1rem;
}

.input-section > div:not(.button-row) {
    flex: 1;
}

/* Left column styling */
.left-column {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

/* Ensure proper spacing between job description and output section */
.left-column .input-section {
    margin-bottom: 2rem;
}

.button-container {
    margin-bottom: 1rem;
    gap: 1rem;
}

.left-button, .right-button {
    width: 100% !important;
    white-space: nowrap !important;
    margin: 0 !important;
}

.job-description {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.job-description .tabs {
    flex: 1;
}

.job-description .textbox textarea {
    height: calc(100% - 40px);  /* Adjust for label height */
}

.output-section {
    margin-top: 2rem;
    padding: 1rem;
    border-radius: 8px;
    background-color: white !important; 
    border: none !important;
}

.output-controls-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.5rem;
}

.view-mode-radio .label-wrap { 
   margin-bottom: 0 !important; 
}

.send-email-button {
    min-width: 150px; 
}

.email-status-success {
    color: green;
    font-weight: bold;
    padding: 0.5rem;
    border: 1px solid green;
    border-radius: 4px;
    margin-top: 0.5rem;
    background-color: #e6ffe6;
}

.email-status-error {
    color: red;
    font-weight: bold;
    padding: 0.5rem;
    border: 1px solid red;
    border-radius: 4px;
    margin-top: 0.5rem;
    background-color: #ffe6e6;
}

.output-view {
    margin-top: 1rem;
    padding: 1rem;
    border-radius: 8px;
    min-height: 300px;
    font-family: Arial, sans-serif;
    line-height: 1.6;
    background-color: white !important;
    color: black !important;
    border: none !important;
}

.output-section .label-wrap > span {
    background-color: white !important;
    color: black !important;
    font-weight: bold !important;
    font-size: 1.1em !important;
    margin-bottom: 10px !important;
    display: block !important;
}

#plain-text-output textarea { 
    background-color: white !important;
    color: black !important;
    border-radius: 5px !important;
    padding: 10px !important;
    font-family: monospace !important;
    font-size: 14px !important;
    border: 1px solid #e0e0e0 !important; 
}

.progress-section {
    margin-top: 1rem;
    padding: 1rem;
    border-radius: 8px;
    background: #f0f8ff;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading-spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-right: 10px;
    vertical-align: middle;
}

.email-content {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    max-width: 800px;
    margin: 0 auto;
    color: black !important; 
    background-color: white !important; 
}

.email-subject {
    font-weight: bold;
    margin-bottom: 20px;
    padding: 10px;
    border-radius: 5px;
    color: black !important; 
    background-color: #f5f5f5 !important; 
}

.email-body {
    color: black !important; 
    background-color: white !important; 
}

.email-body h1 {
    color: #2980b9 !important; 
    font-size: 24px;
    margin-bottom: 20px;
    font-weight: bold;
}

.email-body p {
    margin-bottom: 1em;
    font-size: 16px;
    color: black !important; 
}

.email-signature {
    margin-top: 2em;
    color: black !important; 
}

.output-view *, .output-section * {
    color: black !important;  
    background-color: transparent !important; 
}

.output-view {
    background-color: white !important; 
}

#plain-text-output textarea {
    background-color: white !important; 
    color: black !important;
}

.output-view h1, .output-view h2, .output-view h3 {
    color: #2980b9 !important;  
    background-color: transparent !important;
}

.output-view a {
    color: #2980b9 !important;  
    background-color: transparent !important;
}

.output-view .button { 
    color: white !important;
    padding: 10px 20px;
    border-radius: 5px;
    display: inline-block;
    text-decoration: none;
    font-weight: bold;
    margin-top: 20px;
}
"""

def create_ui() -> gr.Blocks:
    with gr.Blocks(title="RecruitReach AI", css=CUSTOM_CSS) as app:
        gr.Markdown("# 📧 RecruitReach AI")
        gr.Markdown("Generate personalized emails and cover letters using AI with feedback.")

        # Settings
        settings = create_settings_component()

        # Generation Type Selection
        generation_type = gr.Radio(
            choices=["Email", "Cover Letter"],
            label="Generation Type",
            value="Email",
            visible=True
        )

        # Application states
        generated_email_subject_state = gr.State("")
        generated_email_html_state = gr.State("")
        generated_email_text_state = gr.State("")

        # Layout: Left (Job Desc), Right (Resume & Company)
        with gr.Row():
            with gr.Column(scale=1, elem_classes="input-section"):
                with gr.Column(elem_classes="job-description"):
                    job_desc = create_job_description_component()
            with gr.Column(scale=1, elem_classes="input-section"):
                resume = create_resume_component()
                company_details = create_company_details_component()

        # Buttons at the top
        with gr.Row(elem_classes="button-container"):
            with gr.Column(scale=1):
                extract_btn = gr.Button("🔍 Extract Details", variant="primary", size="md", elem_classes="left-button")
            with gr.Column(scale=1):
                generate_btn = gr.Button("✨ Generate", variant="primary", size="md", elem_classes="right-button")

        # Setup job extraction 
        setup_extract_handler(
            {
                "extract_btn": extract_btn,
                "company_name": company_details["company_name"],
                "recruiter_email": company_details["recruiter_email"],
                "job_position": company_details["job_position"],
                "job_source": company_details["job_source"]
            },
            settings["api_key"],
            job_desc["job_desc"]
        )

        with gr.Row():
            with gr.Column(scale=3, visible=False) as output_section:
                with gr.Row():
                    view_mode = gr.Radio(
                        choices=["Rendered HTML", "Plain Text"],
                        label="View Mode",
                        value="Rendered HTML"
                    )
                email_status_md = gr.Markdown(visible=False)
                with gr.Column(elem_classes="output-view"):
                    html_view = gr.HTML()
                    text_view = gr.Textbox(
                        label=None, 
                        lines=15,
                        visible=False,
                        elem_id="plain-text-output"
                    )
            with gr.Column(scale=1):
                # Send Email button
                send_email_btn = gr.Button(
                    "📧 Send Email",
                    variant="secondary",
                    elem_classes="send-email-button",
                    visible=False  # hidden until content is generated
                )
                # Feedback input
                feedback_tb = gr.Textbox(
                    label="Feedback for next generation",
                    lines=2,
                    visible=False
                )
                # Re-generate button
                re_gen_btn = gr.Button(
                    "Re-Generate with Feedback",
                    variant="secondary",
                    elem_classes="right-button",
                    visible=False  # hidden until content is generated
                )

        # Switch rendering mode
        def update_view_mode(mode: str) -> Dict[str, Any]:
            return {
                html_view: gr.update(visible=(mode == "Rendered HTML")),
                text_view: gr.update(visible=(mode == "Plain Text"))
            }

        view_mode.change(update_view_mode, inputs=[view_mode], outputs=[html_view, text_view])

        # Generation logic
        def generate_output(
            api_key: str, 
            job_desc_val: str, 
            company_name_val: str, 
            job_position_val: str,
            resume_choice_val: str, 
            resume_file_val: Any, 
            recruiter_email_val: str, 
            job_source_val: str,
            feedback_val: str = None,
            generation_type_val: str = "Email"
        ):
            """Generate either Email or Cover Letter content, optionally with feedback."""
            try:
                content = generate_content(
                    api_key=api_key,
                    generation_type=generation_type_val,  # "Email" or "Cover Letter"
                    job_desc=job_desc_val,
                    company_name=company_name_val,
                    job_position=job_position_val,
                    resume_choice=resume_choice_val,
                    resume_file=resume_file_val,
                    recruiter_email=recruiter_email_val,
                    job_source=job_source_val,
                    feedback=feedback_val
                )
                html_content_display = f"""
                <div class="email-content">
                    <div class="email-subject">
                        <strong>Subject:</strong> {content['subject']}
                    </div>
                    <div class="email-body">
                        {content['html']}
                    </div>
                </div>
                """
                return {
                    output_section: gr.update(visible=True),
                    html_view: html_content_display,
                    text_view: content['text'],
                    generated_email_subject_state: content['subject'],
                    generated_email_html_state: content['html'],
                    generated_email_text_state: content['text'],
                    email_status_md: gr.update(visible=False, value=""),
                    send_email_btn: gr.update(visible=True),
                    feedback_tb: gr.update(visible=True),
                    re_gen_btn: gr.update(visible=True)
                }
            except Exception as e:
                return {
                    output_section: gr.update(visible=True),
                    html_view: f"<p style='color: red'>Error generating content: {str(e)}</p>",
                    text_view: f"Error: {str(e)}",
                    generated_email_subject_state: "",
                    generated_email_html_state: "",
                    generated_email_text_state: "",
                    email_status_md: gr.update(
                        visible=True, 
                        value=f"<p class='email-status-error'>Error: {str(e)}</p>"
                    ),
                    send_email_btn: gr.update(visible=False),
                    feedback_tb: gr.update(visible=False),
                    re_gen_btn: gr.update(visible=False)
                }

        # Generate (no feedback)
        generate_btn.click(
            generate_output,
            inputs=[
                settings["api_key"],
                job_desc["job_desc"],
                company_details["company_name"],
                company_details["job_position"],
                resume["choice"],
                resume["file"],
                company_details["recruiter_email"],
                company_details["job_source"],
                # no feedback
                generation_type
            ],
            outputs=[
                output_section, 
                html_view, 
                text_view,
                generated_email_subject_state, 
                generated_email_html_state,
                generated_email_text_state, 
                email_status_md,
                send_email_btn,
                feedback_tb,
                re_gen_btn
            ],
            show_progress=True
        )

        # Re-generate with feedback
        re_gen_btn.click(
            generate_output,
            inputs=[
                settings["api_key"],
                job_desc["job_desc"],
                company_details["company_name"],
                company_details["job_position"],
                resume["choice"],
                resume["file"],
                company_details["recruiter_email"],
                company_details["job_source"],
                feedback_tb,
                generation_type
            ],
            outputs=[
                output_section, 
                html_view, 
                text_view,
                generated_email_subject_state, 
                generated_email_html_state,
                generated_email_text_state, 
                email_status_md,
                send_email_btn,
                feedback_tb,
                re_gen_btn
            ],
            show_progress=True
        )

        # Send email
        def handle_send_email_action(
            api_key_val, sender_email_val, sender_name_val, app_password_val,
            recipient_email_val, subject_val, html_body_val, text_body_val,
            resume_choice_val, resume_file_val
        ):
            if not recipient_email_val:
                status_message = "❌ Error: Recipient email is missing. Please enter it in the 'Company Details' section."
                return gr.update(value=f"<p class='email-status-error'>{status_message}</p>", visible=True)
            if not subject_val or not (html_body_val or text_body_val):
                status_message = "❌ Error: Email subject or body is missing. Please generate content first."
                return gr.update(value=f"<p class='email-status-error'>{status_message}</p>", visible=True)
            if not all([sender_email_val, sender_name_val, app_password_val]):
                status_message = "❌ Error: Email settings are incomplete. Please configure them in settings."
                return gr.update(value=f"<p class='email-status-error'>{status_message}</p>", visible=True)

            try:
                effective_body = html_body_val if html_body_val else text_body_val
                send_custom_email(
                    sender_email=sender_email_val,
                    sender_name=sender_name_val,
                    app_password=app_password_val,
                    receiver_email=recipient_email_val,
                    subject=subject_val,
                    html_body=effective_body,
                    resume_choice=resume_choice_val,
                    resume_file=resume_file_val
                )
                status_message = f"✅ Email successfully sent to {recipient_email_val}!"
                return gr.update(value=f"<p class='email-status-success'>{status_message}</p>", visible=True)
            except Exception as e:
                status_message = f"❌ Error sending email: {str(e)}"
                return gr.update(value=f"<p class='email-status-error'>{status_message}</p>", visible=True)

        send_email_btn.click(
            handle_send_email_action,
            inputs=[
                settings["api_key"],
                settings["sender_email"],
                settings["sender_name"],
                settings["app_password"],
                company_details["recruiter_email"],
                generated_email_subject_state,
                generated_email_html_state,
                generated_email_text_state,
                resume["choice"],
                resume["file"]
            ],
            outputs=[email_status_md]
        )

    return app


def main():
    """Main function to launch the Gradio app."""
    app = create_ui()
    app.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=True
    )


if __name__ == "__main__":
    main()

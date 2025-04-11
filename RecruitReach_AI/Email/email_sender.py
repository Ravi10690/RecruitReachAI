from RecruitReach_AI.utils.toml_parser import TomlParser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr
import os
from typing import Union, Optional
from io import BytesIO

class EmailSender:
    def __init__(self):
        """Initialize EmailSender with configuration from TOML."""
        self.parser = TomlParser()
        self.smtp_server = self.parser.get_value("email", "smtp_server")
        self.smtp_port = self.parser.get_value("email", "smtp_port")
        self.sender_email = self.parser.get_value("email", "sender_email")
        self.sender_name = self.parser.get_value("email", "sender_name")
        self.app_password = self.parser.get_value("email", "app_password")

    def send_email(
        self,
        receiver_email: str,
        html_body: str,
        pdf_content: Union[str, bytes, BytesIO, None] = None,
        subject: Optional[str] = None,
        pdf_filename: Optional[str] = None,
        sender_email: Optional[str] = None,
        app_password: Optional[str] = None
    ) -> bool:
        """
        Send an email with HTML content and optional PDF attachment.
        
        Args:
            receiver_email (str): Recipient's email address
            html_body (str): HTML content for email body
            pdf_content (Union[str, bytes, BytesIO, None]): PDF content as file path, bytes, or BytesIO
            subject (str, optional): Email subject (falls back to config default)
            pdf_filename (str, optional): Name for the PDF attachment
            sender_email (str, optional): Sender's email (falls back to config)
            app_password (str, optional): App password (falls back to config)
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Use provided values or fall back to config
            sender = sender_email or self.sender_email
            password = app_password or self.app_password
            email_subject = subject
            sender_name = self.sender_name
            print(sender,password,email_subject,sender_name)
            if not all([sender, password, receiver_email]):
                print("⚠️ Missing required email credentials")
                return False

            # Create email object
            message = MIMEMultipart()
            message["From"] = formataddr((sender_name,sender))
            message["To"] = receiver_email
            message["Subject"] = email_subject

            # Attach HTML content
            html_part = MIMEText(html_body, "html")
            message.attach(html_part)

            # Handle PDF attachment
            if pdf_content is not None:
                try:
                    if isinstance(pdf_content, str):  # File path
                        if os.path.exists(pdf_content):
                            with open(pdf_content, "rb") as file:
                                pdf_bytes = file.read()
                        else:
                            print(f"⚠️ PDF file not found: {pdf_content}")
                            return False
                    elif isinstance(pdf_content, (bytes, BytesIO)):  # Bytes or BytesIO
                        pdf_bytes = pdf_content.read() if isinstance(pdf_content, BytesIO) else pdf_content
                    else:
                        print(f"⚠️ Unsupported PDF content type: {type(pdf_content)}")
                        return False

                    pdf_part = MIMEApplication(pdf_bytes, _subtype="pdf")
                    attachment_filename = pdf_filename or (
                        os.path.basename(pdf_content) if isinstance(pdf_content, str) else "attachment.pdf"
                    )
                    pdf_part.add_header("Content-Disposition", f"attachment; filename={attachment_filename}")
                    message.attach(pdf_part)

                except Exception as e:
                    print(f"⚠️ Failed to attach PDF: {e}")
                    return False

            # Send email using SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(sender, password)
                server.sendmail(sender, receiver_email, message.as_string())
                print("✅ Email sent successfully!")
                return True

        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False

# Example usage
if __name__ == "__main__":
    # Example HTML body
    sample_html = """
    <html>
      <body>
        <h2 style="color:#2e6c80;">Hello from RecruitReach AI!</h2>
        <p>This is a sample email with <b>HTML formatting</b> and an attached PDF file.</p>
      </body>
    </html>
    """

    # Create EmailSender instance
    email_sender = EmailSender()

    # Example with file path
    success = email_sender.send_email(
        receiver_email="extraitem123@gmail.com",
        html_body=sample_html,
        pdf_content=r"RecruitReach_AI/data/Ravi_Ahuja_Resume.pdf",
        subject="yes"
    )

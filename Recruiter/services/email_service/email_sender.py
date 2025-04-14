"""
Email Sender Service for RecruitReach2.

This module provides a service for sending emails with HTML content and attachments.
"""

import os
import smtplib
from io import BytesIO
from typing import Union, Optional, Dict, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr

from Recruiter.models.schemas import EmailConfig
from Recruiter.utils.config.config_manager import ConfigManager


class EmailSenderService:
    """
    Service for sending emails with HTML content and attachments.
    
    This class provides methods for sending emails with HTML content and
    optional attachments such as PDF files.
    """
    
    def __init__(
        self,
        sender_email: Optional[str] = None,
        sender_name: Optional[str] = None,
        app_password: Optional[str] = None,
        smtp_server: str = "smtp.gmail.com",
        smtp_port: int = 587
    ):
        """
        Initialize the email sender service.
        
        Args:
            sender_email: Sender's email address. If not provided, will try to get from config.
            sender_name: Sender's name. If not provided, will try to get from config.
            app_password: App password for email authentication. If not provided, will try to get from config.
            smtp_server: SMTP server address.
            smtp_port: SMTP server port.
        """
        # Get email config from config file if not provided
        if not all([sender_email, sender_name, app_password]):
            config_manager = ConfigManager()
            email_config = config_manager.get_app_config().email
            
            if email_config:
                sender_email = sender_email or email_config.sender_email
                sender_name = sender_name or email_config.sender_name
                app_password = app_password or email_config.app_password
                smtp_server = smtp_server or email_config.smtp_server
                smtp_port = smtp_port or email_config.smtp_port
        
        self.sender_email = sender_email
        self.sender_name = sender_name
        self.app_password = app_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def send_email(
        self,
        receiver_email: str,
        subject: str,
        html_body: str,
        attachment: Optional[Union[str, bytes, BytesIO]] = None,
        attachment_filename: Optional[str] = None,
        attachment_type: str = "application/pdf"
    ) -> bool:
        """
        Send an email with HTML content and optional attachment.
        
        Args:
            receiver_email: Recipient's email address.
            subject: Email subject.
            html_body: HTML content for email body.
            attachment: Optional attachment as file path, bytes, or BytesIO.
            attachment_filename: Name for the attachment file.
            attachment_type: MIME type of the attachment.
            
        Returns:
            True if email sent successfully, False otherwise.
        """
        try:
            # Validate required parameters
            if not all([self.sender_email, self.sender_name, self.app_password, receiver_email, subject, html_body]):
                print("Missing required email parameters")
                return False
            
            # Create email message
            message = MIMEMultipart()
            message["From"] = formataddr((self.sender_name, self.sender_email))
            message["To"] = receiver_email
            message["Subject"] = subject
            
            # Attach HTML content
            html_part = MIMEText(html_body, "html")
            message.attach(html_part)
            
            # Handle attachment if provided
            if attachment:
                try:
                    # Get attachment content based on type
                    if isinstance(attachment, str):  # File path
                        if os.path.exists(attachment):
                            with open(attachment, "rb") as file:
                                attachment_content = file.read()
                        else:
                            print(f"Attachment file not found: {attachment}")
                            return False
                    elif isinstance(attachment, BytesIO):  # BytesIO
                        attachment_content = attachment.read()
                    else:  # Bytes
                        attachment_content = attachment
                    
                    # Determine attachment filename
                    if not attachment_filename:
                        if isinstance(attachment, str):
                            attachment_filename = os.path.basename(attachment)
                        else:
                            attachment_filename = "attachment.pdf"
                    
                    # Create attachment part
                    attachment_part = MIMEApplication(attachment_content, _subtype=attachment_type.split('/')[-1])
                    attachment_part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={attachment_filename}"
                    )
                    message.attach(attachment_part)
                
                except Exception as e:
                    print(f"Failed to attach file: {str(e)}")
                    return False
            
            # Send email using SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.app_password)
                server.sendmail(self.sender_email, receiver_email, message.as_string())
                print("Email sent successfully!")
                return True
        
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
    
    @classmethod
    def from_config(cls) -> 'EmailSenderService':
        """
        Create an EmailSenderService instance from configuration.
        
        Returns:
            EmailSenderService instance initialized with configuration values.
        """
        config_manager = ConfigManager()
        email_config = config_manager.get_app_config().email
        if not email_config:
            raise ValueError("Email configuration not found")
        
        return cls(
            sender_email=email_config.sender_email,
            sender_name=email_config.sender_name,
            app_password=email_config.app_password,
            smtp_server=email_config.smtp_server,
            smtp_port=email_config.smtp_port
        )

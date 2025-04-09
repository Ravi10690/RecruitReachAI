import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Sender and receiver details
sender_email = "raviahuja1998@gmail.com"
receiver_email = "extraitem123@gmail.com"
app_password = "jbgf apkq svcb knhw"  # Use the app password from Gmail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

# --- Email Configuration ---
subject = "Email with HTML Content and PDF Attachment"

# --- HTML Body Content ---
html_body = """
<html>
  <body>
    <h2 style="color:#2e6c80;">Hello from Python!</h2>
    <p>This email contains <b>HTML formatting</b> and an attached PDF file.</p>
  </body>
</html>
"""

# --- Create Email Object ---
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Attach HTML content
html_part = MIMEText(html_body, "html")
message.attach(html_part)

# --- Attach PDF File ---
pdf_path = r"C:\Users\ravia\OneDrive\Documents\Resume\Ravi_Ahuja_Resume.pdf"  # Replace with your PDF filename
if os.path.exists(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_part = MIMEApplication(file.read(), _subtype="pdf")
        pdf_part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(pdf_path)}"
        )
        message.attach(pdf_part)
else:
    print(f"⚠️ PDF file not found: {pdf_path}")

# --- Send Email using Gmail SMTP ---
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Start TLS encryption
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("✅ Email sent successfully with HTML content and PDF attachment!")
except Exception as e:
    print(f"❌ Failed to send email: {e}")

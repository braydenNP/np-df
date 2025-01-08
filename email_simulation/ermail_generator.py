import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
import random

# SMTP server configuration
SMTP_SERVER = "localhost"
SMTP_PORT = 1025

# Email metadata
employees = ["rachel.simmons@evergreentrust.com", "michael.tan@evergreentrust.com", "alan.chow@evergreentrust.com"]
subject_pool = [
    "Critical Task: Disable Logging",
    "Suspicious Activity Detected",
    "Audit Report Review",
    "System Access Alert",
    "Confidential Financial Review"
]
body_templates = [
    """<html>
        <body>
            <p>{recipient_name},</p>
            <p>Ensure logging is disabled for Workstation-12. Do not involve Alan Chow in this.</p>
            <p>Regards,<br>Rachel</p>
        </body>
    </html>""",
    """<html>
        <body>
            <p>{recipient_name},</p>
            <p>I have detected unusual activity in Rachel Simmons' account logs. Please investigate.</p>
            <p>Regards,<br>Alan</p>
        </body>
    </html>""",
    """<html>
        <body>
            <p>{recipient_name},</p>
            <p>Review the attached document immediately and ensure compliance with audit procedures.</p>
            <p>Regards,<br>{sender_name}</p>
        </body>
    </html>"""
]

def generate_attachment():
    """Create a malicious PDF attachment."""
    filename = f"instructions_{random.randint(1000, 9999)}.pdf"
    with open(filename, "wb") as f:
        f.write(b"%PDF-1.4\n% Fake Audit Instructions with Embedded Exploit")
    print(f"[INFO] Malicious PDF {filename} created.")
    return filename

def send_email(sender, recipient, subject, body, attachment=None, spoof=False):
    """Send a phishing email with optional forged headers and attachments."""
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    # Attach HTML body
    msg.attach(MIMEText(body, 'html'))

    # Attach malicious file if provided
    if attachment:
        with open(attachment, "rb") as f:
            attachment_part = MIMEBase("application", "octet-stream")
            attachment_part.set_payload(f.read())
        encoders.encode_base64(attachment_part)
        attachment_part.add_header("Content-Disposition", f"attachment; filename={attachment}")
        msg.attach(attachment_part)

    # Spoof headers to implicate Alan Chow
    if spoof:
        msg.add_header("X-Originating-IP", "10.0.0.99")  # Fake IP
        msg.add_header("Reply-To", "alan.chow@evergreentrust.com")
    else:
        msg.add_header("X-Originating-IP", random.choice(["192.168.1.101", "10.0.0.54"]))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.sendmail(sender, recipient, msg.as_string())
        print(f"[INFO] Email sent from {sender} to {recipient}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

def generate_email_interactions():
    """Simulate multiple email interactions to generate evidence."""
    for _ in range(20):  # Generate 20 email interactions
        sender = random.choice(employees)
        recipient = random.choice([emp for emp in employees if emp != sender])
        subject = random.choice(subject_pool)
        body_template = random.choice(body_templates)
        body = body_template.format(
            recipient_name=recipient.split('@')[0].capitalize(),
            sender_name=sender.split('@')[0].capitalize()
        )

        # Randomly decide if the email has an attachment or is spoofed
        attachment = generate_attachment() if random.choice([True, False]) else None
        spoof = random.choice([True, False])

        send_email(sender, recipient, subject, body, attachment=attachment, spoof=spoof)

if __name__ == "__main__":
    print("[INFO] Starting phishing email simulation...")
    generate_email_interactions()
    print("[INFO] Phishing email simulation completed.")

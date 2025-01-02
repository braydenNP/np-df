"""
1. Creates a fake PDF (instructions_hidden.pdf) containing embedded exploit code.

2. Sending Phishing Emails
    - Email 1: From Rachel Simmons to Michael Tan, instructing him to disable security logging.
    - Email 2: A spoofed email, sent from Alan Chow's account to Michael Tan, raising suspicion about Rachel Simmons.

3. Adds forged headers to implicate Alan Chow and mislead investigators.

Relation to the Attack Scenario:
    - Mimics Rachel Simmons collaborating with Michael Tan to disable critical security features.
    - Creates misleading evidence pointing to Alan Chow, adding complexity to the forensic investigation.
    - Leaves behind the malicious PDF, which investigators can analyze to uncover its purpose.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
import random

def generate_attachment():
    """Create a malicious PDF attachment."""
    with open("instructions_hidden.pdf", "wb") as f:
        f.write(b"%PDF-1.4\n% Fake Audit Instructions with Embedded Exploit")
    print("[INFO] Malicious PDF created.")

def send_email(sender, recipient, subject, body, spoof=False):
    """Send a phishing email with forged headers."""
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    # Attach HTML body
    msg.attach(MIMEText(body, 'html'))

    # Attach malicious file
    generate_attachment()
    filename = "instructions_hidden.pdf"
    with open(filename, "rb") as f:
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(f.read())
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", f"attachment; filename={filename}")
    msg.attach(attachment)

    # Spoof headers to implicate Alan Chow
    if spoof:
        msg.add_header("X-Originating-IP", "10.0.0.99")  # Fake IP
        msg.add_header("Reply-To", "alan.chow@evergreentrust.com")
    else:
        msg.add_header("X-Originating-IP", random.choice(["192.168.1.101", "10.0.0.54"]))

    try:
        with smtplib.SMTP("localhost", 1025) as server:
            server.sendmail(sender, recipient, msg.as_string())
        print(f"[INFO] Email sent from {sender} to {recipient}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

if __name__ == "__main__":
    send_email(
        "rachel.simmons@evergreentrust.com",
        "michael.tan@evergreentrust.com",
        "Critical Task: Disable Logging",
        f"""<html>
            <body>
                <p>Michael,</p>
                <p>Ensure logging is disabled for Workstation-12. Do not involve Alan Chow in this.</p>
                <p>Regards,<br>Rachel</p>
            </body>
        </html>""",
    )
    send_email(
        "alan.chow@evergreentrust.com",
        "michael.tan@evergreentrust.com",
        "Suspicious Email Alert",
        f"""<html>
            <body>
                <p>Michael,</p>
                <p>I have detected unusual activity in Rachel Simmons' account logs. Please investigate.</p>
            </body>
        </html>""",
        spoof=True,
    )

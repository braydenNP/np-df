import re

# File path
input_file = "mbox"  

# List of authorized emails
authorized_emails = [
    "alison@m57.biz",
    "jean@m57.biz",
    "bob@m57.biz",
    "carole@m57.biz",
    "david@m57.biz",
    "emmy@m57.biz",
    "gina@m57.biz",
    "harris@m57.biz",
    "indy@m57.biz"
]

# Regex patterns for extracting email fields
from_pattern = re.compile(r'From:\s*(.*)', re.IGNORECASE)  # Extracts full "From:" field
email_extraction_pattern = re.compile(r'[\w\.-]+@[\w\.-]+')  # Extracts email addresses
date_pattern = re.compile(r'Date:\s*(.*)', re.IGNORECASE)  # Extracts Date header
message_id_pattern = re.compile(r'Message-Id:\s*<(.*?)>', re.IGNORECASE)
to_pattern = re.compile(r'To:\s*(.*)', re.IGNORECASE)
subject_pattern = re.compile(r'Subject:\s*(.*)', re.IGNORECASE)
boundary_pattern = re.compile(r'----boundary.*?')

# New pattern to extract date from "From " line
from_line_date_pattern = re.compile(r'From\s+".*?"\s+(\w{3}\s+\w{3}\s+\d+\s+\d+:\d+:\d+\s+\d{4})')

# List to store filtered emails
emails = []

# Open and process the file with error handling for encoding issues
try:
    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
except UnicodeDecodeError:
    print("[!] UTF-8 decoding failed, retrying with ISO-8859-1...")
    with open(input_file, "r", encoding="ISO-8859-1") as f:
        lines = f.readlines()

email_data = {}
message_body = []
inside_message = False
inside_attachment = False
current_sender_email = ""
current_date = ""
current_subject = ""
current_to = ""

for line in lines:
    line = line.strip()

    # Detect base64 encoded attachment, start ignoring content
    if "Content-Transfer-Encoding: base64" in line:
        inside_attachment = True
        continue
    if inside_attachment and line == "":
        inside_attachment = False
        continue
    if inside_attachment:
        continue  # Skip encoded attachments

    # Capture date from "From " line at the start of an email block
    if line.startswith("From "):
        # Store previous email if from an authorized sender
        if email_data and any(auth_email in current_sender_email for auth_email in authorized_emails):
            email_data["Body"] = "\n".join(message_body).strip()
            emails.append(email_data)

        # Reset for new email
        email_data = {}
        message_body = []
        inside_message = False
        current_sender_email = ""
        current_date = ""
        current_subject = ""
        current_to = ""

        # Extract potential date from "From " line
        date_match = from_line_date_pattern.search(line)
        if date_match:
            current_date = date_match.group(1)  # Store extracted date

    # Extract sender email (handles all variations of "From:" formatting)
    from_match = from_pattern.search(line)
    if from_match:
        full_from_field = from_match.group(1)
        found_emails = email_extraction_pattern.findall(full_from_field)  # Extract email(s)
        if found_emails:
            current_sender_email = found_emails[0].lower()  # Get the first detected email
            email_data["From"] = full_from_field  # Store raw "From:" field
        else:
            current_sender_email = ""

    # Extract fields
    to_match = to_pattern.search(line)
    subject_match = subject_pattern.search(line)
    msg_id_match = message_id_pattern.search(line)
    date_match = date_pattern.search(line)

    if to_match:
        current_to = to_match.group(1).strip()
    if subject_match:
        current_subject = subject_match.group(1).strip()
    if msg_id_match:
        email_data["Message ID"] = msg_id_match.group(1).strip()

    # Extract date from "Date:" header if found
    if date_match:
        current_date = date_match.group(1).strip()

    # Assign captured values before email is stored
    email_data["To"] = current_to
    email_data["Subject"] = current_subject
    email_data["Date"] = current_date

    # Start capturing message body after headers
    if line == "":
        inside_message = True
        continue

    # Ignore MIME boundaries, metadata, and headers
    if not inside_message or boundary_pattern.search(line):
        continue

    # Collect message body
    message_body.append(line)

# Append the last email if it is from an authorized sender
if email_data and any(auth_email in current_sender_email for auth_email in authorized_emails):
    email_data["Body"] = "\n".join(message_body).strip()
    emails.append(email_data)

# Debugging: Check what emails were detected
if not emails:
    print("[!] No relevant emails found.")
else:
    for i, email in enumerate(emails, start=1):
        print(f"\n{'='*80}")
        print(f"Email {i}")
        print(f"From: {email.get('From', 'Unknown')}")
        print(f"To: {email.get('To', 'Unknown')}")
        print(f"Subject: {email.get('Subject', 'No Subject')}")
        print(f"Date: {email.get('Date', 'Unknown')}")  # Date should now always be printed
        print(f"Message ID: {email.get('Message ID', 'Unknown')}")
        print(f"\n--- Message Body ---\n{email.get('Body', 'No Content')}")
        print(f"{'='*80}\n")

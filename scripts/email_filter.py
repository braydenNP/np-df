import re

# File path
input_file = "mbox"  

# Regex patterns for extracting email fields
email_pattern = re.compile(r'From:\s*"?(.*?)"?\s*<(.*?)>')
to_pattern = re.compile(r'To:\s*(.*?)')
subject_pattern = re.compile(r'Subject:\s*(.*?)')
date_pattern = re.compile(r'Date:\s*(.*?)')
message_id_pattern = re.compile(r'Message-Id:\s*<(.*?)>')
boundary_pattern = re.compile(r'----boundary.*?')

# List to store formatted emails
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

for line in lines:
    line = line.strip()

    # Check for email start
    if line.startswith("From "):
        if email_data:  # Store previous email before starting a new one
            email_data["Body"] = "\n".join(message_body).strip()
            emails.append(email_data)

        # Reset for new email
        email_data = {}
        message_body = []
        inside_message = False

    # Extract fields
    from_match = email_pattern.search(line)
    to_match = to_pattern.search(line)
    subject_match = subject_pattern.search(line)
    date_match = date_pattern.search(line)
    msg_id_match = message_id_pattern.search(line)

    if from_match:
        email_data["From Name"] = from_match.group(1)
        email_data["From Email"] = from_match.group(2)
    if to_match:
        email_data["To"] = to_match.group(1)
    if subject_match:
        email_data["Subject"] = subject_match.group(1)
    if date_match:
        email_data["Date"] = date_match.group(1)
    if msg_id_match:
        email_data["Message ID"] = msg_id_match.group(1)

    # Start capturing message body after headers
    if line == "":
        inside_message = True
        continue

    # Ignore MIME boundaries, metadata, and headers
    if not inside_message or boundary_pattern.search(line):
        continue

    # Collect message body
    message_body.append(line)

# Append the last email to the list
if email_data:
    email_data["Body"] = "\n".join(message_body).strip()
    emails.append(email_data)

# Print formatted emails
for i, email in enumerate(emails, start=1):
    print(f"\n{'='*80}")
    print(f"Email {i}")
    print(f"From: {email.get('From Name', 'Unknown')} <{email.get('From Email', 'Unknown')}>")
    print(f"To: {email.get('To', 'Unknown')}")
    print(f"Subject: {email.get('Subject', 'No Subject')}")
    print(f"Date: {email.get('Date', 'Unknown')}")
    print(f"Message ID: {email.get('Message ID', 'Unknown')}")
    print(f"\n--- Message Body ---\n{email.get('Body', 'No Content')}")
    print(f"{'='*80}\n")
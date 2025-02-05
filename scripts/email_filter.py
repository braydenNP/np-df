import mailbox

# Define the path to the mbox file.
mbox_path = "mbox"

# Open the specified mbox file in read mode.
mbox = mailbox.mbox(mbox_path)

# Process each message in the mbox, starting with the first message.
for i, message in enumerate(mbox, start=1):
    # Retrieve essential email headers, providing default values if any headers are missing.
    from_ = message.get('From', 'Unknown')
    to_ = message.get('To', 'Unknown')
    subj = message.get('Subject', 'No Subject')
    date_ = message.get('Date', 'Unknown')
    msg_id = message.get('Message-ID', 'Unknown')

    # Initialize a list to hold parts of the email body.
    body = []

    # Determine if the email message consists of multiple parts.
    if message.is_multipart():
        # Iterate through each part of the email message.
        for part in message.walk():
            # Identify the MIME content type of each part.
            ctype = part.get_content_type()
            # Retrieve content disposition to check for attachments.
            cdisp = str(part.get('Content-Disposition'))

            # Handle only text/plain parts and ignore attachments.
            if ctype == 'text/plain' and 'attachment' not in cdisp:
                # Retrieve the email body payload in raw bytes.
                payload_bytes = part.get_payload(decode=True)
                # Estimate the character set or default to UTF-8.
                charset = part.get_content_charset() or 'utf-8'
                
                try:
                    # Decode the payload using the identified or default character set.
                    text = payload_bytes.decode(charset, errors='replace')
                except:
                    # Handle potential decoding errors gracefully.
                    text = payload_bytes.decode('utf-8', errors='replace')

                # Append the decoded text to the body list.
                body.append(text)
    else:
        # Handle non-multipart emails which have a single payload.
        payload_bytes = message.get_payload(decode=True)
        if payload_bytes:
            # Estimate the character set or use UTF-8 as fallback.
            charset = message.get_content_charset() or 'utf-8'
            try:
                # Decode the single payload using the identified or default charset.
                text = payload_bytes.decode(charset, errors='replace')
            except:
                # Provide a fallback decoding strategy in case of charset issues.
                text = payload_bytes.decode('utf-8', errors='replace')
            body.append(text)

    # Concatenate all parts of the body into a single string and remove extra whitespace.
    full_body = "\n".join(body).strip()

    # Output formatting: Display a separator line for clarity.
    print("=" * 80)
    # Output essential email metadata and the body.
    print(f"Email {i}")
    print(f"From: {from_}")
    print(f"To: {to_}")
    print(f"Subject: {subj}")
    print(f"Date: {date_}")
    print(f"Message ID: {msg_id}")
    print("\n--- Message Body ---")
    print(full_body)
    print("=" * 80)
    print()
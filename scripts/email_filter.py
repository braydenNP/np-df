import mailbox

# Path to your mbox file
mbox_path = "mbox"

# Open the mbox file for reading
mbox = mailbox.mbox(mbox_path)

# Iterate through each message in the mbox, numbering them from 1 upwards
for i, message in enumerate(mbox, start=1):
    # Retrieve header fields with sensible fallbacks if they don't exist
    from_ = message.get('From', 'Unknown')
    to_ = message.get('To', 'Unknown')
    subj = message.get('Subject', 'No Subject')
    date_ = message.get('Date', 'Unknown')
    msg_id = message.get('Message-ID', 'Unknown')

    # Initialize a list to collect the text body (may be multiple parts if multipart)
    body = []

    # Check if the message is multipart (contains multiple parts)
    if message.is_multipart():
        # Walk over each part of the multipart message
        for part in message.walk():
            # Get the MIME content type (e.g. text/plain, text/html, etc.)
            ctype = part.get_content_type()
            # Check the content disposition for "attachment" or inline
            cdisp = str(part.get('Content-Disposition'))
            
            # Only process text/plain parts that are not marked as an attachment
            if ctype == 'text/plain' and 'attachment' not in cdisp:
                # Decode the payload to raw bytes
                payload_bytes = part.get_payload(decode=True)
                
                # Determine the best guess for the character set; default to UTF-8 if unknown
                charset = part.get_content_charset() or 'utf-8'
                try:
                    # Decode the raw bytes into a string using the specified charset
                    text = payload_bytes.decode(charset, errors='replace')
                except:
                    # Fallback decoding in case the specified charset fails
                    text = payload_bytes.decode('utf-8', errors='replace')

                # Append the decoded text to our body list
                body.append(text)
    else:
        # For non-multipart messages, there's only a single payload
        payload_bytes = message.get_payload(decode=True)
        if payload_bytes:
            charset = message.get_content_charset() or 'utf-8'
            try:
                text = payload_bytes.decode(charset, errors='replace')
            except:
                text = payload_bytes.decode('utf-8', errors='replace')
            body.append(text)

    # Combine all body parts (if multiple) into one continuous string, trimmed of extra whitespace
    full_body = "\n".join(body).strip()

    # Print a separator for visual clarity
    print("=" * 80)
    # Print the message index and essential email header information
    print(f"Email {i}")
    print(f"From: {from_}")
    print(f"To: {to_}")
    print(f"Subject: {subj}")
    print(f"Date: {date_}")
    print(f"Message ID: {msg_id}")
    # Print the extracted plain text body
    print("\n--- Message Body ---")
    print(full_body)
    print("=" * 80)
    print()

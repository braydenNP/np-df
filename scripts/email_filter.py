import mailbox

# Path to your mbox file
mbox_path = "mbox"

# Open the mbox
mbox = mailbox.mbox(mbox_path)

for i, message in enumerate(mbox, start=1):
    # Extract some common fields:
    from_ = message.get('From', 'Unknown')
    to_ = message.get('To', 'Unknown')
    subj = message.get('Subject', 'No Subject')
    date_ = message.get('Date', 'Unknown')
    msg_id = message.get('Message-ID', 'Unknown')

    # Now let's get the plain-text message body.
    # Some messages are multipart, some are not.
    body = []

    if message.is_multipart():
        # If it's multipart, walk the parts to find text/plain
        for part in message.walk():
            ctype = part.get_content_type()  # e.g. 'text/plain', 'text/html', 'image/png' ...
            cdisp = str(part.get('Content-Disposition'))
            
            # We only want text/plain that isn't an attachment
            if ctype == 'text/plain' and 'attachment' not in cdisp:
                # Decode the payload into bytes, then decode to string
                payload_bytes = part.get_payload(decode=True)
                
                # Determine the character set. Fallback to utf-8
                charset = part.get_content_charset() or 'utf-8'
                try:
                    text = payload_bytes.decode(charset, errors='replace')
                except:
                    text = payload_bytes.decode('utf-8', errors='replace')

                body.append(text)
    else:
        # Not a multipart - just get the single payload
        payload_bytes = message.get_payload(decode=True)
        if payload_bytes:
            charset = message.get_content_charset() or 'utf-8'
            try:
                text = payload_bytes.decode(charset, errors='replace')
            except:
                text = payload_bytes.decode('utf-8', errors='replace')
            body.append(text)

    # Join all text/plain parts together
    full_body = "\n".join(body).strip()

    # (Optional) If any HTML snuck through in a text/html part, you could do an HTML strip:
    # import re
    # full_body = re.sub(r'<[^>]+>', '', full_body)

    print("=" * 80)
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

import imaplib
import email
from transformers import T5Tokenizer, T5ForConditionalGeneration
import os
import getpass

# Configuration
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
PORT = int(os.getenv("IMAP_PORT", 993))
MODEL_NAME = os.getenv("MODEL_NAME", "google/flan-t5-small")

# Load the summarization model
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

def fetch_emails(username, password, folder="inbox", max_emails=5):
    """Fetches the most recent emails from the IMAP server."""
    try:
        with imaplib.IMAP4_SSL(IMAP_SERVER, PORT) as mail:
            mail.login(username, password)
            mail.select(folder)

            # Search for all emails
            result, data = mail.search(None, "ALL")
            if result != "OK":
                print("Failed to search emails.")
                return []

            email_ids = data[0].split()[-max_emails:][::-1]  # Get latest emails in reverse order

            emails = []
            for eid in email_ids:
                result, data = mail.fetch(eid, "(RFC822)")
                if result != "OK":
                    print(f"Failed to fetch email ID {eid.decode()}.")
                    continue

                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                emails.append(msg)
            return emails
    except imaplib.IMAP4.error as e:
        print(f"IMAP error: {e}")
    except Exception as e:
        print(f"Error fetching emails: {e}")
    return []

def extract_email_content(msg):
    """Extracts the plain text content from an email."""
    try:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    content = part.get_payload(decode=True)
                    if content:
                        return content.decode()
        else:
            content = msg.get_payload(decode=True)
            if content:
                return content.decode()
    except Exception as e:
        print(f"Error extracting content from email: {e}")
    return "Unable to extract content."

def summarize_email(content):
    """Summarizes email content using the Flan-T5 model."""
    try:
        input_text = f"summarize: {content}"
        inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(inputs, max_length=50, num_beams=5, early_stopping=True)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        print(f"Error summarizing content: {e}")
        return "Unable to generate summary."

def generate_digest(emails):
    """Generates a daily digest from the list of emails."""
    digest = "Daily Email Digest\n\n"
    for i, msg in enumerate(emails):
        subject = msg["subject"] or "No Subject"
        content = extract_email_content(msg)
        if not content.strip():
            content = "No content available."
        summary = summarize_email(content)
        digest += f"Email {i+1}:\nSubject: {subject}\nSummary: {summary}\n\n"
    return digest

def save_digest(digest, file_name="daily_digest.txt"):
    """Saves the digest to a text file."""
    try:
        with open(file_name, "w") as f:
            f.write(digest)
        print(f"Digest saved to {file_name}")
    except Exception as e:
        print(f"Error saving digest: {e}")

def main():
    print("Welcome to the Automated Email Summarizer")
    username = input("Enter your email: ")
    password = getpass.getpass("Enter your password (input hidden): ")

    emails = fetch_emails(username, password)
    if not emails:
        print("No emails fetched.")
        return

    digest = generate_digest(emails)
    save_digest(digest)

if __name__ == "__main__":
    main()

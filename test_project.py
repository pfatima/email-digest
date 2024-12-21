import pytest
from unittest.mock import patch, MagicMock
from project import fetch_emails, extract_email_content, summarize_email, generate_digest

# Constants for testing
DUMMY_EMAIL = {
    "subject": "Test Subject",
    "content": "This is a test email content."
}

def mock_email():
    """Creates a mocked email object."""
    msg = MagicMock()
    msg.is_multipart.return_value = False
    msg.get_payload.return_value = DUMMY_EMAIL["content"].encode()
    msg.__getitem__.side_effect = lambda key: DUMMY_EMAIL[key]  # Mock subject retrieval
    return msg

@patch("imaplib.IMAP4_SSL")
def test_fetch_emails(mock_imap):
    """Tests the fetch_emails function by mocking IMAP server interaction."""
    # Mock IMAP server
    mock_mail = MagicMock()
    mock_mail.search.return_value = ("OK", [b"1 2 3"])  # Mock email IDs
    mock_mail.fetch.return_value = ("OK", [(b"1", b"Dummy email data")])  # Mock email fetch
    mock_imap.return_value.__enter__.return_value = mock_mail

    # Test the function
    emails = fetch_emails("user@example.com", "password")
    assert len(emails) == 3
    mock_mail.search.assert_called_once_with(None, "ALL")  # Verify search call
    assert mock_mail.fetch.call_count == 3  # Verify fetch call for each email

def test_extract_email_content():
    """Tests extraction of plain text email content."""
    # Mock email message
    msg = mock_email()

    # Test the function
    content = extract_email_content(msg)
    assert content == DUMMY_EMAIL["content"]

@patch("project.summarize_email", return_value="Summarized content.")
def test_generate_digest(mock_summarize_email):
    """Tests digest generation from emails."""
    # Mock emails
    emails = [mock_email() for _ in range(2)]

    # Test the function
    digest = generate_digest(emails)
    assert "Daily Email Digest" in digest
    assert "Test Subject" in digest
    assert "Summarized content." in digest

    # Verify the summarize_email call
    assert mock_summarize_email.call_count == 2

# @patch("project.T5ForConditionalGeneration")
# @patch("project.T5Tokenizer")
# def test_summarize_email(mock_tokenizer_class, mock_model_class):
#     """Tests email summarization."""
#     # Mock tokenizer and model instances
#     mock_tokenizer_instance = MagicMock()
#     mock_tokenizer_instance.encode.return_value = [0, 1, 2]
#     mock_tokenizer_instance.decode.return_value = "Summarized content."
#     mock_tokenizer_class.from_pretrained.return_value = mock_tokenizer_instance

#     mock_model_instance = MagicMock()
#     mock_model_instance.generate.return_value = [[0, 1, 2]]
#     mock_model_class.from_pretrained.return_value = mock_model_instance

#     # Test the function
#     summary = summarize_email("Email content")
#     assert summary == "Summarized content."

#     # Verify tokenizer and model calls
#     mock_tokenizer_instance.encode.assert_called_once_with(
#         "summarize: Email content", return_tensors="pt", max_length=512, truncation=True
#     )
#     mock_model_instance.generate.assert_called_once()

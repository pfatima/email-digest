# AI-Powered Email Digest Generator

## Overview
The **Email Digest Generator** is a Python-based tool designed to simplify email management. It connects to your email inbox, retrieves recent messages, summarizes their content using AI, and generates a concise daily report. The generated digest is saved as a text file for easy reference.

## Features
- **Email Fetching**: Connects securely to your email inbox using IMAP.
- **Content Extraction**: Processes emails to extract plain text content, even from multipart messages.
- **AI Summarization**: Summarizes email content using the open-source **Flan-T5** model.
- **Daily Digest Creation**: Combines email subjects and summaries into a structured report.
- **File Saving**: Saves the digest as a text file for offline access.

## How It Works
1. **Fetch Emails**: Retrieves recent emails from your inbox.
2. **Extract Content**: Extracts and processes plain text from emails.
3. **Summarize with AI**: Uses Flan-T5 to generate concise summaries.
4. **Generate a Digest**: Combines summaries into a formatted report.
5. **Save to File**: Stores the digest as a text file.

## Setup

### Requirements
- Python 3.7 or higher
- Install dependencies from `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```

### Dependencies
- `transformers==4.34.0`
- `torch>=1.9.0`
- `sentencepiece==0.1.99`
- `pytest==7.4.2` (for testing)

### Environment Variables
Set the following environment variables for custom configurations (optional):
- `IMAP_SERVER` (default: `imap.gmail.com`)
- `IMAP_PORT` (default: `993`)
- `MODEL_NAME` (default: `google/flan-t5-small`)

## Usage

### Run the Tool
1. Clone the repository.
2. Navigate to the project directory.
3. Run the tool:
   ```bash
   python project.py
   ```
4. Enter your email credentials when prompted.

### Output
- A text file named `daily_digest.txt` will be created in the project directory containing the summarized digest.

## Testing
The project includes unit tests to ensure all functions work as expected.
Run tests with:
```bash
pytest test_project.py
```

## Notes
- This tool is designed for personal email management and does not store credentials.
- Use an app-specific password for secure email access when using providers like Gmail.

## License
This project is open-source and available under the [MIT License](LICENSE).

## Acknowledgments
- [Hugging Face](https://huggingface.co/) for the Flan-T5 model.
- Python community for libraries and resources.

---

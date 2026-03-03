# DocSummarizer: Google Drive AI Summarizer

An AI-powered document summarizer that integrates with Google Drive, extracts text from files (PDF, DOCX, TXT), and provides concise summaries using OpenAI.

## Features
- **Google Drive Integration**: Bulk list and download documents from a specific folder.
- **Multiformat Support**: Extracts text from `.pdf`, `.docx`, and `.txt` files.
- **AI Summarization**: Uses OpenAI's GPT models for high-quality summaries.
- **Modern Web Dashboard**: Glassmorphism-inspired UI with a dark theme.
- **Exportable Reports**: Download summaries in CSV or PDF format.

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- A Google Cloud Project with the **Google Drive API** enabled.
- An **OpenAI API Key**.

### 2. Google OAuth2 Setup
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Enable the **Google Drive API**.
4. Configure the **OAuth Consent Screen** (Internal or External/Testing).
5. Go to **Credentials** -> **Create Credentials** -> **OAuth client ID**.
6. Select **Desktop app**.
7. Download the JSON file and rename it to `credentials.json` in the project root.

### 3. Installation
```bash
# Install dependencies
pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Running the Application
```bash
python main.py
```
Alternatively, use uvicorn:
```bash
uvicorn main:app --reload
```

Open your browser at `http://localhost:8000`.

## Project Structure
- `main.py`: FastAPI entry point and routes.
- `services/`:
    - `auth.py`: Google OAuth2 authentication.
    - `drive_service.py`: Folder listing and file downloads.
    - `extractor.py`: Text extraction for PDF, DOCX, and TXT.
    - `summarizer.py`: OpenAI API integration.
    - `report_gen.py`: CSV and PDF generation logic.
- `templates/`: Jinja2 HTML templates.
- `static/`: CSS and assets.

## Usage
1. Enter the Folder ID of the Google Drive folder you want to summarize.
2. Click **Start Summarization**.
3. Authenticate with Google (if it's the first time).
4. Review summaries in the browser and download reports.

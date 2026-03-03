# DocSummarizer: Google Drive AI Summarizer

An AI-powered document summarizer that integrates with Google Drive, extracts text from files (PDF, DOCX, TXT), generates concise summaries using OpenAI/OpenRouter, and persists results in **MongoDB**.

## Features
- **Google Drive Integration**: Bulk list and download documents from a specific folder.
- **Multiformat Support**: Extracts text from `.pdf`, `.docx`, and `.txt` files.
- **AI Summarization**: Uses OpenAI/OpenRouter GPT models for high-quality summaries.
- **MongoDB Persistence**: Folder results are saved and can be retrieved across sessions.
- **Background Processing**: Non-blocking document processing with real-time status tracking.
- **Modern Web Dashboard**: Glassmorphism-inspired UI with a dark theme.
- **Exportable Reports**: Download summaries in CSV or PDF format.

---

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- A Google Cloud Project with the **Google Drive API** enabled.
- An **OpenAI / OpenRouter API Key**.
- A running **MongoDB** instance (local or cloud, e.g. MongoDB Atlas).

### 2. Google OAuth2 Setup
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Enable the **Google Drive API**.
4. Configure the **OAuth Consent Screen** (Internal or External/Testing).
5. Go to **Credentials** → **Create Credentials** → **OAuth client ID**.
6. Select **Desktop app**.
7. Download the JSON file and rename it to `credentials.json` in the project root.

### 3. Installation
```bash
pip install -r requirements.txt
```

### 4. Configuration
Create a `.env` file in the project root (see `.env.example`):
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
MONGO_URI=mongodb://localhost:27017/doc_summarizer
```

> **Note:** `MONGO_URI` defaults to `mongodb://localhost:27017/doc_summarizer` if not set.  
> For MongoDB Atlas, use the connection string from your cluster dashboard.

### 5. Running the Application
```bash
python main.py
```
Or with uvicorn directly:
```bash
uvicorn main:app --reload
```

Open your browser at `http://localhost:8000`.

On startup, the app will verify the MongoDB connection and log the result:
```
✅ MongoDB connected successfully.
```

---

## Project Structure
```
.
├── main.py                  # FastAPI entry point, routes & lifespan
├── credentials.json         # Google OAuth2 credentials (not committed)
├── .env                     # Environment variables (not committed)
├── requirements.txt
└── services/
    ├── auth.py              # Google OAuth2 authentication
    ├── drive_service.py     # Folder listing and file downloads
    ├── extractor.py         # Text extraction (PDF, DOCX, TXT)
    ├── summarizer.py        # OpenRouter/OpenAI API integration
    ├── report_gen.py        # CSV and PDF report generation
    └── database.py          # MongoDB client and persistence layer
├── templates/               # Jinja2 HTML templates
└── static/                  # CSS and static assets
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main dashboard |
| `POST` | `/summarize` | Start background summarization for a folder |
| `GET` | `/status` | Current processing status + MongoDB connection status |
| `GET` | `/api/folders` | List all previously processed folders |
| `GET` | `/api/folders/{folder_id}` | Get results for a specific folder |
| `DELETE` | `/api/folders/{folder_id}` | Delete a folder's saved results |
| `GET` | `/export/csv` | Download results as CSV |
| `GET` | `/export/pdf` | Download results as PDF |

---

## Usage
1. Enter the **Folder ID** of the Google Drive folder you want to summarize.
2. Click **Start Summarization** — processing runs in the background.
3. Authenticate with Google (first run only).
4. Monitor progress via the dashboard; results update incrementally.
5. Previously processed folders are saved and accessible from the sidebar.
6. Download reports as **CSV** or **PDF** at any time.

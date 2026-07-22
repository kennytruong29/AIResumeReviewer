# AI Resume Reviewer

A Claude powered web application that parses content of a DOCX or PDF and provides structured feedback tailored to software engineers, based on a job description.

[Live Demo](https://airesumereviewer-1ohc.onrender.com)

## Tech Stack
Language used: Python 3.14.6

### Backend
- FastAPI
- Uvicorn

### File parsing
- pdfplumber
- python-docx

### AI
- Anthropic API
- Claude Sonnet 4.6 (can be changed within backend)

### Frontend
- Streamlit

### Deployment
- Render


## Features
- File uploading: Upload a DOCX or PDF resume.
- Error handling: Validates file types by extension and rejects empty files and unsupported formats.
- Structured feedback from Claude: Provides an overall score and gives feedback on resume structure, keyword matching, quantifiable achievements and skills alignment.

## How to Run Locally

### Prerequisite
The following needs to be installed:
- python3.x
- pip

### Getting the code 
`git clone https://github.com/kennytruong29/AIResumeReviewer`

### Setting up the environment
- Create virtual environment: `python -m venv venv`
- Activate on Windows: `venv\Scripts\activate`
- Activate on Mac/Linux: `source venv/bin/activate`

### Install dependencies:
- `pip install -r backend/requirements.txt`
- `pip install -r frontend/requirements.txt`

### Configuration
Create a .env file in the root folder and add:

- `ANTHROPIC_API_KEY=your_key_here`
- `API_URL=http://127.0.0.1:8000`

NOTE: Change API_URL to the backend API url link when running on deployment

### Running both services
Run simultaneously in separate windows:
- `uvicorn backend.get_resume:app --host 0.0.0.0 --port 8000`
- `streamlit run frontend/index.py`

## Known Limitations

- Cannot read DOCX tables: Parsing of docx is limited to body content. Table content cannot currently be parsed.

- No checking of magic bytes: File validation relies on extension checking only. A malicious file with a renamed extension may not be rejected as the file's true format is not verified at the byte level.

- Unsupported formats: DOC and txt files are not supported.


## Future Improvements
- DOCX table content parsing
- Allow uploading DOC and txt files
- Magic bytes validation
- Create an interactive experience in which you are able to chat with the AI rather than just a one-time response
- Get code working on docker to ensure it works on all machines

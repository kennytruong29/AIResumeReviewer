from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from pathlib import Path
from io import BytesIO
from docx import Document
from dotenv import load_dotenv
import anthropic
import pdfplumber
import os

load_dotenv()
app = FastAPI()
client = anthropic.Anthropic(
    api_key=os.getenv('ANTHROPIC_API_KEY')
)
accepted_extensions = ['.pdf','.docx']

@app.post("/files/")
async def get_resume(file: UploadFile, job_description: Annotated[str, Form()]):
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in accepted_extensions:
        raise HTTPException(status_code=400, detail="Incorrect file type uploaded")
    if job_description.strip() == "":
        raise HTTPException(status_code=400, detail="No text found in job description")
    
    file_bytes = await file.read()
    content = BytesIO(file_bytes)

    if file_extension == '.pdf':
        raw_content = pull_content_pdf(content)   
    else:
        raw_content = pull_content_docx(content)

    if raw_content is None or raw_content.strip() == "":
        raise HTTPException(status_code=400, detail="No text found in provided resume")
    
    output = await provide_feedback(raw_content, job_description)
    return output
        
    
def pull_content_pdf(file: BytesIO) -> str:
    with pdfplumber.open(file) as pdf:
        return pdf.pages[0].extract_text(x_tolerance=1, y_tolerance=1)
    
def pull_content_docx(file: BytesIO) -> str:
    doc = Document(file)
    doc_content = [para.text for para in doc.paragraphs]
    return " ".join(doc_content)


async def provide_feedback(raw_content : str, job_description : str):
    try:
        message = client.messages.create(
        max_tokens = 1024,
        system = """You are an expert technical recruiter. You specialize in helping software engineers land their next big job. You will be given someone's resume in text format and a job description.
            Provide direct and structured feedback in regards to these things: Resume Structure, Content Quality and/or Redundancies, Keyword Match, Quantifiable Achievements, Skills Alignment and Other Suggestions
            Your answer structure should be as follows: General feedback score, Resume Structure, Keyword Match, Quantifiable Achievements, Skills Alignment and Other Suggestions
            You will always receive resume content first, then the job description. Do not answer until you receive both.""",
        messages = [
            {
                "role": "user",
                "content": f"Here is my raw resume: {raw_content} and here is the job description: {job_description}"
            }
        ],
        model = "claude-opus-4-8"
    )
        response = message.content[0].text
        return response
    except anthropic.APIConnectionError as e:
        raise HTTPException(status_code=503, detail=e.__cause__)
    except anthropic.RateLimitError as e:
        raise HTTPException(status_code=e.status_code, detail=e.__cause__)
    except anthropic.APIStatusError as e:
        raise HTTPException(status_code=e.status_code, detail=e.response)
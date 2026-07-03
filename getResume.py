from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from pathlib import Path
import pdfplumber
from io import BytesIO
from docx import Document

app = FastAPI()

acceptedExtensions = ['.pdf','.docx']

@app.post("/files/")
async def getResume(file: UploadFile, jobDescription: Annotated[str, Form()]):
    fileExtension = Path(file.filename).suffix.lower()

    if fileExtension not in acceptedExtensions:
        raise HTTPException(status_code=400, detail="Incorrect file type uploaded")
    
    fileBytes = await file.read()
    content = BytesIO(fileBytes)

    if fileExtension == '.pdf':
        return pullContentPDF(content)   
    else:
        return pullContentDoc(content)
    
def pullContentPDF(file: BytesIO):
    with pdfplumber.open(file) as pdf:
        return pdf.pages[0].extract_text(x_tolerance=1, y_tolerance=1)
    
def pullContentDoc(file: BytesIO):
    doc = Document(file)
    doc_content = [para.text for para in doc.paragraphs]
    return doc_content
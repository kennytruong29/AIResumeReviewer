from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from pathlib import Path

app = FastAPI()

acceptedExtensions = ['.txt','.pdf', '.doc', '.docx']

@app.post("/files/")
async def getResume(file: UploadFile, jobDescription: Annotated[str, Form()]):
    fileExtension = Path(file.filename).suffix.lower()
    if not any(x in fileExtension for x in acceptedExtensions):
        raise HTTPException(status_code=400, detail="Incorrect file type uploaded")
    content = await file.read()
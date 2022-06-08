from typing import List

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates

from fpdf import FPDF

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}



@app.post("/word_to_pdf/")
async def create_upload_files(files: List[UploadFile]):
    file = files[0].file

    # pdf = FPDF()
    # pdf.add_page()
    # pdf.set_font('Arial', size=14)
    print(file)
    return {"filenames": [file.filename for file in files]}
from io import BytesIO
from typing import List

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates

from fpdf import FPDF

from helpers import upload_file_to_bytes

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/txt_to_pdf/")
async def create_upload_files(files: List[UploadFile]):
    try:
        buffer = BytesIO(await files[0].read())

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', size=14)

        pdf.cell(50, 5, txt=str(buffer.getvalue()), ln=1, align='C')

        pdf.output('test.pdf')
    except Exception as e:
        print(e)
    return {"filenames": [file.filename for file in files]}
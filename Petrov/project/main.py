import os
import time
from io import BytesIO
from typing import List

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.openapi.models import Response
from fastapi.templating import Jinja2Templates

from fpdf import FPDF
from starlette.responses import FileResponse

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

        rows = buffer.getvalue().decode().split('\n')
        for r in rows:
            pdf.cell(200, 20, txt=r, ln=1, align='C')

        fn = f'media/{files[0].filename}__.pdf'
        pdf.output(fn)
        return FileResponse(fn, media_type='application/pdf', filename=files[0].filename + '__.pdf')
    except Exception as e:
        return {"error": str(e)}

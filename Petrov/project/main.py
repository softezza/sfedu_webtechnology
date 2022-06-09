import os
import time
from io import BytesIO
from typing import List

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates

from fpdf import FPDF
from starlette.responses import FileResponse
from PyPDF2 import PdfMerger

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
            pdf.cell(200, 20, txt=r, ln=1, align='R')

        fn = f'media/{files[0].filename}__.pdf'
        pdf.output(fn)
        return FileResponse(fn, media_type='application/pdf', filename=files[0].filename + '__.pdf')
    except Exception as e:
        return {"error": str(e)}


@app.post("/img_to_pdf/")
async def create_upload_files(files: List[UploadFile]):
    try:
        tmp_img_name = f'media/tmp__{files[0].filename}'
        with open(tmp_img_name, 'wb') as fp:
            fp.write(await files[0].read())

        pdf = FPDF()
        pdf.add_page()
        pdf.image(tmp_img_name, 10, 10)

        fn = f'media/{files[0].filename}__.pdf'
        pdf.output(fn)

        os.remove(tmp_img_name)
        return FileResponse(fn, media_type='application/pdf', filename=files[0].filename + '__.pdf')
    except Exception as e:
        return {"error": str(e)}

@app.post("/merge_pdf/")
async def create_upload_files(files: List[UploadFile]):
    try:
        tmp_img_name = f'media/tmp__{files[0].filename}'
        with open(tmp_img_name, 'wb') as fp:
            fp.write(await files[0].read())

        pdf = FPDF()
        pdf.add_page()
        pdf.image(tmp_img_name, 10, 10)

        fn = f'media/{files[0].filename}__.pdf'
        pdf.output(fn)

        os.remove(tmp_img_name)
        return FileResponse(fn, media_type='application/pdf', filename=files[0].filename + '__.pdf')
    except Exception as e:
        return {"error": str(e)}

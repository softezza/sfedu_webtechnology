import io, os, uuid, shutil, uvicorn
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Response, Path, HTTPException, Depends, Form, Cookie
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse, FileResponse
from starlette.requests import Request
from database import Base, engine, SessionLocal
from pdf_diff import command_line
from imp import reload

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#model
class Users(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)

#schema
class UsersSchema(BaseModel):
    id:int 
    email:str 
    password:str

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

@app.get("/PDF")
def index():
    return {"message": "WELCOME in PDF"}

async def get_user_by_email(email: str, db: Session):
    return db.query(Users).filter(Users.email == email).first()

@app.post("/register")
async def registerfunc(id = Form(...), email = Form(...), password = Form(...), db:Session=Depends(get_db)):
    ##### db work to put data into db
    people = Users(id=id, email=email, password=password)
    # print("1111111",people)
    db.add(people)
    # print("22222222222",people)
    db.commit()
    db.refresh(people)
    return people

@app.post("/login")
async def loginfunc(response : Response, is_login : str =  Cookie(None), email = Form(...), password = Form(...), db:Session=Depends(get_db)):
    if is_login == "1":
        return {"message":"you are already logged in"}

    results = db.query(Users).filter(Users.email == email).first()


    if email == results.email and password == results.password:
        response.set_cookie(key="is_login",value="1")

        return "You are logged in. Your user id is {}".format(str(results.id))

DIFF_ID_HEADER = "X-PdfDiff-Id"
DIFF_JSON = "diff.json"
DIFF_PDF = "diff.pdf"
BASE_WORKING_DIR = "working_dir"

@app.post("/diff")
def pdf_diff(response: Response,
             prev: UploadFile = File(...),
             current: UploadFile = File(...),
             img: Optional[bool] = True):
    diff_id = str(uuid.uuid4())
    working_dir = BASE_WORKING_DIR + "/" + diff_id + "/"
    # Create a new directory structure for each request to store the uploaded files and diff.pdf
    os.makedirs(working_dir)
    prev_path = copy_file(working_dir, prev, "prev.pdf")
    current_path = copy_file(working_dir, current, "current.pdf")
    changes = command_line.compute_changes(prev_path, current_path)

    json_path = working_dir + "/" + DIFF_JSON
    import json
    with open(json_path, "w") as fp:
        json.dump(changes, fp)

    pdf_path = working_dir + "/" + DIFF_PDF
    render_changes(changes, pdf_path)
    if img:
        custom_headers = {
            DIFF_ID_HEADER: diff_id,
            "access-control-expose-headers": DIFF_ID_HEADER
        }
        return FileResponse(pdf_path,
                            media_type="application/pdf",
                            headers=custom_headers,
                            filename="diff.pdf")
    else:
        response.headers["access-control-expose-headers"] = DIFF_ID_HEADER
        response.headers[DIFF_ID_HEADER] = diff_id
        return changes

@app.get("/diff/{diff_id}")
def get_diff_by_id(response: Response,
                   diff_id: str = Path(..., title="Diff Id to return"),
                   img: Optional[bool] = True):
    working_dir = BASE_WORKING_DIR + "/" + diff_id

    json_path = working_dir + "/" + DIFF_JSON
    json_exists = os.path.exists(json_path)

    pdf_path = working_dir + "/" + DIFF_PDF
    pdf_exists = os.path.exists(pdf_path)
    if (not json_exists and not pdf_exists):
        raise HTTPException(
            status_code=404,
            detail="Diff Id not found. Consider creating a new Diff Id.")

    # If only JSON exists, generate the PDF and return it, else return PDF directly
    if json_exists and not pdf_exists:
        import json
        with open(json_path, "r") as json_file:
            changes = json.load(json_file)
        render_changes(changes, pdf_path)

    if img:
        return FileResponse(pdf_path,
                            media_type="application/pdf",
                            filename="diff.pdf")
    else:
        import json
        with open(json_path, "r") as json_file:
            changes = json.load(json_file)
        return changes

def copy_file(upload_directory: str, source: UploadFile, filename: str):
    final_file = os.path.join(upload_directory, filename)
    file_to_copy_to = open(final_file, "wb+")
    shutil.copyfileobj(source.file, file_to_copy_to)
    file_to_copy_to.close()
    return final_file

def render_changes(changes, pdf_path):
    if len(changes) == 0:
        # Create a mock PDF and write that
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(40, 10,
                 "There are no textual differences between the documents.")
        pdf.output(pdf_path, "F")
    else:
        img = command_line.render_changes(changes, "strike,box".split(","),
                                          900)
        rgb_img = img.convert("RGB")
        rgb_img.save(pdf_path,
                     "pdf",
                     save_all=True,
                     title="Textual Differences",
                     producer="PDF-Diff/v0.1")
        del img
        del rgb_img

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)

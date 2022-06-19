from fastapi import FastAPI, UploadFile
import json
import PIL.Image as pimg
from pymysql import connect

forbiddenwords = ["идиот", "***", "свингер пати", "митинг", "рэп-баттл", "javascript"]
app = FastAPI()

@app.post("/add_new_content/")
def add_new_content(file: UploadFile, ContentDescription):
    try:
        tmp_file = file.read()
        if not isinstance(tmp_file, pimg):
            return {"status": "uploaded wrong image file"}
        if not check_content_credibility(ContentDescription):
            return {"status": "uploaded wrong description"}
        add_content_toDB(tmp_file ,ContentDescription)
        return {"status": "content added successfuly"}
    except Exception as e:
        return {"error": str(e)}

def check_content_credibility(ContentDescriptionn):
    return all([False if ContentDescription.get(key_) in forbiddenwords else True for key_ in ContentDescription])

def add_content_toDB(tmp_file : pimg,ContentDescription):    
    insert_query = f"INSERT INTO Content (date, name, tags, adress, price, city) VALUES ({ContentDescription.get('date'),ContentDescription.get('name'),ContentDescription.get('tags'),ContentDescription.get('adress'), ContentDescription.get('price'), ContentDescription.get('city')});"
    execute_query(insert_query)

def execute_query(query: str):
        with connect(host="localhost", user='admin', password='homersimpson') as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
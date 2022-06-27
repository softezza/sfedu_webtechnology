from fastapi import FastAPI
from datetime import date
from pydantic import BaseModel
from json import JSONEncoder
import json
import uvicorn
import os
import shutil
import zipfile
from zipfile import ZipFile
from os import path
from shutil import make_archive
from mysql.connector import connect, Error

class NameARC(BaseModel):
    name: str
    dist: str
	
app = FastAPI()

@app.get('/')
def home():
    return get_arc()

@app.get('/arctype')
def get_arc():
    arc = get_type_from_db()
    return serialize(arc)

@app.get('/name')
def get_namearc(): 
    return ()
    
@app.get('/path')
def find_path():
	src = path.realpath

@app.post('/archivation')
def post_arc():
	root_dir,tail = path.split(src)
		
archive = zipfile.ZipFile('Archive.zip', mode='w')

@app.put('/archivation/file')
def post_arc():
	root_dir,tail = path.split(src)
		
archive = zipfile.ZipFile('Archive.zip', mode='w')

@app.post('/unarchive')
def post_unarchive(dist):
	archive = zipfile.ZipFile(dist)
	archive.extractall(dist)
	archive.close()
	
def execute_select_query(query: str):
    #try:
        with connect(
        host="localhost",
        user='root',
        password='242338',
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
    #except Error as e:
    #    print(e)
        
def execute_query(query: str):
    #try:
        with connect(
        host="localhost",
        user='root',
        password='242338',
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
    #except Error as e:
    #    print(e)
	
if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)
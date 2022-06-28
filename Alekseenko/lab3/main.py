from fastapi import FastAPI
from datetime import date
from pydantic import BaseModel
from json import JSONEncoder
import json
import uvicorn
#from mysql.connector import connect, Error

class Photo(BaseModel):
    id: int = None
    brightness: int
    contrast: int
  


class EmployeeEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

app = FastAPI()

def serialize(obj):
    return json.dumps(obj, cls=EmployeeEncoder, ensure_ascii=False)
    #return obj.__dict__
     
@app.get('/')
def home():
    return get_photo()

@app.get('/photo')
def get_photo():
    photo = get_photo_from_db()
    return serialize(photo)

@app.get('/photo/{photoId}')
def get_photo(photoId: int): 
    photo = get_photo_from_db(photoId)
    return serialize(photo[photoId])

    
@app.post('/photo')
def create_photo(newphoto: Photo):
    insert_query = f"INSERT INTO editor.photo(brightness, contrast) VALUES('{newphoto.brightness}',{newphoto.contrast});"
    execute_query(insert_query)
    

@app.put('/photo')
def put_photo(newphoto: Photo):
    insert_query = f"UPDATE editor.photo SET brightness = '{newphoto.brightness}' WHERE id = {newList.id};"
    execute_query(insert_query)
    
    
@app.delete('/photo/{photoId}')
def delete_photo(photoId: int):
    delete_query = f"DELETE FROM editor.photo WHERE id = {photoId};"
    execute_query(insert_query)


def get_photo_from_db(id: int):
    select_photo_query = f"SELECT id, brightness, contrast FROM editor.photo WHERE id = {id};"
    table = execute_select_query(select_photo_query)
    row = table[0]
    MyPhoto = Photo(id = row[0], brightness = row[1], contrast = row[2])
    return myPhoto
    
def get_photo_from_db():
    select_photo_query = "SELECT id, brightness, contrast FROM editor.photo;"
    table = execute_select_query(select_photo_query)
    photo = list()
    for row in table:
        MyPhoto = Photo(id=row[0], brightness=row[1], contrast=row[2])
        photo.append(MyPhoto)
    return photo
    

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

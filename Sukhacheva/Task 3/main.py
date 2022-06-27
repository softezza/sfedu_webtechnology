from fastapi import FastAPI
from datetime import date
from pydantic import BaseModel
from json import JSONEncoder
import json
import uvicorn
from mysql.connector import connect, Error

app = FastAPI()

@app.post('/cakes')
def put_cakes():
    query_str="SELECT * FROM Cakes;"
    return transform_date_cakes(execute_select_query(query_str))

def transform_date_cakes(date):
    return date    

@app.post('/contacts')
def put_contacts():
    query_str="SELECT * FROM Contacts;"
    return transform_date_contacts(execute_select_query(query_str))

def transform_date_contacts(date):
    return date
  
@app.post('/bakery')
def put_bakery():
    query_str="SELECT * FROM Bakery;"
    return transform_date_bakery(execute_select_query(query_str))

def transform_date_bakery(date):
    return date    

@app.post('/desserts')
def put_desserts():
    query_str="SELECT * FROM Desserts;"
    return transform_date_desserts(execute_select_query(query_str))

def transform_date_desserts(date):
    return date    

def execute_select_query(query: str):
    #try:
        with connect(
        host="localhost",
        user='root',
        password='qwerty123',
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()

if __name__ == '__main__':
    print("Проверка")
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)
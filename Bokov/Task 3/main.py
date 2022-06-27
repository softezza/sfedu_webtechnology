from fastapi import FastAPI
from datetime import date
from pydantic import BaseModel
from json import JSONEncoder
import json
import uvicorn
from mysql.connector import connect, Error

app = FastAPI()

@app.post("/log_in/")
def checkCredentials(credentials):
    hash_password = findHashPasswordSql(credentials.get("login"))
    if hash_password is not None and (hash_password == createHash(credentials.get("password"))):
        return {"access":True}
    else:
        return {"access":False, "info": "wrong login\password"}

def findHashPasswordSql(login : str):
     gethash_query = f"SELECT password_hash FROM Credentials WHERE login = {login};"
     return execute_select_query(gethash_query)

def executeSelectQuery(query: str):
        with connect(host="localhost", user='mirmikeeper', password='iloweants') as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchone()

def createHash(password: str):
    """Заглушка, имитирует создание хеша"""
    return password

@app.post('/')
def putAntColony():
    query_str="SELECT * FROM Colony;"
    return tansDateColony(execute_select_query(query_str))

def tansDateColony(Date_fromDB):
    return Date_fromDB

@app.post('/')
def putAntHome():
    query_str="SELECT * FROM Home;"
    return tansDateHome(execute_select_query(query_str))

def tansDateHome(Date_fromDB):
    return Date_fromDB
    
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

if __name__ == '__main__':
    print("Проверка")
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)
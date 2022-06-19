from fastapi import FastAPI, UploadFile
import json
from pymysql import connect

app = FastAPI()

@app.post("/log_in/")
def check_credentials(credentials):
    hash_password = find_hash_password_sql(credentials.get("login"))
    if hash_password is not None and (hash_password == create_hash(credentials.get("password"))):
        return {"access":True}
    else:
        return {"access":False, "info": "wrong login\password"}

def find_hash_password_sql(login : str):
     gethash_query = f"SELECT password_hash FROM Credentials WHERE login = {login};"
     return execute_select_query(gethash_query)

def execute_select_query(query: str):
        with connect(host="localhost", user='admin', password='homersimpson') as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchone()

def create_hash(password: str):
    """Заглушка, имитирует создание хеша"""
    return password
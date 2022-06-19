from fastapi import FastAPI, UploadFile
import json
from pymysql import connect

app = FastAPI()

@app.post("/filter_city/{city_name}")
def find_city_contents(city_name : str):
     get_by_city_query = f"SELECT * FROM Content WHERE city = {city_name};"
     return {"contents": execute_select_query(get_by_city_query)}

def execute_select_query(query: str):
        with connect(host="localhost", user='admin', password='homersimpson') as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()

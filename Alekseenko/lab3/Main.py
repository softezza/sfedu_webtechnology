import Filter, Login, Upload
import uvicorn
from fastapi import FastAPI
from pymysql import connect
app = FastAPI()

@app.get('/')
def main():
    return {"Hello": "world"} #просто проверка что все работает

if __name__ == '__main__':
    uvicorn.run('Main:app', port=8000, host='0.0.0.0', reload=True)

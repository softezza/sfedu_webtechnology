import login_register_routes,file_router
from fastapi import FastAPI
from datetime import date
from pydantic import BaseModel
from json import JSONEncoder
import json
import pydub
import uvicorn

app = FastAPI()
app.include_router(login_register_routes.login_router)
app.include_router(file_router.file_router)


@app.get('/')
def main():
    return {"Hello": "world"}


if __name__ == "__main__":
    uvicorn.run('main:app', port=4445, host='0.0.0.0', reload=True)

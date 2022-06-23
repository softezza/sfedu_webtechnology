import json
import uvicorn
from project_utils import *
from fastapi import FastAPI
from db_worker import Connect2Database


app = FastAPI()


@app.get('/log_in/{login_and_pwd}')
def set_login_and_pwd(login_and_pwd: dict):
    pass


@app.post('/sign_in/{val}')
def set_number_of_phone_or_email(val: str):
    if not check_match(val):
        print(val)
        return {"error_value": 'неверный формат'}
    else:
        generate_key()
        return {'is_ok': 'ожидайте, код подтверждения прийдет в течении 2-х минут'}


@app.get('/user_form/{user_form}')
def set_user_form(user_form: dict):
    connector = Connect2Database()


if __name__ == "__main__":
    uvicorn.run('main:app', port=10000, host='127.0.0.1', reload=True)

import uvicorn
from fastapi import FastAPI
from project_utils import *


app = FastAPI()


@app.get('/')
def main():
    return {"Hello": "world"}


@app.post('/sign_in/{val}')
def set_number_of_phone_or_email(val: str):
    if not check_match(val):
        return {"error_value": 'неверный формат'}
    else:
        send_key(val)
        return {'is_ok': 'ожидайте, код подтверждения прийдет в течении 2-х минут'}


@app.get('/log_in/{login_and_pwd}')
def set_login_and_pwd(login_and_pwd):
    login_ = login_and_pwd.get('login')
    pwd = login_and_pwd.get('pwd')
    is_exist, inform = is_excist_log(login_)
    if not is_exist:
        return {'warning': '{} - user not found'.format(login_)}
    if not is_comparing_passwords(pwd, inform):
        return {'warning': 'wrong password'}
    return {'access': 'wellcam'}


@app.get('/user_form/{user_form}')
def set_user_form(user_form):
    connector = Connect2Database()
    cursor = connector.get_cursor()
    cursor.execute(create_query_for_inserting_form_parser(user_form))
    connector.commit()


if __name__ == "__main__":
    uvicorn.run('main:app',
                port=10000,
                host='0.0.0.0',
                reload=True)

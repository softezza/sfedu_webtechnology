from fastapi import FastAPI
from project_utils import *


app = FastAPI()


@app.get('/log_in/{login_and_pwd}')
def set_login_and_pwd(login_and_pwd: dict):
    login_ = login_and_pwd.get('login')
    pwd = login_and_pwd.get('pwd')
    is_exist, inform = is_excist_log(login_)
    if not is_exist:
        return {'warning': '{} - user not found'.format(login_)}
    if not is_comparing_passwords(pwd, inform):
        return {'warning': 'wrong password'}
    return {'access': 'wellcam'}

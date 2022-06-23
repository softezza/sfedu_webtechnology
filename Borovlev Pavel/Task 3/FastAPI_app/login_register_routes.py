from fastapi import FastAPI, UploadFile, APIRouter
from mysql_connector import MySQLConnector
from pydantic import BaseModel
import json
import traceback
import hashlib
import uuid

login_router = APIRouter()


class User(BaseModel):
    uuid: str = ""
    username: str
    pwd_hash: str


@login_router.post("/log_in/")
def check_credentials(username: str, password: str):
    try:
        password = password
        username = username
        hash_password = create_pwd_hash(password)
        user = find_user(username)
        print("user", user)
        if (user is not None and hash_password is not None) and (username == user[0] and hash_password == user[1]):
            return {"access": True}
        else:
            return {"access": False, "info": "wrong login/password"}
    except Exception as e:
        print(e)
        return {"error_type": "login", "errno": -1}


def find_user(login: str):
    db = MySQLConnector(usr="ksdv", adr="localhost", pwd="123", db="fastapi_app")
    get_user_query = "SELECT user_login, pwd_hash FROM app_users WHERE user_login = %s;"
    params = (login,)
    user = db.make_a_query(get_user_query, params)
    db.close_connection()
    return user


@login_router.post("/register/")
def create_user(user: str, password: str):
    try:
        db = MySQLConnector(usr="ksdv", adr="localhost", pwd="123", db="fastapi_app")
        query = "INSERT INTO app_users(user_uuid,user_login,pwd_hash) VALUES (%s, %s, %s)"
        user_uuid = str(uuid.uuid1().hex)
        hash_pwd = create_pwd_hash(password)
        params = (user_uuid, user, hash_pwd)
        #print(params)
        res = db.make_a_query(query, params)
        db.close_connection()
        return {"is_successful": True, "username": user, "password": hash_pwd}
    except Exception as e:
        traceback.print_exc()
        return {"is_successful": False, "errno": -1}


def create_pwd_hash(password: str):
    hashing_algo = hashlib.sha1()
    hashing_algo.update(password.encode())
    pwd_hash = hashing_algo.hexdigest()
    return pwd_hash

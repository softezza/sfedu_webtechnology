from typing import List

import uvicorn
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

import models, schemas, crud
from db import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
	db = None
	try:
		db = SessionLocal()
		yield db
	finally:
		db.close()


@app.post("/user")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
	db_user = crud.get_user_by_username(db, username=user.username)
	if db_user:
		raise HTTPException(status_code=400, detail='Username already registered')
	else:
		crud.create_user(db=db, user=user)
		return {'response': 'the user was successfuly created'}

@app.get("/users/", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
	users = crud.get_users(db)
	return users

@app.post("/login")
def check_credentials(username: str, password: str, db: Session = Depends(get_db)):
	db_user = crud.get_user_by_username(db, username=username)
	if (db_user is not None and db_user.password == password):
		return {'access': True}
	else:
		return {'access': False}
		raise HTTPException(status_code=403, detail='Invalid credentials')

@app.post("/message")
def create_message(username: str, password: str, message: schemas.MessageCreate, db: Session = Depends(get_db)):
	token = check_credentials(username, password, db)
	db_user = crud.get_user_by_username(db, username=username)
	if token['access']:
		crud.create_message(db=db, message=message, user=db_user)
		return {'response': 'the message was successfuly created'}
	else:
		raise HTTPException(status_code=403, detail='Invalid credentials')

@app.get("/messages/", response_model=List[schemas.Message])
def read_messages(db: Session = Depends(get_db)):
	messages = crud.get_messages(db)
	return messages


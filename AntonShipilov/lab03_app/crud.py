from sqlalchemy.orm import Session

import models, schemas


def get_users(db: Session, skip: int = 0, limit: int = 100):
	return db.query(models.User).offset(skip).limit(limit).all()

def get_messages(db: Session, skip: int = 0, limit: int = 100):
	return db.query(models.Message).offset(skip).limit(limit).all()

def get_user_by_username(db: Session, username: str):
	return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
	db_user = models.User(username=user.username, password=user.password)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user

def create_message(db: Session, message: schemas.MessageCreate, user: schemas.User):
	db_message = models.Message(message=message.message, user_id=user.id)
	db.add(db_message)
	db.commit()
	db.refresh(db_message)
	return db_message


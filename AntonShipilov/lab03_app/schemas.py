from typing import List
from pydantic import BaseModel


class UserBase(BaseModel):
	username: str


class UserCreate(UserBase):
	password: str


class User(UserBase):
	id: int

	class Config:
		orm_mode = True


class MessageBase(BaseModel):
	message: str


class MessageCreate(MessageBase):
	pass


class Message(MessageBase):
	id: int
	
	class Config:
		orm_mode = True

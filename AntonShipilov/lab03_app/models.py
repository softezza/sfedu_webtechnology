from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base


class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True)
	password = Column(String)


class Message(Base):
	__tablename__ = 'messages'

	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	message = Column(String)

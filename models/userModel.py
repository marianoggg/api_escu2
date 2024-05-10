from config.db import engine, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel


class User(Base):

    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    username = Column("username", String)
    password = Column("password", String)

    def __init__(self, id1, username1, password1):
        self.id = id1
        self.username = username1
        self.password = password1


Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)  # creo una clase session

sesionPepito = Session()


class InputUser(BaseModel):
    id: int
    username: str
    password: str

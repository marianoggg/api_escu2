from config.db import engine, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel, EmailStr

# from datetime import datetime


class User(Base):

    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column("password", String)
    email = Column("email", String(80), nullable=False, unique=True)
    # created_at = Column(DateTime(), default=datetime.now())
    id_userdetail = Column(Integer, ForeignKey("userdetails.id"))
    userdetail = relationship("UserDetail", backref="user", uselist=False)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    """ def __str__(self):
        return self.username """


class UserDetail(Base):

    __tablename__ = "userdetails"

    id = Column("id", Integer, primary_key=True)
    dni = Column("dni", Integer)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    type = Column("type", String)

    # Referencia de retorno a Usuario
    # usuario = relationship("User", backref="userdetail", uselist=False)

    def __init__(self, dni, firstname, lastname, type):
        self.dni = dni
        self.firstname = firstname
        self.lastname = lastname
        self.type = type


class InputUser(BaseModel):
    username: str
    password: str
    email: EmailStr
    dni: int
    firstname: str
    lastname: str
    type: str


class InputLogin(BaseModel):
    username: str
    password: str


class InputUserDetail(BaseModel):
    dni: int
    firstname: str
    lastname: str
    type: str


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# creo una clase tipo sessionmaker
Session = sessionmaker(bind=engine)

# instancio un objeto que apunte a cada clase Session
session = Session()

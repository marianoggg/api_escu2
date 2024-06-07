from config.db import engine, Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship, mapped_column
from pydantic import BaseModel, EmailStr
import datetime


class User(Base):

    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column("password", String)
    email = Column("email", String(80), nullable=False, unique=True)
    # created_at = Column(DateTime(), default=datetime.now())
    id_userdetail = Column(Integer, ForeignKey("userdetails.id"))
    userdetail = relationship("UserDetail", backref="user", uselist=False)
    payments = relationship("Payment")

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


class Payment(Base):

    __tablename__ = "payments"

    id = Column("id", Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    amount = Column(Integer)
    affected_month = Column(DateTime())
    user_id = Column(Integer, ForeignKey("users.id"))
    career_id = Column(Integer, ForeignKey("careers.id"))
    career = relationship("Career", uselist=False)
    user = relationship("User", uselist=False)

    def __init__(self, user_id, career_id, amount, affected_month):
        self.user_id = user_id
        self.career_id = career_id
        self.amount = amount
        self.affected_month = affected_month


class Career(Base):

    __tablename__ = "careers"

    id = mapped_column("id", Integer, primary_key=True)
    name = mapped_column(String)

    def __init__(
        self,
        name,
    ):
        self.name = name


class InputCareer(BaseModel):
    name: str


class InputPayment(BaseModel):
    user_id: int
    career_id: int
    amount: int
    affected_month: datetime.date


class InputUser(BaseModel):
    username: str
    password: str
    email: EmailStr
    dni: int | None
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


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# creo una clase tipo sessionmaker
Session = sessionmaker(engine)

# instancio un objeto Session
session = Session()

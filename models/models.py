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
    id_userdetail = Column(Integer, ForeignKey("userdetails.id"))
    userdetail = relationship("UserDetail", uselist=False)
    payments = relationship("Payment", back_populates="user")

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class UserDetail(Base):

    __tablename__ = "userdetails"

    id = Column("id", Integer, primary_key=True)
    dni = Column("dni", Integer)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    type = Column("type", String)

    def __init__(self, dni, firstname, lastname, type):
        self.dni = dni
        self.firstname = firstname
        self.lastname = lastname
        self.type = type


class Payment(Base):
    __tablename__ = "payments"

    id = mapped_column("id", Integer, primary_key=True)
    career_id = mapped_column(ForeignKey("careers.id"))
    user_id = mapped_column(ForeignKey("users.id"))
    amount = mapped_column(Integer)
    affected_month = mapped_column(DateTime)
    created_at = mapped_column(DateTime, default=datetime.datetime.now())
    user = relationship("User", uselist=False, back_populates="payments")
    career = relationship("Career", uselist=False)

    def __init__(self, career_id, user_id, amount, affected_month):
        self.career_id = career_id
        self.user_id = user_id
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
    career_id: int
    user_id: int
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


class InputUserPay(BaseModel):
    id: int


class InputUserDetail(BaseModel):
    dni: int
    firstname: str
    lastname: str
    type: str


class InputUserChanges(BaseModel):
    username: str
    email: EmailStr
    password: str


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# creo una clase tipo sessionmaker
Session = sessionmaker(engine)

# instancio un objeto Session
session = Session()

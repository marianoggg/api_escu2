""" from config.db import engine, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel """

""" 
class UserDetail(Base):

    __tablename__ = "userdetails"

    id = Column("id", Integer, primary_key=True)
    dni = Column("dni", Integer)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    type = Column("type", String)

    # Referencia de retorno a Usuario
    # usuario = relationship("User", backref="userdetail", uselist=False)

    def __init__(self, dni, firstname, lastname, type, email):
        self.dni = dni
        self.firstname = firstname
        self.lastname = lastname
        self.type = type

class InputUserDetail(BaseModel):
    dni: int
    firstname: str
    lastname: str
    type: str

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

Session_userdetail = sessionmaker(bind=engine)  # creo una clase session

session_userdetail = Session_userdetail() """

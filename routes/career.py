from fastapi import APIRouter
from models.models import InputCareer, Career, session


career = APIRouter()


@career.get("/career/all")
def obtener_usuarios():
    return session.query(Career).all()


@career.post("/career/add")
def add_career(ca: InputCareer):
    try:
        newCareer = Career(ca.name)
        session.add(newCareer)
        session.commit()
        session.close()
        res = f"Carrera {ca.name} creada!"
        print(res)
        return res
    except Exception as ex:
        print("Error al agregar career --> ", ex)

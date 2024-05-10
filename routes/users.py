from fastapi import APIRouter
from models.userModel import sesionPepito, User, InputUser


user = APIRouter()


@user.get("/")
def welcome():
    return "Bienvenido a la Api Escuela!!"


@user.get("/users/all")
def obtener_usuarios():
    try:
        return sesionPepito.query(User).all()
    except Exception as e:
        print(e)


@user.post("/users/new")
def crear_usuario(user: InputUser):
    usuNuevo = User(user.id, user.username, user.password)
    sesionPepito.add(usuNuevo)
    sesionPepito.commit()
    return "usuario agregado"


@user.get("/users/login/{un}")
def login(un: str):
    try:
        res = sesionPepito.query(User).filter(User.username == un)
        if res.first():
            return res.first()
        else:
            return None
    except:
        print(Exception)

from fastapi import APIRouter
from models.userModel import session, User, InputUser, InputLogin


user = APIRouter()


@user.get("/")
def welcome():
    return "Bienvenido a la Api Escuela!!"


@user.get("/users/all")
def obtener_usuarios():
    try:
        return session.query(User).all()
    except Exception as e:
        print(e)


@user.post("/users/add")
def crear_usuario(user: InputUser):
    usuNuevo = User(
        user.id,
        user.username,
        user.password,
        user.firstName,
        user.lastName,
    )
    session.add(usuNuevo)
    session.commit()
    return "usuario agregado"


@user.post("/users/loginUser")
def login_post(user: InputLogin):
    try:
        usu = User(0, user.username, user.password, "", "")
        res = session.query(User).filter(User.username == usu.username).first()
        if res.password == usu.password:
            return res
        else:
            return None
    except Exception as e:
        print(e)


@user.get("/users/login/{un}")
def login_get(un: str):
    try:
        res = session.query(User).filter(User.username == un).first()
        if res:
            return res
        else:
            return None
    except:
        print(Exception)

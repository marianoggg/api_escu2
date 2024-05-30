from fastapi import APIRouter
from fastapi.responses import JSONResponse
from psycopg2 import IntegrityError
from models.userModel import session, User, UserDetail, InputUser, InputLogin
from sqlalchemy.orm import (
    joinedload,
)  ## para usar la tecnica de carga con union (join loading) para devolcer el objeto user cada user con su userDetail


user = APIRouter()


@user.get("/")
def welcome():
    return "Bienvenido a la Api Escuela!!"


@user.get("/users/all")
def obtener_usuarios():
    try:
        usuarios = session.query(User).options(joinedload("userdetail")).all()

        # Convierte los usuarios en una lista de diccionarios
        usuarios_con_detalles = []
        for usuario in usuarios:
            usuario_con_detalle = {
                "id": usuario.id,
                "username": usuario.username,
                "email": usuario.email,
                "dni": usuario.userdetail.dni,
                "firstname": usuario.userdetail.firstname,
                "lastname": usuario.userdetail.lastname,
                "type": usuario.userdetail.type,
            }
            usuarios_con_detalles.append(usuario_con_detalle)

        return JSONResponse(status_code=200, content=usuarios_con_detalles)
    except Exception as e:
        print("Error al obtener usuarios:", e)
        return JSONResponse(
            status_code=500, content={"detail": "Error al obtener usuarios"}
        )


@user.post("/users/add")
def crear_usuario(user: InputUser):
    try:
        if validate_username(user.username):
            if validate_email(user.email):
                newUser = User(
                    user.username,
                    user.password,
                    user.email,
                )
                newUserDetail = UserDetail(
                    user.dni, user.firstname, user.lastname, user.type
                )
                newUser.userdetail = newUserDetail

                session_user.add(newUser)
                session_user.commit()
                session_user.close()
                return "usuario agregado"
            else:
                return "el email ya existe"
        else:
            return "el usuario ya existe"
    except IntegrityError as e:
        # Suponiendo que el mensaje de error contiene "username" para el campo duplicado
        if "username" in str(e):
            return JSONResponse(
                status_code=400, content={"detail": "Username ya existe"}
            )
        else:
            # Maneja otros errores de integridad
            print("Error de integridad inesperado:", e)
            return JSONResponse(
                status_code=500, content={"detail": "Error al agregar usuario"}
            )
    except Exception as e:
        print("Error inesperado:", e)
        return JSONResponse(
            status_code=500, content={"detail": "Error al agregar usuario"}
        )


@user.post("/users/loginUser")
def login_post(user: InputLogin):
    try:
        usu = User(user.username, user.password, "", "")
        res = session_user.query(User).filter(User.username == usu.username).first()
        if res.password == usu.password:
            return res
        else:
            return None
    except Exception as e:
        print(e)


""" @user.get("/users/login/{un}")
def login_get(un: str):
    try:
        res = session_user.query(User).filter(User.username == un).first()
        if res:
            return res
        else:
            return None
    except:
        print(Exception)  """


def validate_username(value):
    existing_user = session_user.query(User).filter(User.username == value).first()
    session_user.close()
    if existing_user:
        ##raise ValueError("Username already exists")
        return None
    else:
        return value


def validate_email(value):
    existing_email = session_user.query(User).filter(User.email == value).first()
    session_user.close()
    if existing_email:
        ##raise ValueError("Username already exists")
        return None
    else:
        return value

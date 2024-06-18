from fastapi import APIRouter
from fastapi.responses import JSONResponse
from psycopg2 import IntegrityError
from models.models import (
    session,
    User,
    UserDetail,
    InputUser,
    InputLogin,
    InputUserPay,
    InputUserChanges,
)
from sqlalchemy.orm import joinedload
from auth.security import Security

## para usar la tecnica de carga con union (join loading) para devolver el objeto user con cada uno de sus userDetail


user = APIRouter()


@user.get("/")
def welcome():
    return "Bienvenido a la Api Escuela!!"


@user.get("/users/all")
def obtener_usuarios():
    usuarios = session.query(User).all()
    for ele in usuarios:
        print(ele.userdetail.firstname)
    return usuarios


@user.post("/users/payments")
def show_user_payments(u: InputUserPay):
    usuario = session.query(User).filter(User.id == u.id).first()
    if usuario:
        return usuario.payments
    else:
        return "Usuario no existe"


@user.post("/users/add")  # endpoint
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

                session.add(newUser)
                session.commit()
                session.close()
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
def login_post(userIn: InputLogin):
    try:
        user = session.query(User).filter(User.username == userIn.username).first()
        if not user.password == userIn.password:
            return JSONResponse(
                status_code=401,
                content={
                    "success": False,
                    "message": "Usuario y/o password incorrectos!",
                },
            )
        else:
            authDat = Security.generate_token(user)
            if not authDat:
                return JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "message": "Error de generación de token!",
                    },
                )
            else:
                return JSONResponse(
                    status_code=200, content={"success": True, "token": authDat}
                )

    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Error interno del servidor",
            },
        )


@user.put("/users/emailChange")
def email_update(usrToChange: InputUserChanges):
    user = session.query(User).filter(User.username == usrToChange.username).first()
    if not user:
        return JSONResponse(
            status_code=404, content={"detail": "Usuario no encontrado"}
        )
    EmExist = session.query(User).filter(User.email == usrToChange.email).first()
    if EmExist:
        return JSONResponse(status_code=404, content={"detail": "Email ya existe"})
    user.email = usrToChange.email
    session.commit()
    session.refresh(user)
    return {"mensaje": "Email actualizado!!", "usuario": user}


@user.put("/users/passwordChange")
def email_update(usrToChange: InputUserChanges):
    user = session.query(User).filter(User.username == usrToChange.username).first()
    if not user:
        return JSONResponse(
            status_code=404, content={"detail": "Usuario no encontrado"}
        )
    user.password = usrToChange.password
    session.commit()
    session.refresh(user)
    return {"mensaje": "Password cambiada!!", "usuario": user}


def validate_username(value):
    existing_user = session.query(User).filter(User.username == value).first()
    session.close()
    if existing_user:
        ##raise ValueError("Username already exists")
        return None
    else:
        return value


def validate_email(value):
    existing_email = session.query(User).filter(User.email == value).first()
    session.close()
    if existing_email:
        ##raise ValueError("Username already exists")
        return None
    else:
        return value

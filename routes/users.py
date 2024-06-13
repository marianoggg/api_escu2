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
    Payment,
)
from sqlalchemy.orm import joinedload

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


# El siguiente endpoint intenta devolver de manera erronea
# los pagos del usuario filtrado
# El error radica en devolver el objeto de relacion completo:
# usuario.payments
# en lugar de consultar explicitamente los pagos del usuario
# sobre dicho objeto de relacion.
@user.post("/users/payments1")
def show_user_payments(u: InputUserPay):
    usuario = session.query(User).filter(User.id == u.id).first()
    if usuario:
        return usuario.payments
    else:
        return "Usuario no existe"


# Solucion
@user.post("/users/payments2")
def show_user_payments(u: InputUserPay):
    usuario = session.query(User).filter(User.id == u.id).first()
    if usuario:
        # Filtra los pagos del usuario actual a través de la relación
        payments = usuario.payments.filter(Payment.user == usuario)
        payments1 = usuario.get_payments(
            usuario.id
        )  # opcion usando un filtro definido especialmente en la clase User para filtrar pagos.
        return payments  # Devuelve solo los pagos del usuario filtrado
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
def login_post(user: InputLogin):
    try:
        usu = User(user.username, user.password, "", "")
        res = session.query(User).filter(User.username == usu.username).first()
        if res.password == usu.password:
            return res
        else:
            return None
    except Exception as e:
        print(e)


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

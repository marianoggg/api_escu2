from fastapi import APIRouter
from fastapi.responses import JSONResponse
from psycopg2 import IntegrityError
from models.models import session, User, UserDetail, InputUser, InputLogin
from sqlalchemy.orm import joinedload

## para usar la tecnica de carga con union (join loading) para devolver el objeto user con cada uno de sus userDetail


user = APIRouter()


@user.get("/")
def welcome():
    return "Bienvenido a la Api Escuela!!"


@user.get("/users/all")
def obtener_usuarios():
    try:
        # Carga los detalles del usuario con unión
        usuarios = session.query(User).options(joinedload(User.userdetail)).all()

        # Convierte los usuarios en una lista de diccionarios
        usuarios_con_detalles = []
        for usuario in usuarios:
            payDet = []
            payments = usuario.payments
            for payment in payments:
                payDetail = {
                    "id": payment.id,
                    "date": payment.created_at,
                    "affected_month": payment.affected_month,
                    "amount": payment.amount,
                }
                payDet.append(payDetail)
            usuario_con_detalle = {
                "id": usuario.id,
                "username": usuario.username,
                "email": usuario.email,
                "dni": usuario.userdetail.dni,
                "firstname": usuario.userdetail.firstname,
                "lastname": usuario.userdetail.lastname,
                "type": usuario.userdetail.type,
                "payDetail": payDet,
            }
            usuarios_con_detalles.append(usuario_con_detalle)

        return usuarios_con_detalles
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


""" @user.get("/users/login/{un}")
def login_get(un: str):
    try:
        res = session.query(User).filter(User.username == un).first()
        if res:
            return res
        else:
            return None
    except:
        print(Exception)  """


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

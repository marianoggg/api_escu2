from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.userModel import session, UserDetail, InputUserDetail


userDetail = APIRouter()


@userDetail.get("/userdetail/all")
def get_userDetails():
    try:
        return session.query(UserDetail).all()
    except Exception as e:
        print(e)


@userDetail.post("/userdetail/add")
def add_usuarDetail(userDet: InputUserDetail):
    try:
        usuNuevo = UserDetail(
            userDet.dni,
            userDet.firstname,
            userDet.lastname,
            userDet.type,
            userDet.email,
        )
        session.add(usuNuevo)
        session.commit()
        return "usuario detail agregado"
    except Exception as e:
        print("Error al agregar userDetail --> ", e)
        return JSONResponse(
            status_code=500, content={"detail": "Error al agregar detalles del usuario"}
        )

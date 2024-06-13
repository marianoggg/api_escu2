from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.models import InputPayment, Payment, session, User
from sqlalchemy.orm import joinedload


payment = APIRouter()


@payment.get("/payment/all")
def read_payments():
    return session.query(Payment).all()


@payment.post("/payment/add")
def add_payment(pay: InputPayment):
    usuario = session.query(User).filter(User.id == pay.user_id).first()
    if usuario:
        newPayment = Payment(pay.career_id, pay.user_id, pay.amount, pay.affected_month)

        session.add(newPayment)
        session.commit()
        salida = f"Pago cargado para: {usuario.userdetail.lastname}, {usuario.userdetail.firstname}"
        session.close()
        print(salida)
        return salida
    else:
        return f"El usuario con el id: {pay.user_id} no existe!!"

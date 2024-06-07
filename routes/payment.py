from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.models import InputPayment, Payment, session
from sqlalchemy.orm import joinedload


payment = APIRouter()


@payment.get("/payment/all")
def read_payments():
    payments = session.query(Payment).options(joinedload(Payment.user)).all()

    pyDet = []
    for payment in payments:
        user = payment.user
        userdetail = user.userdetail
        pago_con_detalle = {
            "id": payment.id,
            "date": payment.created_at,
            "user_id": user.id,
            "username": user.username,
            "user_firstname": userdetail.firstname,
            "user_lastname": userdetail.lastname,
            "affected_month": payment.affected_month,
            "amount": payment.amount,
        }
        pyDet.append(pago_con_detalle)

    return pyDet


@payment.post("/payment/add")
def add_career(py: InputPayment):
    try:
        newPayment = Payment(py.user_id, py.career_id, py.amount, py.affected_month)
        session.add(newPayment)
        session.commit()
        res = f"Pago para el alumno {newPayment.user.userdetail.firstname} guardado!"
        session.close()
        print(res)
        return res
    except Exception as ex:
        print("Error al agregar payment --> ", ex)

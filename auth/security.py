import datetime, pytz, jwt
from fastapi.responses import JSONResponse


class Security:
    secret = "hola"
    hoy = datetime.datetime.now(pytz.timezone("America/Buenos_Aires"))
    print(hoy)

    @classmethod
    def generate_token(cls, authUser):
        payload = {
            "iat": cls.hoy,
            "exp": cls.hoy + datetime.timedelta(minutes=480),
            "username": authUser.username,
        }
        try:
            return jwt.encode(payload, cls.secret, algorithm="HS256")
        except Exception:
            return None

    @classmethod
    def verify_token(cls, headers):
        print(headers)
        if headers["authorization"]:
            tkn = headers["authorization"].split(" ")[1]
            try:
                payload = jwt.decode(tkn, cls.secret, algorithms=["HS256"])
                return payload
            except jwt.ExpiredSignatureError:
                return {"success": False, "message": "Token expired!"}
            except jwt.InvalidSignatureError:
                return {"success": False, "message": "Token: signature error!"}
            except jwt.DecodeError as e:
                return {"success": False, "message": "Invalid token!"}
            except Exception as e:
                return {"success": False, "message": "Token: unknown error!"}


##
## explicacion del codigo ##
##

## pip install pyjwt, pytz

##El decorador @classmethod se utiliza para definir métodos de clase. Un método de clase es una función especial que está asociada a una clase en lugar de a una instancia individual de la clase.

##Los métodos de clase se utilizan para realizar operaciones que no dependen de un estado específico de una instancia, sino que se relacionan con la clase en general.

## Entonces generate_token es un metodo de clase y no de instancia

## En un metodo de instancia se utiliza self como argumento a si imismo pero en uno de clase se utiliza cls , el cual representa la clase en si misma.

##por lo tanto

##para usar un metodo de clase no es necesario intanciar previamente su clase

##al payload tiene
# iat: create at del payload del token
# exp: expiracion o tiempo de vida del token
# username: usuario relacionado

## jwt.encode , con el payload y la key secreta, genera el tkn.

## headers["authorization"].split(" ")[1]
## dado que headers["authorization"] devuelve algo como "bearer wieuyroiwueyroiwuer"
## spliter separa el texto en 2 partes, 0 y 1, devolviendo la 1, o sea el tkn

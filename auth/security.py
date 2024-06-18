## pip install pyjwt, pytz
import datetime, pytz, jwt


class Security:
    secret = "hola"
    hoy = datetime.datetime.now()

    @classmethod
    def generate_token(cls, authUser):
        payload = {
            "iat": cls.hoy,
            "exp": cls.hoy + datetime.timedelta(minutes=10),
            "username": authUser.username,
        }
        return jwt.encode(payload, cls.secret)

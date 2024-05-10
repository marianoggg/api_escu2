from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users import user


apiEscu2 = FastAPI()

origins = ["*"]

apiEscu2.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


apiEscu2.include_router(user)

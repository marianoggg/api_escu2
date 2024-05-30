from fastapi import FastAPI
from routes.users import user
from routes.userDetails import userDetail
from fastapi.middleware.cors import CORSMiddleware

apiEscu2 = FastAPI()

apiEscu2.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

apiEscu2.include_router(user)
apiEscu2.include_router(userDetail)

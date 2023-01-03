from fastapi import APIRouter
from fastapi import status
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse
from schemas.users import User

from utils.jwt_manager import create_token

users_router = APIRouter()


@users_router.get('/', tags=['home'], status_code=status.HTTP_200_OK)
def home():
    return HTMLResponse('<h1 style=color:blue> hola mundo </h1>')


@users_router.post('/login', tags=['aut'])
def login(user: User):
    if user.user == "revo" and user.password == "admin":
        token = create_token(user.dict())
        return JSONResponse(content=token, status_code=status.HTTP_200_OK)

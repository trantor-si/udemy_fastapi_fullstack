from starlette.responses import RedirectResponse
from fastapi import Depends, HTTPException, status, APIRouter, Request, \
    Response, Form

# from pydantic import BaseModel
# from typing import Optional
# import domain.models.models as models
# from domain.models.users import UsersModel
# from passlib.context import CryptContext
# from database import SessionLocal, engine
# from datetime import datetime, timedelta
# from jose import jwt, JWTError
# from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm #, OAuth2PasswordBearer
from fastapi.responses import HTMLResponse
from config import get_session
from services import users


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)

@router.post("/token")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_session)):
    token = users.get_access_token(form_data, db)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return True

@router.get("/", response_class=HTMLResponse)
async def authentication_page(request: Request):
    return users.get_login_response({"request": request})

@router.post("/", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_session)):
    try:
        form = users.LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

        validate_user_cookie = await login_for_access_token( \
            response=response, form_data=form, db=db)
        
        if not validate_user_cookie:
            return users.get_login_response({"request": request, "msg": "Incorrect Username or Password"})
        else:
            return response
    
    except HTTPException:
        return users.get_login_response({"request": request, "msg": "Unknown Error"})

@router.get("/logout")
async def logout(request: Request):
    return users.get_logout_response(request)


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return users.get_register_response({"request": request})


@router.post("/register", response_class=HTMLResponse)
async def register_user(request: Request, 
                        email: str = Form(...), username: str = Form(...),
                        firstname: str = Form(...), lastname: str = Form(...),
                        password: str = Form(...), password2: str = Form(...),
                        db: Session = Depends(get_session)):
    return users.register_user(
        request, email, username, firstname, lastname, password, password2, db)
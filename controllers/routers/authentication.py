import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import (APIRouter, Depends, HTTPException, Request, Response,
                     status)
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import repositories.authentication as repository
from config.database import get_session

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"Authentication": "Not authorized"}}
)

templates = Jinja2Templates(directory="templates")
SECRET_KEY = os.getenv('SECRET_KEY', '')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
TIMEDELTA = os.getenv('TIMEDELTA',15)


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")

# SUPPORT FUNCTIONS
def validate_user_cookie(response: Response, form_data: OAuth2PasswordRequestForm,
                                 db: Session):
    token = get_access_token(form_data, db)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return True

def create_access_token(username: str, user_id: int,
                        expires_delta: Optional[timedelta] = None):

    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=TIMEDELTA)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_access_token(form_data: OAuth2PasswordRequestForm, db: Session):
    user = repository.db_get_user(form_data.username, form_data.password, db)
    if not user:
        return False
    token_expires = timedelta(minutes=60)
    token = create_access_token(user.username,
                                user.id,
                                expires_delta=token_expires)
    return token

def get_login_response(request_dict: dict):
    return templates.TemplateResponse(os.getenv('LOGIN_HTML', 'login.html'), request_dict)


def get_home_response(request_dict: dict):
    return templates.TemplateResponse(os.getenv('HOME_HTML', 'login.html'), request_dict)


def get_register_response(request_dict: dict):
    return templates.TemplateResponse(os.getenv('REGISTER_HTML', 'register.html'), request_dict)


def get_addtodo_response(request_dict: dict):
    return templates.TemplateResponse(os.getenv('ADDTODO_HTML', 'add-todo.html'), request_dict)


def get_edittodo_response(request_dict: dict):
    return templates.TemplateResponse(os.getenv('EDITTODO_HTML', 'edit-todo.html'), request_dict)


def get_logout_response(request: Request):
    response = get_login_response(
        {"request": request, "msg": "Logout Successful"})
    response.delete_cookie(key="access_token")
    return response


def get_authentication_page(request: Request):
    return get_login_response({"request": request})


async def get_login(request: Request, db: Session):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()

        response = RedirectResponse(
            url="/todos", status_code=status.HTTP_302_FOUND)
        validated = validate_user_cookie(
            response=response, form_data=form, db=db
        )

        if not validated:
            return get_login_response(
                {"request": request, "msg": "Incorrect Username or Password"}
            )
        else:
            return response

    except HTTPException:
        return get_login_response({"request": request, "msg": "Unknown Error"})


def get_logout(request: Request):
    return get_logout_response(request)


def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        else:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            username: str = payload.get("sub")
            user_id: int = payload.get("id")

            if username is None or user_id is None:
                get_logout(request)
            else:
                return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")


# ROUTES
@router.post("/token")
async def login_for_access_token(response: Response,
                                 form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_session)):
    token = get_access_token(form_data, db)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return True


@router.get("/", response_class=HTMLResponse)
async def authentication_page(request: Request):
    return get_authentication_page(request)


@router.post("/", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_session)):
    return get_login(request, db)


@router.get("/logout")
async def logout(request: Request):
    return get_logout(request)

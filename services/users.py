from fastapi import HTTPException, Request, status
from typing import Optional

# import domain.models.models as models
from domain.models.users import UsersModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError

from fastapi.templating import Jinja2Templates

from config import get_session
from repositories.users import db_exist_user, get_validations, db_register_user


SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"

templates = Jinja2Templates(directory="templates")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")

def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user = db.query(UsersModel)\
        .filter(UsersModel.username == username)\
        .first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int,
                        expires_delta: Optional[timedelta] = None):

    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
          get_logout_response(request)
        else:
          return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
          detail="Not found")


def get_access_token(form_data: OAuth2PasswordRequestForm, db: Session):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return False
    token_expires = timedelta(minutes=60)
    token = create_access_token(user.username,
                                user.id,
                                expires_delta=token_expires)
    return token

def get_login_response(request_dict: dict):
  return templates.TemplateResponse("login.html", request_dict)

def get_register_response(request_dict: dict):
  return templates.TemplateResponse("register.html", request_dict)

def get_logout_response(request: Request):
    response = get_login_response({"request": request, "msg": "Logout Successful"})
    response.delete_cookie(key="access_token")
    return response

def register_user(request: Request, email: str, username: str, firstname: str, 
                  lastname: str, password: str, password2: str, db: Session):
    already_exists = db_exist_user(username, email, db)
    if password != password2 or already_exists:
        return get_register_response({"request": request, "msg": "Invalid registration request"})

    hash_password = get_password_hash(password)
    db_register_user(username, email, firstname, lastname, hash_password, db)

    return get_login_response({"request": request, "msg": "User successfully created"})
























# from fastapi import HTTPException
# from sqlalchemy.orm import Session

# from domain.models.user import User
# from domain.models.item import Item
# from domain.schemas.user import UserCreate
# from domain.schemas.item import ItemCreate
# from repositories import users as user_repository


# def get_user(user_id: int, db: Session):
#     db_user = user_repository.get_user(db, user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# def get_user_by_email(email: str, db: Session):
#     return user_repository.get_user_by_email(db, email)


# def get_users(db: Session):
#     return user_repository.get_users(db)


# def create_user(user: UserCreate, db: Session):
#     db_user = get_user_by_email(user.email, db)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = User(email=user.email, hashed_password=fake_hashed_password)
#     return user_repository.create_user(db, db_user)


# def create_user_item(user_id: int, item: ItemCreate, db: Session):
#     db_user = get_user(user_id, db)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     db_item = Item(**item.dict(), owner_id=user_id)
#     return user_repository.create_user_item(db, db_item)

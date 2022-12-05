from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

import controllers.routers.authentication as auth
import repositories.users as repository
from config.database import get_session

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"user": "Not found"}}
)

@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return auth.get_register_response(request)

@router.post("/register", response_class=HTMLResponse)
async def register_user(request: Request, 
                        email: str = Form(...), username: str = Form(...),
                        firstname: str = Form(...), lastname: str = Form(...),
                        password: str = Form(...), password2: str = Form(...),
                        db : Session = Depends(get_session)):
    already_exists = repository.db_exist_user(username, email, db)
    if password != password2 or already_exists:
        return auth.get_register_response({"request": request, "msg": "Invalid registration request"})
    else:
        hash_password = auth.get_password_hash(password)
        repository.db_register_user(
            username, email, firstname, lastname, hash_password, db
        )
        return auth.get_login_response(
            {"request": request, "msg": "User successfully created"}
        )
        
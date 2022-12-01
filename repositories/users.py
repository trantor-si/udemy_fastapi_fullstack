from sqlalchemy.orm import Session

from domain.models.user import User
from domain.models.item import Todo
from domain.models.users import UsersModel


def get_users(db: Session):
    return db.query(User).all()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_user_todo(db: Session, todo: Todo):
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def db_exist_user(username: str, email: str, db : Session) -> bool:
    exist_username = db.query(UsersModel).filter(UsersModel.username == username).first()
    exist_email = db.query(UsersModel).filter(UsersModel.email == email).first()

    return exist_username is not None or exist_email is not None

def db_register_user(email: str, username: str, firstname: str, 
                  lastname: str, hash_password: str, db: Session):
    user_model = UsersModel()
    user_model.username = username
    user_model.email = email
    user_model.first_name = firstname
    user_model.last_name = lastname

    user_model.hashed_password = hash_password
    user_model.is_active = True

    db.add(user_model)
    db.commit()

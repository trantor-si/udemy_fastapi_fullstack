from sqlalchemy.orm import Session

from domain.models.todos import TodosModel


def db_get_todos(user_id : int, db: Session, skip: int = 0, limit: int = None):
    if limit is None:
        todos = db.query(TodosModel) \
            .filter(TodosModel.owner_id == user_id) \
            .offset(skip).limit(limit) \
            .all()
    else:
        todos = db.query(TodosModel) \
            .filter(TodosModel.owner_id == user_id) \
            .offset(skip) \
            .all()

    return todos

def db_get_todo(user_id: int, todo_id: int, db: Session):
    todo_model = db.query(TodosModel).filter(TodosModel.id == todo_id)\
        .filter(TodosModel.owner_id == user_id).first()
    return todo_model

def db_get_todo(todo_id: int, db: Session):
    todo_model = db.query(TodosModel).filter(TodosModel.id == todo_id).first()
    return todo_model

def db_create_todo(user_id: int, title: str, description: str, priority: int, db: Session):
    todo_model = TodosModel()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    todo_model.complete = False
    todo_model.owner_id = user_id

    db.add(todo_model)
    db.commit()
    db.refresh()

def db_edit_todo_commit(todo_id: int, title: str, description: str, 
                        priority: int, db: Session):

    todo_model = db.query(TodosModel).filter(TodosModel.id == todo_id).first()

    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority

    db.add(todo_model)
    db.commit()
    db.refresh()

def db_delete_todo(todo_id: int, db: Session):
    db.query(TodosModel).filter(TodosModel.id == todo_id).delete()
    db.commit()
    db.refresh()

def db_complete_todo(todo_id: int, db: Session):
    todo_model = db.query(TodosModel).filter(TodosModel.id == todo_id).first()
    todo_model.complete = not todo_model.complete
    db.add(todo_model)
    db.commit()
    db.refresh()

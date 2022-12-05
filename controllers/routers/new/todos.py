from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

import controllers.routers.authentication as auth
import repositories.todos as repository
from config.database import get_session

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}}
)

# ROUTES
@router.get("/test")
async def test(request: Request):
    return auth.get_home_response(request)

@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_session)):
    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    else:
        todos = repository.db_get_todos(user.get("id"), db)
        auth.get_current_user({"request": request, "todos": todos, "user": user})

@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request):
    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    else:
        return auth.get_addtodo_response({"request": request, "user": user})

@router.post("/add-todo", response_class=HTMLResponse)
async def create_todo(request: Request, title: str = Form(...), description: str = Form(...),
                      priority: int = Form(...), db: Session = Depends(get_session)):
    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    else:
        repository.db_create_todo(user.get("id"), title, description, priority, db)
        return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(request: Request, todo_id: int, db: Session = Depends(get_session)):
    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    else:
        todo = repository.db_get_todo(todo_id, db)
        return auth.get_edittodo_response({"request": request, "todo": todo, "user": user})

@router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo_commit(request: Request, todo_id: int, title: str = Form(...),
                           description: str = Form(...), priority: int = Form(...),
                           db: Session = Depends(get_session)):
    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    else:
        repository.db_edit_todo_commit(todo_id, title, description, priority, db)
        return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

@router.get("/delete/{todo_id}")
async def delete_todo(request: Request, todo_id: int, db: Session = Depends(get_session)):
    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    else:
        todo_model = repository.db_get_todo(user.get("id"), todo_id, db)
        if todo_model is None:
            return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
        else:
            repository.db_delete_todo(todo_id, db)
            return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

@router.get("/complete/{todo_id}", response_class=HTMLResponse)
async def complete_todo(request: Request, todo_id: int, db: Session = Depends(get_session)):
    user = await auth.get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    else:
        repository.db_complete_todo(todo_id, db)
        return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)



















# @router.get("/", response_class=HTMLResponse)
# async def read_all_by_user(request: Request, db: Session = Depends(get_session)):

#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todos = db_get_todos(user.get("id"), db)
#     #db.query(TodosModel).filter(TodosModel.owner_id == user.get("id")).all()

#     return templates.TemplateResponse("home.html", {"request": request, "todos": todos, "user": user})


# @router.get("/add-todo", response_class=HTMLResponse)
# async def add_new_todo(request: Request):
#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})


# @router.post("/add-todo", response_class=HTMLResponse)
# async def create_todo(request: Request, title: str = Form(...), description: str = Form(...),
#                       priority: int = Form(...), db: Session = Depends(get_session)):
#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todo_model = TodosModel()
#     todo_model.title = title
#     todo_model.description = description
#     todo_model.priority = priority
#     todo_model.complete = False
#     todo_model.owner_id = user.get("id")

#     db.add(todo_model)
#     db.commit()

#     return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


# @router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
# async def edit_todo(request: Request, todo_id: int, db: Session = Depends(get_session)):

#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todo = db.query(TodosModel).filter(TodosModel.id == todo_id).first()

#     return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})


# @router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
# async def edit_todo_commit(request: Request, todo_id: int, title: str = Form(...),
#                            description: str = Form(...), priority: int = Form(...),
#                            db: Session = Depends(get_session)):

#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todo_model = db.query(TodosModel).filter(TodosModel.id == todo_id).first()

#     todo_model.title = title
#     todo_model.description = description
#     todo_model.priority = priority

#     db.add(todo_model)
#     db.commit()

#     return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


# @router.get("/delete/{todo_id}")
# async def delete_todo(request: Request, todo_id: int, db: Session = Depends(get_session)):

#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todo_model = db.query(TodosModel).filter(TodosModel.id == todo_id)\
#         .filter(TodosModel.owner_id == user.get("id")).first()

#     if todo_model is None:
#         return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

#     db.query(TodosModel).filter(TodosModel.id == todo_id).delete()

#     db.commit()

#     return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


# @router.get("/complete/{todo_id}", response_class=HTMLResponse)
# async def complete_todo(request: Request, todo_id: int, db: Session = Depends(get_session)):

#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todo = db.query(TodosModel).filter(TodosModel.id == todo_id).first()

#     todo.complete = not todo.complete

#     db.add(todo)
#     db.commit()

#     return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette import status
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from config import database
#import domain.models.models as models
from config.server import port
from controllers import app_routes
from domain.models.generic import create_all

app = FastAPI(
  title="Todo App",
  version="0.0.1",
  description="A simple todo app"
)

#models.Base.metadata.create_all(bind=engine)
create_all()

app.mount("/static", StaticFiles(directory="static"), name="static")

for router in app_routes:
    app.include_router(router)

@app.get("/")
async def root():
  return RedirectResponse(url="/todos/", status_code=status.HTTP_302_FOUND)

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=port, reload=True)

# app.include_router(auth.router)
# app.include_router(todos.router)

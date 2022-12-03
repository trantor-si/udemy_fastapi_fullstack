#from database import engine
#from routers import auth, todos
import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

#import domain.models.models as models
from config.server import port
from controllers import app_routes

app = FastAPI(
  title="Todo App",
  version="0.0.1",
  description="A simple todo app",
  openapi_url="/api"
)

#models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

for router in app_routes:
    app.include_router(router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=port, reload=True)

# app.include_router(auth.router)
# app.include_router(todos.router)

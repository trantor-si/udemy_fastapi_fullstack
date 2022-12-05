import os

# from controllers.routers import authentication, todos, users
from controllers.routers import auth, todos, user

app_routes = [
    # authentication.router,
    # users.router,
    auth.router,
    todos.router,
    user.router
]


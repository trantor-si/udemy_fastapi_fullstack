import os

from controllers.routers import authentication, todos, users

app_routes = [
    users.router,
    todos.router,
    authentication.router,
]


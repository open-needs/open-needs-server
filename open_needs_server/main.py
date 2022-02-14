import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from open_needs_server import routers
from open_needs_server.database import create_db_and_tables
from open_needs_server import models, schemas
from open_needs_server.security import auth_backend, get_user_manager


app = FastAPI(
    title="Open-Needs Server",
    version="0.1.0",
    description="REST API Server of Open-Needs",
    license_info={"name": "MIT License",
                  "url": "https://github.com/open-needs/open-needs-server/blob/main/LICENSE"},
    contact={"name": "Open-Needs community",
             "url": "https://github.com/open-needs"}
)

app.include_router(routers.organizations)
app.include_router(routers.projects)
app.include_router(routers.needs)
app.include_router(routers.filters)

fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
    schemas.User,
    schemas.UserCreate,
    schemas.UserUpdate,
    schemas.UserDB,
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"],
)


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

current_active_user = fastapi_users.current_user(active=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

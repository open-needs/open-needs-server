from fastapi import FastAPI

from open_needs_server.database import engine, Base
from open_needs_server import routers

Base.metadata.create_all(bind=engine)

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

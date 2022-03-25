from fastapi import APIRouter, Request

from .schemas import ExtensionBaseSchema


extension_viewer_router = APIRouter(
    prefix="/api/extensions",
    tags=["admin"],
    dependencies=[],
    responses={"404": {"description": "Not found"}}
)


@extension_viewer_router.get("/", response_model=list[ExtensionBaseSchema])
async def rest_read_extensions(request: Request):
    ons_app = request.app
    extensions = []

    for ext in ons_app.ons_extensions.values():
        extensions.append({
            'name': ext.name,
            'description': ext.description,
            'version': ext.version,
        })

    return extensions

import logging
from open_needs_server.extensions.base import ONSExtension
from open_needs_server.version import VERSION

from .routers import projects_router

log = logging.getLogger(__name__)

PROJECT_EVENTS = [
    ('project_create', 'Called before project gets created'),
    ('project_create_done', 'Called after project got created'),
    ('project_read', 'Called before project get read'),
    ('project_read_done', 'Called after project got read'),
    ('project_update', 'Called before project gets updated'),
    ('project_update_done', 'Called after project got updated'),
    ('project_delete', 'Called before project gets deleted'),
    ('project_delete_done', 'Called after project got deleted'),
]


class ProjectExtension(ONSExtension):
    """Project handling"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = VERSION

        for event in PROJECT_EVENTS:
            self.register_event(*event)

        self.register_router(projects_router)

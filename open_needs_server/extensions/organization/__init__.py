import logging
from open_needs_server.extensions.base_extension import ONSExtension
from .routers import organizations_router

log = logging.getLogger(__name__)

ORG_EVENTS = [
    ('org_create', 'Called before organization gets created'),
    ('org_create_done', 'Called after organization got created'),
    ('org_read', 'Called before organization get read'),
    ('org_read_done', 'Called after organization got read'),
    ('org_update', 'Called before organization gets updated'),
    ('org_update_done', 'Called after organization got updated'),
    ('org_delete', 'Called before organization gets deleted'),
    ('org_delete_done', 'Called after organization got deleted'),
]


class OrganizationExtension(ONSExtension):
    """Organization handling"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for event in ORG_EVENTS:
            self.register_event(*event)

        self.register_router(organizations_router)

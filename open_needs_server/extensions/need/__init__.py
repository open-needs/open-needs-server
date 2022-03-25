import logging
from open_needs_server.extensions.base_extension import ONSExtension
from .routers import needs_router

log = logging.getLogger(__name__)

ORG_EVENTS = [
    ('need_create', 'Called before need gets created'),
    ('need_create_done', 'Called after need got created'),
    ('need_read', 'Called before need get read'),
    ('need_read_done', 'Called after need got read'),
    ('need_update', 'Called before need gets updated'),
    ('need_update_done', 'Called after need got updated'),
    ('need_delete', 'Called before need gets deleted'),
    ('need_delete_done', 'Called after need got deleted'),
]


class NeedExtension(ONSExtension):
    """Need object handling"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for event in ORG_EVENTS:
            self.register_event(*event)

        self.register_router(needs_router)

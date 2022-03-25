import logging
from open_needs_server.extensions.base_extension import ONSExtension

log = logging.getLogger(__name__)

PROJECT_EVENTS = [
    ('project_create', 'Called before organization gets created'),
    ('project_create_done', 'Called after organization got created'),
    ('project_read', 'Called before organization get read'),
    ('project_read_done', 'Called after organization got read'),
    ('project_update', 'Called before organization gets updated'),
    ('project_update_done', 'Called after organization got updated'),
    ('project_delete', 'Called before organization gets deleted'),
    ('project_delete_done', 'Called after organization got deleted'),
]


class ProjectExtension(ONSExtension):
    """Maintains the needed configuration for handling projects"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for event in PROJECT_EVENTS:
            self.register_event(*event)

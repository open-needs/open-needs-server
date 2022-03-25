import logging
from open_needs_server.extensions.base_extension import ONSExtension
from .routers import filter_router

log = logging.getLogger(__name__)

FILTER_EVENTS = [
]


class FilterExtension(ONSExtension):
    """Adds filter features"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for event in FILTER_EVENTS:
            self.register_event(*event)

        self.register_router(filter_router)

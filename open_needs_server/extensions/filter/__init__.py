import logging
from open_needs_server.extensions.base import ONSExtension
from .routers import filter_router

from open_needs_server.version import VERSION


log = logging.getLogger(__name__)

FILTER_EVENTS = []


class FilterExtension(ONSExtension):
    """Adds filter features"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = VERSION

        for event in FILTER_EVENTS:
            self.register_event(*event)

        self.register_router(filter_router)

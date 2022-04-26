import logging
from open_needs_server.extensions.base import ONSExtension
from open_needs_server.version import VERSION

from .routers import extension_viewer_router

log = logging.getLogger(__name__)


class ExtensionViewerExtension(ONSExtension):
    """Basic extension information"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = VERSION

        self.register_router(extension_viewer_router)

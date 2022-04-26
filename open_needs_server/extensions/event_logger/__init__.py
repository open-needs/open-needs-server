import logging
from open_needs_server.extensions.base import ONSExtension
from open_needs_server.version import VERSION

log = logging.getLogger(__name__)


class EventLoggerExtension(ONSExtension):
    """Logs event information"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = VERSION

        @self.ons_app.on_event("startup")
        async def on_startup():
            self._register_own_listeners()

    def _register_own_listeners(self):
        for event in self.ons_app.ons_events:
            self.register_listener(event, self._event_logger)

    def _event_logger(self, event, data, extra, ext):
        self.print(f'{event} fired by {ext} with {str(data)[:50]}')
        # A listener functions needs to return the data, in this case it
        # is untouched
        return data

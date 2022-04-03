import logging
from open_needs_server.extensions.base_extension import ONSExtension
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

    def _event_logger(self, event, data, extra):
        print(f'{event} fired with {data}')

from open_needs_server.app import OpenNeedsServerApp
from open_needs_server.exceptions import ONSExtensionException

import logging


log = logging.getLogger(__name__)


class ONSExtension:

    def __init__(self, ons_app: OpenNeedsServerApp, version: str = "0.0.0"):
        self.ons_app = ons_app
        self.name = type(self).__name__
        self.version = version
        self.description = self.__doc__

    def register_event(self, event: str, description: str):
        if event not in self.ons_app.ons_events:
            self.ons_app.ons_events[event] = {
                "extension": self.name,
                "description": description,
                "listeners": []
            }
            log.debug(f'Event registered: {event} by {self.name}')
        else:
            owner = self.ons_app.ons_events[event]['owner']
            log.debug(f'Event already exist: {event} {self.name} (owner={owner})')

    def register_listener(self, event: str, func: object, extra: dict = None):
        if event not in self.ons_app.ons_events:
            raise ONSExtensionException(f'Unknown event: {event}')

        if extra is None:
            extra = {}

        self.ons_app.ons_events[event]["listeners"] = {
            'extension': self.name,
            'func': func,
            'extra': extra
        }
        log.debug(f'Listener registered: On "{event} for {self.name}')

    def fire_event(self, event, data):
        log.debug(f'Event "{event} fired for {len(self.ons_app.ons_events[event])} listeners')

        if event not in self.ons_app.ons_events:
            raise ONSExtensionException(f'Unknown event: {event}')

        for listener in self.ons_app.ons_events[event]:
            log.debug(f'Calling listener {listener["extension"]}:{listener["func"].__name__} for event {event}')
            listener['func'](event, data=data, extra=listener['extra'])

    def register_router(self, router, *args, **kwargs):
        self.ons_app.include_router(router, *args, **kwargs)
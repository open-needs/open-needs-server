from open_needs_server.app import OpenNeedsServerApp
from open_needs_server.exceptions import ONSExtensionException

import logging


log = logging.getLogger(__name__)


class ONSExtension:

    def __init__(self, ons_app: OpenNeedsServerApp, name: str, version: str):
        self.ons_app = ons_app
        self.name = name
        self.version = version
        self.description = self.__doc__

        if self.name in self.ons_app.ons_extensions:
            raise KeyError(f"Extension already registered: {self.name}")

        self.ons_app.ons_extensions[self.name] = self
        log.debug(f'Extension loaded: {self.name} {self.version}')

    def register_event(self, event: str, description: str):
        if event not in self.ons_app.ons_events:
            self.ons_app.ons_events[event] = {
                "owner": self.name,
                "description": description,
                "listeners": []
            }
            log.debug(f'Event registered: {event} by {self.name}')
        else:
            owner = self.ons_app.ons_events[event]['owner']
            log.debug(f'Event already exist: {event} {self.name} (owner={owner})')

    def register_listener(self, event: str, func: object):
        if event not in self.ons_app.ons_events:
            raise ONSExtensionException(f'Unknown event: {event}')

        self.ons_app.ons_events[event]["listeners"] = {
            'extension': self.name,
            'func': func
        }

    def register_router(self, router, *args, **kwargs):
        self.ons_app.include_router(router, *args, **kwargs)
from rich import print

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

    def print(self, msg):
        print(f'[blue]{self.name[:20]:<20}[/blue]: {msg}')

    def register_role(self, role: str, description: str):
        if role not in self.ons_app.ons_roles:
            self.ons_app.ons_roles[role] = {
                "name": role,
                "extension": self.name,
                "description": description,
                "users": []
            }
            log.debug(f'Role registered: {role} by {self.name}')
        else:
            extension = self.ons_app.ons_roles[role]['extension']
            log.debug(f'Role already exist: {role} {self.name} (extension={extension})')

    def register_event(self, event: str, description: str):
        if event not in self.ons_app.ons_events:
            self.ons_app.ons_events[event] = {
                "extension": self.name,
                "description": description,
                "listeners": []
            }
            log.debug(f'Event registered: {event} by {self.name}')
        else:
            extension = self.ons_app.ons_events[event]['extension']
            log.debug(f'Event already exist: {event} {self.name} (extension={extension})')

    def register_listener(self, event: str, func: object, extra: dict = None):
        if event not in self.ons_app.ons_events:
            raise ONSExtensionException(f'Unknown event: {event}')

        if extra is None:
            extra = {}

        self.ons_app.ons_events[event]["listeners"].append({
            'extension': self.name,
            'func': func,
            'extra': extra
        })
        log.debug(f'Listener registered: On "{event} for {self.name}')

    def fire_event(self, event, data):
        if event not in self.ons_app.ons_events:
            raise ONSExtensionException(f'Unknown event: {event} fired by {self.name}')

        log.debug(f'Event "{event} fired for {len(self.ons_app.ons_events[event]["listeners"])} listeners')

        # Calls all listeners in a fix sequence. No parallel execution
        for listener in self.ons_app.ons_events[event]['listeners']:
            log.debug(f'Calling listener {listener["extension"]}:{listener["func"].__name__} for event {event}')
            data = listener['func'](event, data=data, extra=listener['extra'], ext=self.name)

        return data

    def register_router(self, router, *args, **kwargs):
        self.ons_app.include_router(router, *args, **kwargs)


class OnsExtensionException(BaseException):
    def __init__(self, msg, **args):
        self.msg = msg

    def __repr__(self):
        return f'{self.__name__}: {self.msg}'

import logging

from fastapi import HTTPException

from jsonschema import validate, ValidationError
from jsonschema.exceptions import SchemaError

from open_needs_server.extensions.base import ONSExtension
from open_needs_server.version import VERSION
from open_needs_server.extensions.base import OnsExtensionException

from .routers import domains_router

log = logging.getLogger(__name__)

DOMAIN_EVENTS = [
    ("domain_create", "Called before domain gets created"),
    ("domain_create_done", "Called after domain got created"),
    ("domain_read", "Called before domain get read"),
    ("domain_read_done", "Called after domain got read"),
    ("domain_update", "Called before domain gets updated"),
    ("domain_update_done", "Called after domain got updated"),
    ("domain_delete", "Called before domain gets deleted"),
    ("domain_delete_done", "Called after domain got deleted"),
]


class DomainExtension(ONSExtension):
    """Domain handling"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = VERSION

        for event in DOMAIN_EVENTS:
            self.register_event(*event)

        self.register_router(domains_router)

        self.register_role("view_domains_all", "Can read all domains")
        self.register_role("change_domains_all", "Can change all domains")
        self.register_role("delete_domains_all", "Can delete all domains")

        @self.ons_app.on_event("startup")
        async def on_startup():
            self.register_listener("need_create", self._check_need)

    def _check_need(self, event, data, extra, ext):
        self.print(f'Checking need: {data["need"]}')
        project = data["project"]

        passed = False
        for domain in project.domains:
            self.print(f"Domain check: {domain.title} ({domain.id})")
            try:
                validate(instance=data["need"], schema=domain.jsonschema)
            except ValidationError:
                break  # Next check needed
            except SchemaError:
                raise HTTPException(500, f"Domain {domain.title} has invalid schema.")
            log.debug(f"Domain {domain.title} passed")
            passed = True

        if passed or not project.domains:
            return data
        else:
            raise HTTPException(400, "Need does not match any domain")

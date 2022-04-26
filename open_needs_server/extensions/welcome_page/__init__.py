import os
import logging
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from open_needs_server.extensions.base import ONSExtension
from open_needs_server.version import VERSION


log = logging.getLogger(__name__)


class WelcomePage(ONSExtension):
    """Basic entry page with links to other pages"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = VERSION

        template_path = os.path.join(os.path.dirname(__file__), '_templates')
        templates = Jinja2Templates(directory=template_path)

        self.context = {"ons_app": self.ons_app}

        # Register welcome route
        @self.ons_app.get("/")
        async def welcome(request: Request):
            return templates.TemplateResponse("ons_frame.html", self.context | {"request": request})

        @self.ons_app.get("/welcome.html")
        async def welcome(request: Request):
            return templates.TemplateResponse("welcome.html", self.context | {"request": request})


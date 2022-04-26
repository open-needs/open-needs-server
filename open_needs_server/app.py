import importlib
import logging
import os.path

from open_needs_server.version import VERSION
import time
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from rich.console import Console
from rich.markdown import Markdown


log = logging.getLogger(__name__)

WELCOME = f"""
# Open-Needs Server {VERSION}
"""


class OpenNeedsServerApp(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ons_extensions = {}
        self.ons_events = {}
        self.ons_extensions = {}
        self.ons_roles = {}

        self.ons_version = VERSION

        template_path = os.path.join(os.path.dirname(__file__), '_templates')
        static_path = os.path.join(os.path.dirname(__file__), '_static')

        self.template = Jinja2Templates(directory=template_path)
        self.mount("/static", StaticFiles(directory=static_path), name="static")

        self.console = Console()  # Create rich console
        self._welcome_text()

    def load_extensions(self, extensions):
        for extension in extensions:
            ext_mod, ext_class = extension.split(":")
            try:
                module = importlib.import_module(ext_mod)
            except ModuleNotFoundError:
                raise ONSExceptions(f'Extension module could not be imported/found: {ext_mod}')

            try:
                clazz = getattr(module, ext_class)
            except AttributeError:
                raise ONSExceptions(f'Extension class could not be found: {ext_class}')

            ext_obj = clazz(self)  # Initialize extension
            try:
                self.ons_extensions[ext_obj.name] = ext_obj
            except KeyError:
                raise ONSExceptions(f"Extension already registered: {ext_obj.name}")
            log.debug(f'Extension loaded: {ext_obj.name} {ext_obj.version}')

    def _welcome_text(self):
        text = Markdown(WELCOME)
        self.console.print(text)

    def startup_report(self, start_time):
        startup_time = time.time() - start_time

        self.console.rule(f"[bold red]Statistics")
        print(f'Extensions:   {len(self.ons_extensions)}')
        print(f'Events:       {len(self.ons_events)}')
        print(f'Roles:       {len(self.ons_roles)}')
        print(f'Startup time: {startup_time}')

        self.console.rule(f"[bold red]Extensions")
        for ext in self.ons_extensions.values():
            print(f'{ext.name:25}\t{ext.version:10}\t{ext.description}')


class ONSExceptions(BaseException):
    """Generic ONS Exception"""

import os.path

from open_needs_server.version import VERSION
import time
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from rich.console import Console
from rich.markdown import Markdown



WELCOME = f"""
# Open-Needs Server {VERSION}
"""


class OpenNeedsServerApp(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ons_extensions = {}
        self.ons_events = {}
        self.ons_version = VERSION

        template_path = os.path.join(os.path.dirname(__file__), '_templates')
        static_path = os.path.join(os.path.dirname(__file__), '_static')

        self.template = Jinja2Templates(directory=template_path)
        self.mount("/static", StaticFiles(directory=static_path), name="static")

        self.console = Console()  # Create rich console
        self._welcome_text()

    def _welcome_text(self):
        text = Markdown(WELCOME)
        self.console.print(text)

    def startup_report(self, start_time):
        startup_time = time.time() - start_time

        self.console.rule(f"[bold red]Statistics")
        print(f'Extensions:   {len(self.ons_extensions)}')
        print(f'Events:       {len(self.ons_events)}')
        print(f'Startup time: {startup_time}')

        self.console.rule(f"[bold red]Extensions")
        for ext in self.ons_extensions.values():
            print(f'{ext.name:15}\t{ext.version:10}\t{ext.description}')

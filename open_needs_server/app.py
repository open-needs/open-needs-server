from open_needs_server.version import VERSION
import time
from fastapi import FastAPI
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

        self.console = Console()  # Create rich console
        self.welcome_text()

    def welcome_text(self):
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

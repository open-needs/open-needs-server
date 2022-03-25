from fastapi import FastAPI
from rich.console import Console


class OpenNeedsServerApp(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ons_extensions = {}
        self.ons_events = {}

        self.console = Console()  # Create rich console

    def startup_report(self):
        self.console.rule(f"[bold red]Statistics")
        print(f'Extensions: {len(self.ons_extensions)}')
        print(f'Events:     {len(self.ons_events)}')

        self.console.rule(f"[bold red]Extensions")
        for ext in self.ons_extensions.values():
            print(f'{ext.name:15}\t{ext.version:10}\t{ext.description}')

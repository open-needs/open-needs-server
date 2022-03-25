import json
import rich_click as click

from rich import print
from rich.console import Console

import requests
import urllib.parse


console = Console()


@click.command()
@click.argument('input', type=click.File('rb'))
@click.option('--server', default='127.0.0.1', type=str)
@click.option('--port', default='8000', type=str)
def install(input, server, port):
    base_url = f'http://{server}:{port}'
    user_url = urllib.parse.urljoin(base_url, 'auth/register')
    org_url = urllib.parse.urljoin(base_url, 'api/organizations')
    project_url = urllib.parse.urljoin(base_url, 'api/projects')
    needs_url = urllib.parse.urljoin(base_url, 'api/needs')

    data = json.load(input)

    console.rule(f"[bold red]Users")
    for index, user in enumerate(data['users']):
        r = requests.post(user_url, json=user)
        print(f'{index}. {user["email"]}\t{r.status_code}: {r.text if r.status_code > 300 else ""}')

    console.rule(f"[bold red]Organizations")
    for index, org in enumerate(data['organizations']):
        r = requests.post(org_url, json=org)
        print(f'{index}. {org["title"]}\t{r.status_code}: {r.text if r.status_code != 200 else ""}')

    console.rule(f"[bold red]Projects")
    for index, project in enumerate(data['projects']):
        r = requests.post(project_url, json=project)
        print(f'{index}. {project["title"]}\t {r.status_code}: {r.text if r.status_code != 200 else ""}')

    console.rule(f"[bold red]Needs")
    for index, need in enumerate(data['needs']):
        r = requests.post(needs_url, json=need)
        print(f'{index}. {need["title"]}\t {r.status_code}: {r.text if r.status_code != 200 else ""}')

if __name__ == '__main__':
    install()

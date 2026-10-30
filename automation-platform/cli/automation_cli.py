import click
import requests
import json
from typing import Optional

API_BASE_URL = "http://localhost:5000/api"

@click.group()
def cli():
    """Automation Platform CLI - Manage automation tasks."""
    pass

@cli.command()
@click.option('--type', 'task_type', required=True, 
              type=click.Choice(['backup', 'deploy', 'cleanup']))
@click.option('--params', required=True, help='JSON parameters')
@click.option('--priority', default='medium', 
              type=click.Choice(['high', 'medium', 'low']))
def submit(task_type: str, params: str, priority: str):
    """Submit new automation task."""
    try:
        parameters = json.loads(params)
    except json.JSONDecodeError as e:
        click.echo(click.style(f"Error parsing JSON parameters: {e}", fg='red'))
        return
        
    payload = {
        "task_type": task_type,
        "parameters": parameters,
        "priority": priority
    }
    
    try:
        resp = requests.post(f"{API_BASE_URL}/tasks", json=payload)
        if resp.status_code == 201:
            data = resp.json()
            click.echo(click.style("✓ Task submitted successfully!", fg='green'))
            click.echo(f"Task ID: {click.style(data['task_id'], fg='cyan', bold=True)}")
            click.echo(f"Status: {data['status']}")
        else:
            click.echo(click.style(f"Failed to submit task: {resp.json().get('error', resp.text)}", fg='red'))
    except requests.exceptions.ConnectionError:
        click.echo(click.style("Error: Could not connect to API server at http://localhost:5000", fg='red'))

@cli.command()
@click.argument('task_id')
def status(task_id: str):
    """Check status of automation task."""
    try:
        resp = requests.get(f"{API_BASE_URL}/tasks/{task_id}")
        if resp.status_code == 200:
            data = resp.json()
            click.echo(click.style(f"=== Task Details: {task_id} ===", fg='cyan', bold=True))
            click.echo(f"Type: {data.get('task_type')}")
            click.echo(f"Priority: {data.get('priority')}")
            
            status_val = data.get('status')
            color = 'yellow' if status_val == 'RUNNING' else ('green' if status_val == 'COMPLETED' else 'red')
            click.echo(f"Status: {click.style(status_val, fg=color, bold=True)}")
            
            click.echo(f"Parameters: {json.dumps(data.get('parameters'))}")
            if 'result' in data:
                click.echo(click.style(f"Result: {data['result']}", fg='green'))
            if 'error' in data:
                click.echo(click.style(f"Error: {data['error']}", fg='red'))
        else:
            click.echo(click.style(f"Task not found or error: {resp.status_code}", fg='red'))
    except requests.exceptions.ConnectionError:
        click.echo(click.style("Error: Could not connect to API server.", fg='red'))

@cli.command()
@click.option('--status', help='Filter by status')
@click.option('--type', 'task_type', help='Filter by task type')
def list(status: Optional[str], task_type: Optional[str]):
    """List automation tasks with optional filters."""
    params = {}
    if status:
        params['status'] = status
    if task_type:
        params['type'] = task_type
        
    try:
        resp = requests.get(f"{API_BASE_URL}/tasks", params=params)
        if resp.status_code == 200:
            data = resp.json()
            tasks = data.get('tasks', [])
            click.echo(click.style(f"Found {data.get('count')} tasks:", fg='cyan', bold=True))
            for t in tasks:
                click.echo(f" - [{t.get('task_id')}] Type: {t.get('task_type')} | Status: {t.get('status')}")
        else:
            click.echo(click.style("Failed to fetch tasks.", fg='red'))
    except requests.exceptions.ConnectionError:
        click.echo(click.style("Error: Could not connect to API server.", fg='red'))

if __name__ == '__main__':
    cli()

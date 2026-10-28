#!/usr/bin/env python3
import click
import requests
from tabulate import tabulate
import json
import sys
import os
from pathlib import Path

# Configuration
API_BASE_URL = "http://127.0.0.1:5000/api"
TOKEN_FILE = Path.home() / ".user_cli_token"

def save_token(token):
    """Save authentication token to file with secure permissions (0600)."""
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
    os.chmod(TOKEN_FILE, 0o600)

def load_token():
    """Load authentication token from file if it exists."""
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    return None

def delete_token():
    """Delete stored authentication token file."""
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()

class APIClient:
    """Client for interacting with the User API"""
    
    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.token = token
        self.session = requests.Session()
        if self.token:
            self.session.headers.update({
                'Authorization': f'Bearer {self.token}'
            })
    
    def health_check(self):
        """Check API health status"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            click.echo("Error: Cannot connect to API server. Ensure api_server.py is running.", err=True)
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            click.echo(f"Error: {str(e)}", err=True)
            sys.exit(1)
    
    def get_users(self):
        """Retrieve all users from the API"""
        try:
            response = self.session.get(f"{self.base_url}/users")
            if response.status_code == 401:
                click.echo("Error: Authentication failed. Invalid or missing token.", err=True)
                sys.exit(1)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            click.echo(f"Error fetching users: {e}", err=True)
            sys.exit(1)
    
    def get_user_by_id(self, user_id):
        """Retrieve a specific user by ID"""
        try:
            response = self.session.get(f"{self.base_url}/users/{user_id}")
            if response.status_code == 401:
                click.echo("Error: Authentication failed. Invalid or missing token.", err=True)
                sys.exit(1)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            click.echo(f"Error fetching user: {e}", err=True)
            sys.exit(1)

@click.group()
def cli():
    """User Management CLI - Interact with User API"""
    pass

@cli.command()
def health():
    """Check API server health"""
    client = APIClient(API_BASE_URL)
    result = client.health_check()
    click.echo(f"Status: {result.get('status')}")
    click.echo(f"Service: {result.get('service')}")

@cli.command()
@click.option('--token', default=None, help='API authentication token')
def list_users(token):
    """List all users in a tabular format"""
    active_token = token or load_token()
    if not active_token:
        click.echo("Error: No authentication token provided or found. Use 'login' or pass --token.", err=True)
        sys.exit(1)
        
    client = APIClient(API_BASE_URL, token=active_token)
    data = client.get_users()
    users = data.get("users", [])
    
    if not users:
        click.echo("No users found.")
        return
        
    table_data = [[u["id"], u["name"], u["role"]] for u in users]
    click.echo(tabulate(table_data, headers=["ID", "Name", "Role"], tablefmt="pretty"))

@cli.command()
@click.argument('user_id', type=int)
@click.option('--token', default=None, help='API authentication token')
def get_user(user_id, token):
    """Get user details by ID"""
    active_token = token or load_token()
    if not active_token:
        click.echo("Error: No authentication token provided or found. Use 'login' or pass --token.", err=True)
        sys.exit(1)
        
    client = APIClient(API_BASE_URL, token=active_token)
    user = client.get_user_by_id(user_id)
    
    if user:
        click.echo(f"User ID: {user.get('id')}")
        click.echo(f"Name:    {user.get('name')}")
        click.echo(f"Role:    {user.get('role')}")
    else:
        click.echo(f"User with ID {user_id} not found.", err=True)

@cli.command()
@click.argument('token')
def login(token):
    """Save authentication token for future use after validation"""
    client = APIClient(API_BASE_URL, token=token)
    # Test token validity with health or users endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/users", headers={'Authorization': f'Bearer {token}'})
        if response.status_code == 200:
            save_token(token)
            click.echo("Successfully authenticated and saved token.")
        else:
            click.echo("Error: Invalid token provided.", err=True)
            sys.exit(1)
    except Exception as e:
        click.echo(f"Error during login validation: {e}", err=True)
        sys.exit(1)

@cli.command()
def logout():
    """Remove saved authentication token"""
    delete_token()
    click.echo("Successfully logged out (token removed).")

@cli.command()
def whoami():
    """Display current authentication status"""
    token = load_token()
    if token:
        click.echo(f"Authenticated: Yes (Token stored at {TOKEN_FILE})")
    else:
        click.echo("Authenticated: No (No active token found)")

if __name__ == '__main__':
    cli()

# CLI and API Integration Lab

A robust Python command-line interface tool built with `Click`, `Requests`, and `Tabulate` designed to interact securely with authenticated REST APIs.

## Objectives
- Implement a structured CLI application with subcommands and argument parsing.
- Integrate Bearer token authentication into HTTP request headers via persistent sessions.
- Manage local credential caching securely with strict file permissions (`0600`).
- Format JSON payloads into clean, readable tabular outputs using `tabulate`.

## Tools Used
- **Click** for advanced CLI command parsing and decorators
- **Requests** for HTTP REST operations and session management
- **Tabulate** for professional terminal table rendering
- **Flask & Flask-HTTPAuth** for building the mock backend server

## Key Skills Demonstrated
- **API Client Architecture:** Separating transport logic (`APIClient`) from command-line interface definitions (`Click` groups and commands).
- **Secure Token Storage:** Safely storing authentication tokens in hidden home directory files with restricted file modes.
- **Defensive Error Handling:** Catching connection errors, HTTP 401 unauthorized responses, and 404 missing resource exceptions cleanly.

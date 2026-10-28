# Opsctl CLI Foundation

A modular, production-grade Command Line Interface (CLI) tool built in Python for operational system management, service health checks, deployments, and persistent configuration management.

## Objectives
- Design and implement a structured CLI tool architecture using Python's `argparse` with subcommands.
- Implement robust environment validation, colored terminal output helpers, and structured JSON/text formatting.
- Build persistent local configuration handling (`~/.opsctl/config.json`).
- Package the tool professionally using setuptools with entry points for global system execution.

## Tools Used
- **Python 3** (`argparse`, `json`, `os`, `sys`, `time`)
- **Setuptools** for CLI packaging and distribution
- **Linux Terminal** & Shell environment

## Key Skills Demonstrated
- **CLI Engineering:** Designing scalable argument parsers with nested subparsers and custom formatting.
- **State Persistence:** Managing local configuration files safely with directory auto-creation and error handling.
- **Software Modularity:** Clean separation of concerns across command modules (`status`, `deploy`, `config`) and utility helpers.
- **DevOps Tooling:** Building developer-facing CLI utilities for infrastructure automation and service management.

## Troubleshooting Log
- **Subparser Resolution:** Ensured `dest='command'` and `set_defaults(func=execute)` are correctly configured for clean command routing.
- **Config Directory Isolation:** Handled missing configuration files and directories gracefully using `os.makedirs` and `os.path.expanduser`.
